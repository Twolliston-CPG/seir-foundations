#!/usr/bin/env bash
# create_balerica_with_gateway_vpc.sh
# Same as create_balerica_vpc.sh but adds a NAT gateway in public-a and
# a 0.0.0.0/0 → NAT route on private1 and private2 route tables.
#
# NAT gateway incurs AWS charges (~$0.045/hr + data transfer).
# Run delete_balerica_vpc.sh when finished to avoid ongoing costs.
#
# Requires Bash 4+ (macOS: /opt/homebrew/bin/bash create_balerica_with_gateway_vpc.sh)
set -Eeuo pipefail

export AWS_REGION="${AWS_REGION:-us-east-1}"
export AWS_DEFAULT_REGION="$AWS_REGION" AWS_PAGER=""
PROJECT="${PROJECT:-balerica}"
NETWORK_PREFIX="${NETWORK_PREFIX:-10.20}"
VPC_CIDR="$NETWORK_PREFIX.0.0/16"
STATE_FILE="${PROJECT}-network.env"

trap 'echo "Deployment stopped at line $LINENO. Inspect $STATE_FILE and AWS before retrying; partial resources may remain." >&2' ERR

command -v aws >/dev/null
aws sts get-caller-identity

[[ ! -e "$STATE_FILE" ]] || { echo "State file already exists: $STATE_FILE" >&2; exit 1; }

existing=$(aws ec2 describe-vpcs --filters "Name=tag:Name,Values=$PROJECT-vpc" --query 'length(Vpcs)' --output text)
[[ "$existing" == 0 ]] || { echo 'Named VPC already exists. Inspect it before proceeding.' >&2; exit 1; }

for az in a b c; do
  state=$(aws ec2 describe-availability-zones --zone-names "$AWS_REGION$az" --query 'AvailabilityZones[0].State' --output text)
  [[ "$state" == available ]] || { echo "AZ $AWS_REGION$az unavailable" >&2; exit 1; }
done

umask 077
: > "$STATE_FILE"
save() { printf '%s=%q\n' "$1" "$2" >> "$STATE_FILE"; }
save AWS_REGION "$AWS_REGION"
save VPC_CIDR "$VPC_CIDR"

# --- VPC ---
VPC_ID=$(aws ec2 create-vpc \
  --cidr-block "$VPC_CIDR" \
  --tag-specifications "ResourceType=vpc,Tags=[{Key=Name,Value=$PROJECT-vpc}]" \
  --query Vpc.VpcId --output text)
save VPC_ID "$VPC_ID"
aws ec2 wait vpc-available --vpc-ids "$VPC_ID"
aws ec2 modify-vpc-attribute --vpc-id "$VPC_ID" --enable-dns-support '{"Value":true}'
aws ec2 modify-vpc-attribute --vpc-id "$VPC_ID" --enable-dns-hostnames '{"Value":true}'

# --- Internet Gateway ---
IGW_ID=$(aws ec2 create-internet-gateway \
  --tag-specifications "ResourceType=internet-gateway,Tags=[{Key=Name,Value=$PROJECT-igw}]" \
  --query InternetGateway.InternetGatewayId --output text)
save IGW_ID "$IGW_ID"
aws ec2 attach-internet-gateway --internet-gateway-id "$IGW_ID" --vpc-id "$VPC_ID"

# --- Elastic IP for NAT gateway ---
EIP_ALLOC_ID=$(aws ec2 allocate-address \
  --domain vpc \
  --tag-specifications "ResourceType=elastic-ip,Tags=[{Key=Name,Value=$PROJECT-nat-eip}]" \
  --query AllocationId --output text)
save EIP_ALLOC_ID "$EIP_ALLOC_ID"
echo "Elastic IP allocated: $EIP_ALLOC_ID"

# NAT_GW_ID and the first public subnet ID are set during the public tier iteration
# and used when configuring private tier route tables.
NAT_GW_ID=""
FIRST_PUBLIC_SUBNET=""

