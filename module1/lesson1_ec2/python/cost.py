#!/usr/bin/env python3
"""
=========================================================
                    BALERICA AI
                Cost Analyzer Agent v1.0
=========================================================

SEIR Foundations

Purpose:
Estimate EC2 cost efficiency by comparing AWS cost data
against EC2 utilization data.

This is a FinOps teaching tool.

It does NOT replace AWS Billing, Cost Explorer, Compute
Optimizer, or a formal FinOps process.

=========================================================
"""

import json
import os
from datetime import datetime, timedelta, timezone

import boto3
from dotenv import load_dotenv

from banner import show_banner, show_footer
from bedrock import invoke_bedrock
from telemetry import get_instance_id, get_instance_type, get_availability_zone


AGENT = True
NAME = "Cost Analyzer"
DESCRIPTION = "Estimate EC2 cost efficiency using Cost Explorer and CloudWatch."
VERSION = "1.0"
REQUIRES_TELEMETRY = True


load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DAYS_BACK = int(os.getenv("COST_LOOKBACK_DAYS", "30"))


# ---------------------------------------------------------
# Chewbacca says:
#
# "Rrrrrrrgh..."
#
# Translation:
#
# Cost without utilization is just a bill.
# Cost with utilization becomes engineering evidence.
# ---------------------------------------------------------


def get_date_range(days_back=DAYS_BACK):
    """
    Return start and end dates for Cost Explorer.

    Cost Explorer expects dates in YYYY-MM-DD format.
    End date is exclusive.
    """

    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=days_back)

    return str(start), str(end)


def get_ec2_service_cost(start_date, end_date):
    """
    Retrieve total EC2 service cost for the account over the date range.

    This is account-level EC2 cost, not per-instance cost.
    """

    client = boto3.client("ce", region_name="us-east-1")

    response = client.get_cost_and_usage(
        TimePeriod={
            "Start": start_date,
            "End": end_date
        },
        Granularity="MONTHLY",
        Metrics=[
            "UnblendedCost"
        ],
        Filter={
            "Dimensions": {
                "Key": "SERVICE",
                "Values": [
                    "Amazon Elastic Compute Cloud - Compute"
                ]
            }
        }
    )

    total = 0.0
    unit = "USD"

    for result in response.get("ResultsByTime", []):
        amount = result["Total"]["UnblendedCost"]["Amount"]
        unit = result["Total"]["UnblendedCost"]["Unit"]
        total += float(amount)

    return total, unit


def get_average_cpu_utilization(instance_id, days_back=DAYS_BACK):
    """
    Get average EC2 CPU utilization from CloudWatch.

    Uses the AWS/EC2 CPUUtilization metric.
    """

    client = boto3.client("cloudwatch", region_name=AWS_REGION)

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=days_back)

    response = client.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": instance_id
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=86400,
        Statistics=[
            "Average"
        ],
        Unit="Percent"
    )

    datapoints = response.get("Datapoints", [])

    if not datapoints:
        return 0.0

    total = sum(point["Average"] for point in datapoints)

    return total / len(datapoints)


def calculate_efficiency(monthly_cost, average_cpu):
    """
    Estimate utilization-adjusted cost.

    Example:
    Monthly cost = 100
    Average CPU = 20%

    Utilization-adjusted cost = 20
    Waste signal = 80
    """

    utilization_ratio = average_cpu / 100

    utilization_adjusted_cost = monthly_cost * utilization_ratio

    waste_signal = monthly_cost - utilization_adjusted_cost

    return {
        "Utilization Ratio": utilization_ratio,
        "Utilization Adjusted Cost": utilization_adjusted_cost,
        "Waste Signal": waste_signal
    }


def build_prompt(report):
    """
    Build a FinOps explanation prompt.
    """

    return f"""
You are Balerica AI acting as a FinOps teaching assistant.

Analyze the following EC2 cost and utilization report.

Explain:
1. What the billed cost means
2. What the utilization-adjusted cost means
3. Why this is only a signal, not a final billing conclusion
4. What the student should investigate next
5. Practical recommendations
6. One FinOps lesson

Rules:
- Do not invent facts.
- Be clear that Cost Explorer cost may be account-level or service-level.
- Be clear that CPU utilization alone is not enough for a final rightsizing decision.
- Keep the explanation practical for a junior cloud engineer.

Report:

{json.dumps(report, indent=4)}
"""


def run(question=None):
    """
    Agent entry point used by ask.py.
    """

    show_banner(
        agent_name=NAME,
        version=VERSION
    )

    print("Collecting cost and utilization data...\n")

    try:
        instance_id = get_instance_id()
        instance_type = get_instance_type()
        availability_zone = get_availability_zone()

        start_date, end_date = get_date_range()

        print(f"[✓] Instance ID: {instance_id}")
        print(f"[✓] Instance Type: {instance_type}")
        print(f"[✓] Availability Zone: {availability_zone}")
        print(f"[✓] Cost Window: {start_date} to {end_date}")

        monthly_cost, unit = get_ec2_service_cost(
            start_date,
            end_date
        )

        print(f"[✓] EC2 Service Cost Retrieved: {unit} {monthly_cost:.2f}")

        average_cpu = get_average_cpu_utilization(
            instance_id
        )

        print(f"[✓] Average CPU Utilization: {average_cpu:.2f}%")

        efficiency = calculate_efficiency(
            monthly_cost,
            average_cpu
        )

        report = {
            "Instance ID": instance_id,
            "Instance Type": instance_type,
            "Availability Zone": availability_zone,
            "Cost Window Start": start_date,
            "Cost Window End": end_date,
            "EC2 Service Cost": round(monthly_cost, 2),
            "Currency": unit,
            "Average CPU Utilization Percent": round(average_cpu, 2),
            "Utilization Adjusted Cost": round(
                efficiency["Utilization Adjusted Cost"],
                2
            ),
            "Waste Signal": round(
                efficiency["Waste Signal"],
                2
            ),
            "Important Limitation": (
                "This uses EC2 service-level cost and this instance's CPU "
                "utilization. It is a teaching signal, not exact per-instance "
                "billing attribution."
            )
        }

        print("\nGenerating FinOps analysis with Amazon Bedrock...\n")

        prompt = build_prompt(report)

        response = invoke_bedrock(prompt)

        print("=" * 60)
        print("Balerica AI Cost Report")
        print("=" * 60)
        print()
        print(response)
        print()
        print("=" * 60)

        show_footer()

    except Exception as ex:
        print()
        print("Unable to complete cost analysis.\n")
        print("Things to check:\n")
        print("✓ IAM Role has Cost Explorer permissions")
        print("✓ IAM Role has CloudWatch read permissions")
        print("✓ Cost Explorer is enabled")
        print("✓ EC2 instance has CloudWatch CPU metrics")
        print("✓ AWS_REGION is correct in .env")
        print()
        print("Technical Details:\n")
        print(ex)


if __name__ == "__main__":
    run()