# --- Tiers: public → private1 → private2 ---
for tier in public private1 private2; do
  case "$tier" in public) base=0;; private1) base=10;; private2) base=20;; esac

  rt=$(aws ec2 create-route-table \
    --vpc-id "$VPC_ID" \
    --tag-specifications "ResourceType=route-table,Tags=[{Key=Name,Value=$PROJECT-$tier-rt}]" \
    --query RouteTable.RouteTableId --output text)
  save "${tier^^}_RT_ID" "$rt"

  if [[ "$tier" == public ]]; then
    # Public traffic exits through the Internet Gateway
    aws ec2 create-route \
      --route-table-id "$rt" \
      --destination-cidr-block 0.0.0.0/0 \
      --gateway-id "$IGW_ID" >/dev/null
  else
    # Private traffic exits through the NAT gateway (created after public subnets)
    aws ec2 create-route \
      --route-table-id "$rt" \
      --destination-cidr-block 0.0.0.0/0 \
      --nat-gateway-id "$NAT_GW_ID" >/dev/null
  fi

  n=0
  for az in a b c; do
    n=$((n+1))
    cidr="$NETWORK_PREFIX.$((base+n)).0/24"
    subnet=$(aws ec2 create-subnet \
      --vpc-id "$VPC_ID" \
      --cidr-block "$cidr" \
      --availability-zone "$AWS_REGION$az" \
      --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=$PROJECT-$tier-$az}]" \
      --query Subnet.SubnetId --output text)
    save "${tier^^}_${az^^}_ID" "$subnet"
    aws ec2 wait subnet-available --subnet-ids "$subnet"

    if [[ "$tier" == public ]]; then
      aws ec2 modify-subnet-attribute --subnet-id "$subnet" --map-public-ip-on-launch
      # Track the first public subnet for NAT gateway placement
      [[ -n "$FIRST_PUBLIC_SUBNET" ]] || FIRST_PUBLIC_SUBNET="$subnet"
    else
      aws ec2 modify-subnet-attribute --subnet-id "$subnet" --no-map-public-ip-on-launch
    fi

    assoc=$(aws ec2 associate-route-table \
      --route-table-id "$rt" \
      --subnet-id "$subnet" \
      --query AssociationId --output text)
    save "${tier^^}_${az^^}_ASSOC_ID" "$assoc"
    echo "$tier-$az: $cidr ($subnet)"
  done

  # After all public subnets are ready, create the NAT gateway in public-a and wait.
  # Private tiers need NAT_GW_ID set before their route tables are configured,
  # which happens at the top of the next loop iteration — this wait ensures it.
  if [[ "$tier" == public ]]; then
    echo "Creating NAT gateway in public-a ($FIRST_PUBLIC_SUBNET)..."
    NAT_GW_ID=$(aws ec2 create-nat-gateway \
      --subnet-id "$FIRST_PUBLIC_SUBNET" \
      --allocation-id "$EIP_ALLOC_ID" \
      --tag-specifications "ResourceType=natgateway,Tags=[{Key=Name,Value=$PROJECT-nat}]" \
      --query NatGateway.NatGatewayId --output text)
    save NAT_GW_ID "$NAT_GW_ID"
    echo "Waiting for NAT gateway $NAT_GW_ID to become available (1-2 min)..."
    aws ec2 wait nat-gateway-available --nat-gateway-ids "$NAT_GW_ID"
    echo "NAT gateway available."
  fi
done

aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'Subnets[].{Name:Tags[?Key==`Name`]|[0].Value,CIDR:CidrBlock,AZ:AvailabilityZone,PublicIP:MapPublicIpOnLaunch}' \
  --output table

echo "Created VPC $VPC_ID with NAT gateway $NAT_GW_ID. Resource IDs saved in $STATE_FILE."
echo "NOTE: NAT gateway incurs ongoing charges. Run delete_balerica_vpc.sh when done."
