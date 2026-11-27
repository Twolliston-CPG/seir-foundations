# Module 1 — AWS Infrastructure Runbook

---

## Lab 0 — First EC2 Deployment

### Lab 0: EC2 Basics

#### Step 1 — Get the startup script

If you haven't cloned the repo yet:

```bash
sudo dnf install -y git
git clone https://github.com/BalericaAI/SEIR-Foundations.git
cd SEIR-Foundations/module1/lab0_basics
```

If already cloned, navigate to your existing copy. The script you need is `seir_ec2_userdata.sh`. Open it and copy its **entire contents** — not the GitHub URL, the actual script text.

#### Step 2 — Create the EC2 launch template

1. Sign in to the AWS Console and confirm your Region.
2. Go to **EC2 → Launch Templates → Create launch template**.
3. Name it `seir-foundations-lab0`.
4. AMI: **Amazon Linux 2023**
5. Instance type: a Free Tier-eligible or credit-covered small instance for your account.
6. Key pair: select an existing one or create a new one.
7. Security group: allow **SSH (TCP 22)** inbound.
8. Expand **Advanced details → User data**. Paste the full contents of `seir_ec2_userdata.sh` (starts with `#!/bin/bash`).
9. Save the template.

> Keep this template — it is reused throughout Module 1. It has no compute charge on its own.

#### Step 3 — Launch an instance

1. Go to **EC2 → Launch Templates**, select `seir-foundations-lab0`.
2. **Actions → Launch instance from template**.
3. Launch **one** instance.
4. Wait in **EC2 → Instances** until status is **Running** and status checks pass.
5. Record the **public IPv4 address**.

#### Step 4 — Connect

1. Select the running instance and click **Connect**.
2. Use either:
   - **EC2 Instance Connect** (browser-based), or
   - **SSH client** — follow the exact instructions shown by AWS on the Connect screen.

SSH example (use values from the Connect screen, not these placeholders):

```bash
chmod 400 ~/Downloads/YOUR-KEY.pem
ssh -i ~/Downloads/YOUR-KEY.pem ec2-user@YOUR-PUBLIC-DNS
```

Default user for Amazon Linux 2023: `ec2-user`.

#### Step 5 — Inspect the dashboard

After login the SEIR dashboard should appear automatically. If it doesn't:

```bash
seir-dashboard
```

Identify these values:

| Item | What it tells you |
|---|---|
| Hostname / Instance ID | Which EC2 machine you're on |
| Instance type / AZ | Compute type and location |
| CPU usage / vCPUs | Processor activity and logical CPU count |
| Memory | RAM in use and total |
| Disk usage | Root filesystem space consumed |
| Uptime | How long Linux has been running |
| Load average | Workload over 1, 5, 15 minutes |

#### Step 6 — Terminate the instance (keep the template)

1. **EC2 → Instances** → select the instance.
2. **Instance state → Terminate instance** → confirm.
3. Verify it transitions to **Terminated**.
4. Check **EC2 → Volumes** and **Elastic IPs** — remove any leftover billable resources you created.
5. Confirm `seir-foundations-lab0` still exists in **EC2 → Launch Templates**.

#### Checklist

- [ ] Repo cloned and `seir_ec2_userdata.sh` contents copied
- [ ] Launch template `seir-foundations-lab0` created with Amazon Linux 2023, correct instance type, key pair, and security group
- [ ] User Data pasted as full script text (starting with `#!/bin/bash`)
- [ ] Instance launched from template and reached **Running** with status checks passed
- [ ] Public IPv4 address recorded
- [ ] Connected via EC2 Instance Connect or SSH
- [ ] SEIR dashboard displayed (`seir-dashboard` runs without error)
- [ ] Instance terminated and confirmed **Terminated**
- [ ] No leftover EBS volumes or Elastic IPs
- [ ] Launch template still present in **EC2 → Launch Templates**

#### Troubleshooting

| Symptom | Check |
|---|---|
| Dashboard doesn't appear | Run `seir-dashboard`; verify User Data was pasted as script text |
| `seir-dashboard: command not found` | Full script wasn't in the template before launch; use the corrected template for a new instance |
| Can't SSH | Instance running, correct key, username `ec2-user`, security group TCP 22 open, correct public IP |
| No public IP | Check subnet public IP assignment; verify connection method |
| User Data didn't run | `sudo tail -n 100 /var/log/cloud-init-output.log` on the instance |

---

## Lesson 1 — Balerica Legacy Bank on EC2

### Prerequisites — SSH into the instance

**macOS / Linux:**
```bash
chmod 400 your-key.pem
ssh -i your-key.pem ec2-user@YOUR-EC2-IP
```

**Windows (PowerShell):**
```powershell
ssh -i .\your-key.pem ec2-user@YOUR-EC2-IP
```

This is **Window 1** for the rest of the lesson.

---

### Step 0 — Confirm you are on the server

```bash
whoami
```
Expected: `ec2-user`

```bash
pwd
```
Expected: `/home/ec2-user`

---

### Step 1 — Set timezone, install git, clone the repo

```bash
sudo timedatectl set-timezone America/New_York
```

```bash
sudo dnf install -y git
```
Expected last line: `Complete!` (or `Nothing to do` — both fine)

```bash
git clone https://github.com/BalericaAI/SEIR-Foundations.git
```

```bash
ls SEIR-Foundations
```
Expected: `README.md  module1  module2  module3  module4  playbook.md  podcasts.md  python`

---

### Step 2 — Run the installer

```bash
bash SEIR-Foundations/module1/lesson1_ec2/API/install/install.sh
```

Takes a few minutes. Expected output:

```
======================================
 BALERICA LEGACY BANK INSTALLER
======================================
[1/9] Updating packages...
[2/9] Installing dependencies...
[3/9] Creating directories...
[4/9] Copying Balerica Bank sources...
[5/9] Creating Python virtual environment...
[6/9] Installing Python packages...
[7/9] Creating database...
[8/9] Compiling COBOL programs...
[9/9] Exporting the ledger for the COBOL core...
  exported 3 account(s) to data/accounts.dat

Installation complete.
```

`[8/9]` with no errors after it and `Installation complete.` are what matter. Safe to re-run if it fails.

---

### Step 3 — Run the COBOL core

```bash
cd /opt/balerica-bank
ls
```
Expected: `agents  app  cobol  data  logs  swift  venv`

**Look up an account:**
```bash
./cobol/bin/account_lookup 100001
echo $?
```
Expected:
```
ACCOUNT=100001
NAME=Alice Johnson
STATUS=ACTIVE
BALANCE=5000.00
CURRENCY=USD
0
```

**Look up a missing account:**
```bash
./cobol/bin/account_lookup 999999
echo $?
```
Expected:
```
ERROR=ACCOUNT NOT FOUND
ACCOUNT=999999
4
```

Return code reference:

| Code | Meaning |
|------|---------|
| 0 | success — account found / payment posted |
| 4 | warning — account not found |
| 8 | business rejection — not active, zero amount, insufficient funds |
| 12 | environment failure — missing file, malformed arguments |

**Post a payment:**
```bash
./cobol/bin/payment_post TXN0001 100001 125.50 USD INV-1001
```
Expected:
```
TXN=TXN0001
ACCOUNT=100001
AMOUNT=125.50
CURRENCY=USD
STATUS=POSTED
REASON=APPROVED
```

**View the payment journal:**
```bash
cat data/payments.dat
```
Expected: `TXN0001             100001000000012550USDPOSTED  INV-1001`

---

### Optional — Set up AWS Bedrock access (required for Steps 4 and 8 Bedrock variants)

Skip this section if you do not need the Bedrock-powered `/ask` endpoint. Complete it **before Step 4** if you do — the instance profile must be attached before the server starts.

**What you are building:**

| AWS object | Name | Purpose |
|---|---|---|
| IAM Role | `balerica-ec2-bedrock-profile` | Holds the Bedrock permissions |
| Inline policy | `bedrock-Invoke` | Grants `InvokeModel` on Anthropic models |
| Instance profile | `balerica-ec2-bedrock-profile` | The attachment point EC2 uses to assume the role |

---

#### Part 1 — Get your AWS account ID

You need this for the policy resource ARN. Run:

```bash
aws sts get-caller-identity --query Account --output text
```

Record the 12-digit number. It is also visible in the top-right of the AWS Console.

---

#### Part 2 — Enable model access in the Bedrock console

1. Sign in to the AWS Console and switch to **us-east-1**.
2. Go to **Amazon Bedrock → Model access** (left nav).
3. Click **Modify model access**.
4. Check **Claude Sonnet 4** (or whichever Claude model you plan to use).
5. Click **Next → Submit**.
6. Refresh until the **Access status** column shows **Access granted** (usually 1–2 minutes).

> `us.anthropic.claude-sonnet-4-6` is a cross-region inference profile that spans US regions. Enabling access in us-east-1 covers it.

---

#### Part 3 — Create the IAM role

> **Note on naming:** The AWS Console automatically creates an instance profile with the **same name** as the role. To keep everything console-only, name the role **`balerica-ec2-bedrock-profile`** — the console will create a matching instance profile of the same name, which is what you select in EC2.

1. Go to **IAM → Roles → Create role**.
2. **Trusted entity type:** AWS service → **EC2** → **Next**.
3. Skip the permissions page — click **Next** without selecting anything.
4. Role name: **`balerica-ec2-bedrock-profile`**
5. Click **Create role**.

The console automatically creates an instance profile named **`balerica-ec2-bedrock-profile`** linked to this role.

---

#### Part 4 — Attach the inline policy to the role

1. In **IAM → Roles**, open **`balerica-ec2-bedrock-profile`**.
2. Click **Add permissions → Create inline policy**.
3. Click the **JSON** tab. Replace all existing content with the policy below, substituting your 12-digit account ID from Part 1:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/anthropic.*",
        "arn:aws:bedrock:*:YOUR_ACCOUNT_ID:inference-profile/*"
      ]
    }
  ]
}
```

4. Click **Next**.
5. Policy name: **`bedrock-Invoke`**
6. Click **Create policy**.

**Verify:** On the role's **Permissions** tab, `bedrock-Invoke` appears with type **Customer inline**.

---

#### Part 5 — Attach the instance profile to EC2

**Option A — Attach to a running instance** (no restart needed):

1. Go to **EC2 → Instances** → select your running instance.
2. **Actions → Security → Modify IAM role**.
3. In the dropdown, select **`balerica-ec2-bedrock-profile`**.
4. Click **Update IAM role**.

**Option B — Bake into the launch template** (recommended — every new instance gets it automatically):

1. **EC2 → Launch Templates** → select `seir-foundations-lab0` → **Actions → Modify template (Create new version)**.
2. Scroll to **Advanced details → IAM instance profile**.
3. Select **`balerica-ec2-bedrock-profile`** from the dropdown.
4. Click **Create template version**.
5. **Actions → Set default version** → select the new version number → **Set as default version**.

---

#### Part 6 — Verify the profile is active on the instance

**Console check:** EC2 → Instances → select your instance → **Security** tab → **IAM Role** must show `balerica-ec2-bedrock-profile`. If it says "none", repeat Part 5 Option A.

**On-instance check** — SSH into the instance and run:

```bash
aws sts get-caller-identity
```

Expected — `Arn` must contain `assumed-role/balerica-ec2-bedrock-profile`:

```json
{
    "UserId": "AROAEXAMPLE...:i-0abc...",
    "Account": "YOUR_ACCOUNT_ID",
    "Arn": "arn:aws:sts::YOUR_ACCOUNT_ID:assumed-role/balerica-ec2-bedrock-profile/i-0abc..."
}
```

If `Arn` still shows `arn:aws:iam::...user/...`, wait 30 seconds and retry.

**Success check:** `Arn` on the instance contains `assumed-role/balerica-ec2-bedrock-profile`.

---

### Step 4 — Start the web API (Window 1)

```bash
cd /opt/balerica-bank
source venv/bin/activate
```
Prompt should now show `(venv)`.

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Expected:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

> Window 1 is now occupied by the running server. Leave it alone.

**Optional — with AWS Bedrock** (requires the IAM role from the Bedrock setup section above):
```bash
BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-6 AWS_REGION=us-east-1 uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

### Step 5 — Open a second terminal (Window 2)

Open a new terminal and SSH into the same instance:

```bash
ssh -i your-key.pem ec2-user@YOUR-EC2-IP
```

**Check the API is responding:**
```bash
curl http://127.0.0.1:8000/status
```
Expected: `{"platform":"Balerica Legacy Bank","environment":"Amazon EC2","api":"online","core_banking":"GnuCOBOL"}`

**Run the platform diagnostic:**
```bash
curl http://127.0.0.1:8000/chewbacca
```
Expected: a Wookiee response — platform is healthy.

---

### Step 6 — Send SWIFT traffic (Window 2)

```bash
cd /opt/balerica-bank
python3 swift/traffic_generator.py --count 10
```

Expected:
```
[3/3] Traffic report
  Sent     : 10
  POSTED   : 7
  REJECTED : 3
  FAILED   : 0

  CONNECTIVITY CONFIRMED.
  Modern edge and COBOL core are talking.
```

`FAILED` must be `0`. `REJECTED` is expected — the core intentionally rejects bad payments.

**Optional — view raw MT103 messages:**
```bash
python3 swift/traffic_generator.py --count 3 --show-mt103
```

---

### Step 7 — Explore the API in a browser

Open in a browser (replace with your instance's public IP):

```
http://YOUR-EC2-IP:8000/docs
```

1. Click **`GET /accounts/{account_id}`**
2. Click **Try it out**
3. Enter `100001` → **Execute**

**If the page never loads**, port 8000 is blocked by the security group. Fix it in the AWS Console:

EC2 → instance → **Security** tab → Security group → **Edit inbound rules** → **Add rule**:

| Type | Port | Source |
|------|------|--------|
| Custom TCP | 8000 | My IP |

Save rules, then reload the `/docs` page.

---

### Step 8 — Query the Balerica AI helper (Window 2)

**Standard (offline fallback built in):**
```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{"question": "What does return code 8 mean?"}'
```

**With AWS Bedrock:**
```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{"question": "What does return code 8 mean?", "model_id": "us.anthropic.claude-sonnet-4-6", "region": "us-east-1"}'
```

If the response shows `"source": "offline-knowledge-base"`, all three must be true for Bedrock to answer:
1. IAM role attached to the instance with Bedrock permissions (see `iam/PERMISSIONS.md`)
2. `AWS_REGION` matches the region where you enabled model access
3. `BEDROCK_MODEL_ID` is a valid inference profile ID (starts with `us.`)

---

### Step 9 — Stop the server

In Window 1, press **`Ctrl+C`**.

Data persists in `data/bank.db` and the journal files. Repeat Step 4 to reopen the bank next time.

> Stop (not terminate) the EC2 instance from the AWS Console when done for the day to avoid charges.

---

### Checklist

- [ ] SSH'd into EC2 instance as `ec2-user`
- [ ] `whoami` returns `ec2-user`, `pwd` returns `/home/ec2-user`
- [ ] Timezone set, git installed, `SEIR-Foundations` cloned
- [ ] Installer completed with `Installation complete.`
- [ ] `account_lookup 100001` returns Alice Johnson (rc=0)
- [ ] `account_lookup 999999` returns ACCOUNT NOT FOUND (rc=4)
- [ ] Payment TXN0001 posted and visible in `data/payments.dat`
- [ ] `(venv)` active, uvicorn running on port 8000 (Window 1)
- [ ] Window 2 open, `/status` returns expected JSON
- [ ] `/chewbacca` returns Wookiee response
- [ ] SWIFT traffic sent with `FAILED: 0` and `CONNECTIVITY CONFIRMED`
- [ ] `/docs` loads in browser and account 100001 lookup works
- [ ] `/ask` returns a response
- [ ] Server stopped with `Ctrl+C`

### Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Permission denied (publickey)` | Wrong key or user — use `ec2-user@` and your `.pem`; run `chmod 400 your-key.pem` on macOS |
| `git: command not found` | Run `sudo dnf install -y git` |
| Installer stops with error | Re-run it — safe to re-run |
| `cobc: command not found` | Re-run the installer |
| `FILE-STATUS=35` / rc=12 | Wrong directory — `cd /opt/balerica-bank` first |
| `(venv)` missing from prompt | Run `source venv/bin/activate` again (per-terminal) |
| `command not found: uvicorn` | Activate the venv first |
| Traffic generator prints `UNREACHABLE` | Server not running in Window 1 — redo Step 4 |
| `/docs` never loads | Open port 8000 in the Security Group (Step 7) |
| Every payment REJECTED | Read the `REASON=` line — the core explains itself |
| `/ask` returns `offline-knowledge-base` | Check IAM role, `AWS_REGION`, and `BEDROCK_MODEL_ID` — all three must be correct |

---

## Lesson 2 — Balerica AI Slack Integration

### Step 1 — Install Slack on your local machine

**macOS:**
```bash
brew install --cask slack
open -a Slack
```

**Windows (PowerShell as Administrator):**
```powershell
choco install slack -y
```
Launch Slack from the Start menu.

---

### Step 2 — Create your Slack workspace and alert channel

1. Sign in or create an account at https://slack.com/
2. Create a new workspace (suggested name: `SEIR-Foundations-<your-alias>`)
3. Inside the workspace, create a channel named **`#balerica-alerts`**

---

### Step 3 — Create a Slack app and configure the Incoming Webhook

1. Go to https://api.slack.com/apps
2. **Create New App → From scratch**
3. App name: `Balerica AI` — select your own workspace → **Create App**
4. In the app settings, click **Incoming Webhooks**
5. Toggle **Activate Incoming Webhooks** to **On**
6. Click **Add New Webhook to Workspace**
7. Select `#balerica-alerts` → **Allow**
8. Return to **Incoming Webhooks** and copy the webhook URL

> The webhook URL starts with `https://hooks.slack.com/services/`. Treat it as a password — never paste it into GitHub, chat, or screenshots.

---

### Step 4 — Get the Lesson 2 files onto EC2

SSH into your EC2 instance. If the course repo is already on the instance:

```bash
cd ~/SEIR-Foundations
git pull
```

If this is a fresh instance:

```bash
sudo dnf install -y git
git clone https://github.com/BalericaAI/SEIR-Foundations.git
```

Confirm the files are present:

```bash
ls ~/SEIR-Foundations/module1/lesson2_slack/
```
Expected: `slack.py`, `slack.env.example`, `runbook.md` among the output.

---

### Step 5 — Copy `slack.py` into the bank directory

```bash
cp ~/SEIR-Foundations/module1/lesson2_slack/slack.py /opt/balerica-bank/
cd /opt/balerica-bank
ls slack.py
```
Expected: `slack.py`

---

### Step 6 — Set your workspace URL in `slack.py`

```bash
nano slack.py
```

Find this line near the top:

```python
SLACK_WORKSPACE_URL = "https://chewbacca.slack.com"
```

Replace `chewbacca` with your own workspace name. Save and exit: **`Ctrl+O` → `Enter` → `Ctrl+X`**

> This is not optional — `slack.py` refuses to run while the placeholder URL is in place.

---

### Step 7 — Create `.env` with your webhook

```bash
cp -n ~/SEIR-Foundations/module1/lesson2_slack/slack.env.example /opt/balerica-bank/.env
chmod 600 .env
nano .env
```

Set these values (replace the webhook with your real one):

```dotenv
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/REAL/WEBHOOK
SLACK_ALERTS_ENABLED=true
SLACK_ALERT_SEVERITY=ERROR
SLACK_ALERT_CHANNEL=balerica-alerts
```

Save and exit: **`Ctrl+O` → `Enter` → `Ctrl+X`**

Add `.env` to `.gitignore`:

```bash
grep -qxF '.env' .gitignore 2>/dev/null || echo '.env' >> .gitignore
```

---

### Step 8 — Activate the venv and install dependencies

```bash
cd /opt/balerica-bank
source venv/bin/activate
python -m pip install requests python-dotenv
```

Verify:

```bash
python -c "import requests; import dotenv; print('Dependencies OK')"
```
Expected: `Dependencies OK`

---

### Step 9 — Run the test

```bash
python slack.py --test
```

Expected terminal output: `SUCCESS: Chewbacca approves!`

Open Slack on your computer and confirm the alert appears in `#balerica-alerts`:

```
BALERICA AI ALERT
Severity: ERROR
Agent: slack.py
Incident: TEST-001
Message: TEST: Slack is connected. RRRRAAAWWWRRR!
```

A terminal success without the message visible in Slack is not complete — verify both.

---

### Using `send_alert()` from other agents

```python
from slack import send_alert

send_alert(
    agent="health.py",
    severity="ERROR",
    message="Simulated disk threshold exceeded",
    incident_id="LAB-001"
)
```

---

### Checklist

- [ ] Slack installed on local machine via `brew` or `choco`
- [ ] Slack workspace created with `#balerica-alerts` channel
- [ ] `Balerica AI` Slack app created with Incoming Webhooks enabled
- [ ] Webhook authorized for `#balerica-alerts` and URL copied
- [ ] Webhook URL stored securely (password manager or private notes) — never in GitHub
- [ ] Course repo pulled/cloned on EC2
- [ ] `slack.py` copied to `/opt/balerica-bank/`
- [ ] `SLACK_WORKSPACE_URL` updated in `slack.py` to your own workspace
- [ ] `.env` created with real webhook, `chmod 600`, and added to `.gitignore`
- [ ] `Dependencies OK` confirmed
- [ ] `python slack.py --test` returns `SUCCESS: Chewbacca approves!`
- [ ] Test alert visible in `#balerica-alerts` in Slack

### Troubleshooting

| Symptom | Fix |
|---------|-----|
| `FAILED: CHOMP!!! Chewbacca bit you` | Step 6 — placeholder URL still in `slack.py` |
| `FAILED: Configure SLACK_WEBHOOK_URL in .env` | Step 7 — `.env` missing, wrong directory, or placeholder webhook |
| `ModuleNotFoundError: No module named 'requests'` | Step 8 — venv not active or packages not installed |
| `No such file or directory: slack.py` | Step 5 — not in `/opt/balerica-bank`; run `pwd` |
| `SKIPPED: Check alert settings in .env` | Set `SLACK_ALERTS_ENABLED=true` and `SLACK_ALERT_SEVERITY=ERROR` |
| HTTP 403 / 404 | Webhook revoked or wrong URL — regenerate in Slack app settings |
| Timeout / network error | EC2 needs outbound HTTPS (TCP 443) — check security group egress |
| Terminal success but no Slack message | Wrong workspace or channel open — the webhook controls delivery, not the workspace URL in `slack.py` |

---

## Lesson 3 — Jira + Slack Incident Integration

### Step 1 — Create a Jira Cloud Free site (browser)

1. Go to https://www.atlassian.com/software/jira/free → **Get it free**
2. Create an Atlassian account or sign in, verify email
3. Choose **Jira** on the **Free** plan
4. Create your site — suggested name: `yourname-seir` → your URL will be `https://yourname-seir.atlassian.net`

---

### Step 2 — Create the Balerica AI project (browser)

1. In Jira: **Projects → Create project**
2. Template: **Kanban** (team-managed)
3. Name: `Balerica AI Incident Management`
4. Key: set to `BAI` if available — if Jira assigns a different key, record the actual one
5. Create a manual test work item: type **Task**, summary `TEST — EC2 application error`
6. Record the issue key (e.g. `BAI-1`) — confirm the ticket appears on the board

---

### Step 3 — Create a plain Atlassian API token (browser)

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click **Create API token** — **NOT** "Create API token with scopes"
3. Name: `balerica-seir-ec2`, set an expiration date, click **Create**
4. **Copy the token immediately** — it is shown only once
5. Store it in a password manager or private note — never in GitHub, chat, or screenshots

> A scoped token fails with HTTP 401 against `*.atlassian.net`. Use the plain token only.

---

### Step 4 — Get the Lesson 3 files onto EC2

SSH into your EC2 instance and update the repo:

```bash
cd ~/SEIR-Foundations
git pull
```

Confirm the files are present:

```bash
ls ~/SEIR-Foundations/module1/lesson3_Jira/
```
Expected: `jira.py`, `incident.py`, `jira_runbook.md` among the output.

---

### Step 5 — Copy `jira.py` and `incident.py` to the bank

```bash
cp ~/SEIR-Foundations/module1/lesson3_Jira/jira.py /opt/balerica-bank/
cp ~/SEIR-Foundations/module1/lesson3_Jira/incident.py /opt/balerica-bank/
cd /opt/balerica-bank
ls slack.py jira.py incident.py
```
All three files must be present before continuing.

---

### Step 6 — Add Jira settings to the existing `.env`

> **Do NOT overwrite `.env`** — that erases your Slack webhook. Open and append.

```bash
cd /opt/balerica-bank
nano .env
```

Add these lines at the bottom (keep all existing Slack lines untouched):

```dotenv
# JIRA — Lesson 3
JIRA_SITE_URL=https://YOUR-SITE.atlassian.net
JIRA_EMAIL=your-atlassian-email@example.com
JIRA_API_TOKEN=paste-your-plain-token-here
JIRA_PROJECT_KEY=BAI
JIRA_ISSUE_TYPE=Task
JIRA_ENABLED=true
INCIDENT_STATE_DB=data/incident_state.db
```

Save and exit: **`Ctrl+O` → `Enter` → `Ctrl+X`**

Verify both sections survived:

```bash
chmod 600 .env
grep -c '^SLACK_' .env    # expect 2 or more
grep -c '^JIRA_' .env     # expect 6
```

If the Slack count is 0, restore your Slack settings before continuing.

---

### Step 7 — Activate the venv and install dependencies

```bash
cd /opt/balerica-bank
source venv/bin/activate
python3 -m pip install requests python-dotenv
mkdir -p data
```

---

### Step 8 — Verify Jira connectivity

```bash
python3 jira.py --verify
```

Expected:
```
Connected to Jira project: BAI (Balerica AI Incident Management)
```

Do not continue until `--verify` succeeds.

---

### Step 9 — Create a test ticket

```bash
python3 jira.py --test
```

Expected:
```
Connected to Jira project: BAI (Balerica AI Incident Management)
Test issue created: https://YOUR-SITE.atlassian.net/browse/BAI-2
```

Open the printed URL in your browser and confirm the ticket exists. If the ticket is not on the board, check **Backlog** in the left navigation — items commonly land there in team-managed projects.

---

### Step 10 — Run the full incident pipeline

Dry run first (calls no external services):

```bash
python3 incident.py --dry-run
```

Then run the real test:

```bash
python3 incident.py --test
```

Expected output:
```json
{
  "incident_id": "SEIR-TEST-...",
  "jira_key": "BAI-3",
  "jira_url": "https://YOUR-SITE.atlassian.net/browse/BAI-3",
  "jira_created": true,
  "slack_status": "sent"
}
```

Verify all three:
1. `jira_created: true` and `slack_status: sent` in the terminal
2. The ticket is on your Jira board (check Backlog if needed)
3. The Slack alert is in `#balerica-alerts` with a clickable link to the same ticket

---

### Step 11 — Test deduplication

Create a small script to call `report_incident` directly:

```bash
nano my_first_incident.py
```

```python
from incident import report_incident

result = report_incident(
    agent='health.py',
    severity='CRITICAL',
    message='Synthetic test: application process is unavailable',
    incident_id='EC2-PROCESS-DOWN-001',
    evidence='Health check returned unhealthy',
    recommendation='Inspect process status and service logs'
)
print(result)
```

Save and exit: **`Ctrl+O` → `Enter` → `Ctrl+X`**

**Run once:**
```bash
python3 my_first_incident.py
```
Expected: `jira_created: True, slack_status: 'sent'`

**Run again:**
```bash
python3 my_first_incident.py
```
Expected: `jira_created: False, slack_status: 'already_sent'` — no new ticket.

This confirms the deduplication logic is working. The same incident ID reuses the existing Jira ticket instead of creating a duplicate.

---

### Checklist

- [ ] Jira Cloud Free site created (`*.atlassian.net`)
- [ ] `Balerica AI Incident Management` project created, key confirmed (e.g. `BAI`)
- [ ] Manual test work item created and visible on the board
- [ ] Plain (unscoped) API token created, expiry date noted, stored privately
- [ ] `jira.py` and `incident.py` copied to `/opt/balerica-bank/`
- [ ] Jira settings appended to `.env` without overwriting Slack settings
- [ ] `grep -c '^SLACK_' .env` ≥ 2 and `grep -c '^JIRA_' .env` = 6
- [ ] `chmod 600 .env` applied
- [ ] `python3 jira.py --verify` reports correct project key and name
- [ ] `python3 jira.py --test` printed a ticket URL; ticket opens in browser
- [ ] Ticket visible on Jira board (or found in Backlog)
- [ ] `python3 incident.py --dry-run` completes without calling external services
- [ ] `python3 incident.py --test` shows `jira_created: true` and `slack_status: sent`
- [ ] Jira ticket visible on board; Slack alert in `#balerica-alerts` with correct link
- [ ] Deduplication confirmed — second run produces `jira_created: False`

### Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Jira HTTP 401` immediately after creating token | Used "Create API token with scopes" — create a plain token instead |
| `Jira HTTP 401` after weeks of working | Token expired — create a new one and update `.env` |
| `Jira HTTP 401` with fresh plain token | `JIRA_EMAIL` wrong, or token copied with extra spaces/quotes |
| `Jira HTTP 403` | Account lacks create-issue permission on that project |
| `Jira HTTP 404` | Wrong `JIRA_SITE_URL` or `JIRA_PROJECT_KEY` — run `--verify` |
| `Jira HTTP 400` on `--test` | `JIRA_ISSUE_TYPE` doesn't exist in the project — check project settings |
| `--test` succeeded but no card on board | Open the printed URL first; then check Backlog, filters, project key, and signed-in site |
| Slack worked before Lesson 3, not now | Jira setup overwrote `.env` and removed `SLACK_WEBHOOK_URL` — restore Slack lines |
| `ModuleNotFoundError` | Activate venv and run `pip install requests python-dotenv` |
| `No module named 'jira'` or `'slack'` | `jira.py` or `slack.py` missing from `/opt/balerica-bank/` — copy them |
| EC2 can't reach Jira | Check outbound HTTPS (TCP 443) and DNS |
| `jira_created: True` but `slack_status` not `sent` | Jira half worked — troubleshoot Slack independently using `python3 slack.py --test` |

---

## Lesson 4 — Balerica Bank VPC

### Network design

One VPC (`10.20.0.0/16`) in us-east-1, one Internet Gateway, three route tables, and nine subnets.

| Tier | us-east-1a | us-east-1b | us-east-1c | Internet route |
|---|---|---|---|---|
| Public | 10.20.1.0/24 | 10.20.2.0/24 | 10.20.3.0/24 | Yes (via IGW) |
| Private 1 | 10.20.11.0/24 | 10.20.12.0/24 | 10.20.13.0/24 | No |
| Private 2 | 10.20.21.0/24 | 10.20.22.0/24 | 10.20.23.0/24 | No |

The script writes `balerica-network.env` in the folder you run it from — keep it, do not commit it to GitHub.

> **Teardown is mandatory.** When the module ends, run Step 6 the same day. Set a calendar reminder now.

---

### Step 1 — Check your tools

Run from the shell you will use to execute the script (Git Bash, macOS Terminal, Ubuntu, or AWS CloudShell — not PowerShell):

```bash
aws --version
aws sts get-caller-identity
bash --version
```

- `aws --version` → `aws-cli/2.x.x ...` (install CLI v2 if missing)
- `aws sts get-caller-identity` → JSON showing your `Account` number; confirm it is your **lab** account, not a personal or work production account
- `bash --version` → must be **4.0 or newer**

> **macOS warning:** the system default is Bash 3.2 — the script will crash mid-run after creating partial resources. Fix: `brew install bash`, then run the script as `/opt/homebrew/bin/bash create_balerica_vpc.sh` (Apple Silicon) or `/usr/local/bin/bash create_balerica_vpc.sh` (Intel). Or use AWS CloudShell.

---

### Step 2 — Get the script

**Option A — clone the repo** (or pull if already cloned):

```bash
git clone https://github.com/BalericaAI/SEIR-Foundations.git
cd SEIR-Foundations/module1/lesson4_vpc
```

If already cloned: `cd ~/SEIR-Foundations && git pull && cd module1/lesson4_vpc`

> Windows Git Bash: before cloning, run `git config --global core.autocrlf input` to prevent CRLF line-ending conversion.

**Option B — download just the script:**

macOS / Ubuntu / Git Bash:
```bash
curl -fsSL -o create_balerica_vpc.sh \
  https://raw.githubusercontent.com/BalericaAI/SEIR-Foundations/main/module1/lesson4_vpc/create_balerica_vpc.sh
```

Windows PowerShell (download only — still must run from Git Bash / WSL / CloudShell):
```powershell
Invoke-WebRequest -Uri https://raw.githubusercontent.com/BalericaAI/SEIR-Foundations/main/module1/lesson4_vpc/create_balerica_vpc.sh -OutFile create_balerica_vpc.sh
```

Verify the download — first line must be `#!/usr/bin/env bash`, not `<!DOCTYPE html>`:
```bash
ls -l create_balerica_vpc.sh
head -1 create_balerica_vpc.sh
```

---

### Step 3 — Syntax-check the script

```bash
bash -n create_balerica_vpc.sh
```

No output = pass. If you see `syntax error near unexpected token '$'do\r''`, fix CRLF line endings:

```bash
# Git Bash / Ubuntu:
sed -i 's/\r$//' create_balerica_vpc.sh
# macOS:
sed -i '' 's/\r$//' create_balerica_vpc.sh
```

Then re-run `bash -n` — must be silent before continuing.

---

### Step 4 — Run the script (once)

```bash
bash create_balerica_vpc.sh
```

Takes 1–2 minutes. Expected final lines:

```
public-a: 10.20.1.0/24 (subnet-0...)
...
private2-c: 10.20.23.0/24 (subnet-0...)
+------------+---------------+----------------------+-------------------+
|     AZ     |     CIDR      |        Name          |     PublicIP      |
+------------+---------------+----------------------+-------------------+
|  us-east-1a|  10.20.1.0/24 |  balerica-public-a   |  True             |
...
Created VPC vpc-0.... Resource IDs saved in balerica-network.env.
```

**Run it once only.** A second run stops immediately with `State file already exists` or `Named VPC already exists` — both are safety guards, not errors. Never delete the state file to bypass them.

If the script stops mid-run, check `balerica-network.env` to see how far it got, fix the cause (usually expired credentials — rerun `aws sts get-caller-identity` first), and ask your instructor before any second attempt.

---

### Step 5 — Verify the build

```bash
cat balerica-network.env
source ./balerica-network.env
aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'length(Subnets)' --output text
```
Expected: `9`

```bash
aws ec2 describe-internet-gateways \
  --filters "Name=attachment.vpc-id,Values=$VPC_ID" --output table
```
Expected: one IGW attached to your VPC.

Also confirm in the AWS Console: **VPC → Your VPCs → balerica-vpc → Resource map** — nine subnets across three tiers and three AZs, one IGW.

---

### Alternative: Manual CLI build (Gate-by-Gate)

Use `VPC_cli_runbook.md` to build the same network command-by-command. **Do not run both methods against the same account** — they create duplicate resources. Use this path only on a fresh environment.

**Setup:**
```bash
aws --version && aws sts get-caller-identity
export AWS_REGION=us-east-1 AWS_DEFAULT_REGION="$AWS_REGION" AWS_PAGER=""
aws ec2 describe-availability-zones \
  --query 'AvailabilityZones[].{AZ:ZoneName,State:State}' --output table
```

**Variables:**
```bash
PROJECT=balerica
NETWORK_PREFIX=10.20
VPC_CIDR="${NETWORK_PREFIX}.0.0/16"
STATE_FILE="${PROJECT}-network.env"
AZ_A="${AWS_REGION}a"; AZ_B="${AWS_REGION}b"; AZ_C="${AWS_REGION}c"
```

Check no existing deployment: `aws ec2 describe-vpcs --filters "Name=tag:Name,Values=${PROJECT}-vpc" --query 'Vpcs[].VpcId' --output text` must return nothing.

Initialize state file:
```bash
umask 077
( set -o noclobber; : > "$STATE_FILE" )
save() { printf '%s=%q\n' "$1" "$2" >> "$STATE_FILE"; }
save AWS_REGION "$AWS_REGION"; save VPC_CIDR "$VPC_CIDR"
```

**Create VPC:**
```bash
VPC_ID=$(aws ec2 create-vpc --cidr-block "$VPC_CIDR" \
  --tag-specifications "ResourceType=vpc,Tags=[{Key=Name,Value=${PROJECT}-vpc}]" \
  --query 'Vpc.VpcId' --output text)
echo "$VPC_ID" && save VPC_ID "$VPC_ID"
aws ec2 wait vpc-available --vpc-ids "$VPC_ID"
aws ec2 modify-vpc-attribute --vpc-id "$VPC_ID" --enable-dns-support '{"Value":true}'
aws ec2 modify-vpc-attribute --vpc-id "$VPC_ID" --enable-dns-hostnames '{"Value":true}'
```

**Create and attach IGW:**
```bash
IGW_ID=$(aws ec2 create-internet-gateway \
  --tag-specifications "ResourceType=internet-gateway,Tags=[{Key=Name,Value=${PROJECT}-igw}]" \
  --query 'InternetGateway.InternetGatewayId' --output text)
echo "$IGW_ID" && save IGW_ID "$IGW_ID"
aws ec2 attach-internet-gateway --internet-gateway-id "$IGW_ID" --vpc-id "$VPC_ID"
```

**Create three route tables:**
```bash
PUBLIC_RT_ID=$(aws ec2 create-route-table --vpc-id "$VPC_ID" \
  --tag-specifications "ResourceType=route-table,Tags=[{Key=Name,Value=${PROJECT}-public-rt}]" \
  --query RouteTable.RouteTableId --output text)
echo "$PUBLIC_RT_ID" && save PUBLIC_RT_ID "$PUBLIC_RT_ID"

PRIVATE1_RT_ID=$(aws ec2 create-route-table --vpc-id "$VPC_ID" \
  --tag-specifications "ResourceType=route-table,Tags=[{Key=Name,Value=${PROJECT}-private1-rt}]" \
  --query RouteTable.RouteTableId --output text)
echo "$PRIVATE1_RT_ID" && save PRIVATE1_RT_ID "$PRIVATE1_RT_ID"

PRIVATE2_RT_ID=$(aws ec2 create-route-table --vpc-id "$VPC_ID" \
  --tag-specifications "ResourceType=route-table,Tags=[{Key=Name,Value=${PROJECT}-private2-rt}]" \
  --query RouteTable.RouteTableId --output text)
echo "$PRIVATE2_RT_ID" && save PRIVATE2_RT_ID "$PRIVATE2_RT_ID"

aws ec2 create-route --route-table-id "$PUBLIC_RT_ID" \
  --destination-cidr-block 0.0.0.0/0 --gateway-id "$IGW_ID"
```

**Create nine subnets:**
```bash
make_subnet() {
  aws ec2 create-subnet --vpc-id "$VPC_ID" \
    --cidr-block "${NETWORK_PREFIX}.$2.0/24" --availability-zone "$3" \
    --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=${PROJECT}-$1}]" \
    --query Subnet.SubnetId --output text
}
PUBLIC_A_ID=$(make_subnet public-a 1 "$AZ_A"); echo "$PUBLIC_A_ID"; save PUBLIC_A_ID "$PUBLIC_A_ID"
PUBLIC_B_ID=$(make_subnet public-b 2 "$AZ_B"); echo "$PUBLIC_B_ID"; save PUBLIC_B_ID "$PUBLIC_B_ID"
PUBLIC_C_ID=$(make_subnet public-c 3 "$AZ_C"); echo "$PUBLIC_C_ID"; save PUBLIC_C_ID "$PUBLIC_C_ID"
PRIVATE1_A_ID=$(make_subnet private1-a 11 "$AZ_A"); echo "$PRIVATE1_A_ID"; save PRIVATE1_A_ID "$PRIVATE1_A_ID"
PRIVATE1_B_ID=$(make_subnet private1-b 12 "$AZ_B"); echo "$PRIVATE1_B_ID"; save PRIVATE1_B_ID "$PRIVATE1_B_ID"
PRIVATE1_C_ID=$(make_subnet private1-c 13 "$AZ_C"); echo "$PRIVATE1_C_ID"; save PRIVATE1_C_ID "$PRIVATE1_C_ID"
PRIVATE2_A_ID=$(make_subnet private2-a 21 "$AZ_A"); echo "$PRIVATE2_A_ID"; save PRIVATE2_A_ID "$PRIVATE2_A_ID"
PRIVATE2_B_ID=$(make_subnet private2-b 22 "$AZ_B"); echo "$PRIVATE2_B_ID"; save PRIVATE2_B_ID "$PRIVATE2_B_ID"
PRIVATE2_C_ID=$(make_subnet private2-c 23 "$AZ_C"); echo "$PRIVATE2_C_ID"; save PRIVATE2_C_ID "$PRIVATE2_C_ID"
```

**Configure subnet attributes and route table associations:**
```bash
configure_subnet() {
  local subnet="$1" rt="$2" visibility="$3" key="$4" assoc
  aws ec2 wait subnet-available --subnet-ids "$subnet" || return 1
  if [[ "$visibility" == public ]]; then
    aws ec2 modify-subnet-attribute --subnet-id "$subnet" --map-public-ip-on-launch || return 1
  else
    aws ec2 modify-subnet-attribute --subnet-id "$subnet" --no-map-public-ip-on-launch || return 1
  fi
  assoc=$(aws ec2 associate-route-table --subnet-id "$subnet" \
    --route-table-id "$rt" --query AssociationId --output text) || return 1
  save "$key" "$assoc"
  echo "$subnet -> $rt ($assoc)"
}
configure_subnet "$PUBLIC_A_ID"   "$PUBLIC_RT_ID"   public  PUBLIC_A_ASSOC_ID
configure_subnet "$PUBLIC_B_ID"   "$PUBLIC_RT_ID"   public  PUBLIC_B_ASSOC_ID
configure_subnet "$PUBLIC_C_ID"   "$PUBLIC_RT_ID"   public  PUBLIC_C_ASSOC_ID
configure_subnet "$PRIVATE1_A_ID" "$PRIVATE1_RT_ID" private PRIVATE1_A_ASSOC_ID
configure_subnet "$PRIVATE1_B_ID" "$PRIVATE1_RT_ID" private PRIVATE1_B_ASSOC_ID
configure_subnet "$PRIVATE1_C_ID" "$PRIVATE1_RT_ID" private PRIVATE1_C_ASSOC_ID
configure_subnet "$PRIVATE2_A_ID" "$PRIVATE2_RT_ID" private PRIVATE2_A_ASSOC_ID
configure_subnet "$PRIVATE2_B_ID" "$PRIVATE2_RT_ID" private PRIVATE2_B_ASSOC_ID
configure_subnet "$PRIVATE2_C_ID" "$PRIVATE2_RT_ID" private PRIVATE2_C_ASSOC_ID
```

**Verify:**
```bash
aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'Subnets[].{Name:Tags[?Key==`Name`]|[0].Value,CIDR:CidrBlock,AZ:AvailabilityZone,PublicIP:MapPublicIpOnLaunch}' \
  --output table
aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'length(Subnets)' --output text
aws ec2 describe-vpc-attribute --vpc-id "$VPC_ID" --attribute enableDnsSupport
aws ec2 describe-vpc-attribute --vpc-id "$VPC_ID" --attribute enableDnsHostnames
aws ec2 describe-internet-gateways \
  --filters "Name=attachment.vpc-id,Values=$VPC_ID" --output table
```

Expected: 9 subnets; 3 public rows with `PublicIP: True`; 6 private rows `False`; one attached IGW; both DNS attributes `true`.

---

### Alternative: NAT Gateway Variant Script

Use `create_balerica_with_gateway_vpc.sh` instead of `create_balerica_vpc.sh` when instances in Private 1 or Private 2 need outbound internet access (e.g., to pull packages or call external APIs) without a public IP.

> **Cost warning:** NAT gateways bill ~$0.045/hr even when idle, plus data transfer. Run the teardown the same day.

**What it adds over the base script:**

| Addition | Detail |
|----------|--------|
| Elastic IP | Allocated before the loop, tagged `balerica-nat-eip` |
| NAT gateway | Created in `public-a` after public subnets are ready, tagged `balerica-nat` |
| Wait | `aws ec2 wait nat-gateway-available` — 1–2 minutes |
| Private routes | `0.0.0.0/0 → NAT_GW_ID` on both `private1-rt` and `private2-rt` |
| State file | Saves `EIP_ALLOC_ID` and `NAT_GW_ID` alongside all other IDs |

**Run it:**
```bash
bash -n create_balerica_with_gateway_vpc.sh      # syntax check
/opt/homebrew/bin/bash create_balerica_with_gateway_vpc.sh
```

Requires the same prerequisites as the base script: Bash 4+, AWS CLI v2, no existing `balerica-vpc`, no existing `balerica-network.env` state file.

---

### Step 6 — Teardown (mandatory when module ends)

Run from the same folder as `balerica-network.env`, in a Bash 4+ shell.

**Download the teardown script** (skip if you cloned the repo):

macOS / Ubuntu / Git Bash:
```bash
curl -fsSL -o delete_balerica_vpc.sh \
  https://raw.githubusercontent.com/BalericaAI/SEIR-Foundations/main/module1/lesson4_vpc/delete_balerica_vpc.sh
```

**Syntax-check:**
```bash
bash -n delete_balerica_vpc.sh
```

> **Bug fix (commit `a30cf13`):** Earlier versions of both teardown scripts used a JMESPath filter `[?!Associations[?Main==\`true\`]]` to find custom route tables. This filter silently returns empty when route tables have no subnet associations (e.g. after a partial teardown run), leaving route tables behind and causing `DependencyViolation` on VPC delete. Fixed in both scripts by querying all route tables and excluding the main one via the EC2 `association.main` filter.

#### If you used `create_balerica_with_gateway_vpc.sh` — use the matching teardown script

Use `delete_balerica_with_gateway_vpc.sh`. It automatically deletes the NAT gateway, waits for the ENI to clear, releases the Elastic IP, then tears down the rest of the VPC in one run.

```bash
bash -n delete_balerica_with_gateway_vpc.sh      # syntax check
/opt/homebrew/bin/bash delete_balerica_with_gateway_vpc.sh
```

The script prints the NAT gateway state and Elastic IP in the inventory, waits for your `DELETE vpc-...` confirmation, then handles everything in order:
1. Delete NAT gateway → wait for deleted state
2. Release Elastic IP
3. Wait for NAT gateway ENI to fully clear
4. Disassociate route tables → delete subnets → delete route tables → detach/delete IGW → delete VPC

> If you prefer to handle the NAT gateway manually first, delete it and release the EIP (see the manual steps below), then run `delete_balerica_vpc.sh` as usual.

#### Standard teardown (base script only — no NAT gateway)

**Run:**
```bash
/opt/homebrew/bin/bash delete_balerica_vpc.sh
```

The script verifies the VPC contents, prints an inventory, and waits for confirmation. Type `DELETE vpc-YOURVPCID` exactly as prompted:

```
Type DELETE vpc-0abc1234def567890 to proceed:
```

Expected completion:
```
VPC deleted and verified. State archived: balerica-network.env.deleted.YYYYMMDDTHHMMSSZ
```

**Verify in the console:** VPC → Your VPCs — `balerica-vpc` must no longer appear.

> If the script refuses with `Dependencies found`, something is still inside the VPC (stopped EC2, DB subnet group, NAT gateway, custom security group). Remove that resource first, then rerun.

#### Alternative: Manual teardown (no script)

Use this if the teardown script is unavailable or if you built the VPC manually via the Gate-by-Gate CLI method.

```bash
source ./balerica-network.env

# Step 1 — Remove NAT gateway and EIP (skip if you used the base script)
aws ec2 delete-nat-gateway --nat-gateway-id "$NAT_GW_ID"
aws ec2 wait nat-gateway-deleted --nat-gateway-ids "$NAT_GW_ID"
aws ec2 release-address --allocation-id "$EIP_ALLOC_ID"

# Step 2 — Disassociate and delete custom route tables
# Query all RTs, subtract the main one (JMESPath negation fails when associations are empty)
MAIN_RT=$(aws ec2 describe-route-tables \
  --filters "Name=vpc-id,Values=$VPC_ID" "Name=association.main,Values=true" \
  --query 'RouteTables[0].RouteTableId' --output text)
for rt in $(aws ec2 describe-route-tables \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'RouteTables[].RouteTableId' --output text); do
  [[ "$rt" == "$MAIN_RT" ]] && continue
  for assoc in $(aws ec2 describe-route-tables --route-table-ids "$rt" \
    --query 'RouteTables[0].Associations[?Main!=`true`].RouteTableAssociationId' \
    --output text); do
    aws ec2 disassociate-route-table --association-id "$assoc"
  done
  aws ec2 delete-route-table --route-table-id "$rt"
  echo "Deleted route table $rt"
done

# Step 3 — Delete all subnets
for subnet in $(aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'Subnets[].SubnetId' --output text); do
  aws ec2 delete-subnet --subnet-id "$subnet"
  echo "Deleted subnet $subnet"
done

# Step 4 — Detach and delete the Internet Gateway
aws ec2 detach-internet-gateway --internet-gateway-id "$IGW_ID" --vpc-id "$VPC_ID"
aws ec2 delete-internet-gateway --internet-gateway-id "$IGW_ID"

# Step 5 — Delete the VPC
aws ec2 delete-vpc --vpc-id "$VPC_ID"
echo "VPC $VPC_ID deleted."
```

**Verify nothing remains:**
```bash
aws ec2 describe-vpcs \
  --filters "Name=tag:Name,Values=balerica-vpc" \
  --query 'length(Vpcs)' --output text          # expect: 0
aws ec2 describe-nat-gateways \
  --filter "Name=state,Values=available,pending,deleting" \
  --query 'length(NatGateways)' --output text   # expect: 0
aws ec2 describe-addresses \
  --query 'Addresses[?AssociationId==null].AllocationId' \
  --output text                                 # expect: empty
```

---

### Checklist

- [ ] `aws sts get-caller-identity` confirmed lab account
- [ ] Bash ≥ 4.0 confirmed in the shell used (macOS: Homebrew Bash or CloudShell)
- [ ] `bash -n create_balerica_vpc.sh` returned silence
- [ ] Script ran once and ended with `Created VPC vpc-... Resource IDs saved in balerica-network.env.`
- [ ] Subnet count query returns `9`
- [ ] IGW table shows one gateway attached to the VPC
- [ ] AWS Console resource map matches the design table
- [ ] `balerica-network.env` kept locally and not committed to GitHub
- [ ] Calendar reminder set for teardown
- [ ] *(When module ends)* `bash delete_balerica_vpc.sh` ran, `DELETE vpc-...` typed, ended with `VPC deleted and verified`
- [ ] *(When module ends)* Archived `.deleted.` file exists; console shows no `balerica-vpc`

### Troubleshooting

| Symptom | Fix |
|---------|-----|
| `aws: command not found` | Install AWS CLI v2; open a new terminal after install |
| `Unable to locate credentials` / `ExpiredToken` | Run `aws configure` or refresh session; retest with `aws sts get-caller-identity` |
| `syntax error near unexpected token '$'do\r''` | CRLF line endings — run `sed -i 's/\r$//' create_balerica_vpc.sh` |
| `bad substitution` midway (macOS) | Bash 3.2 — resources up to that point were created; use Homebrew Bash 5 or CloudShell |
| `State file already exists` | Script already ran — safety stop; inspect before doing anything |
| `Named VPC already exists` | A `balerica-vpc` already exists in the account — do not duplicate; inspect first |
| `UnauthorizedOperation` | IAM permission missing — show your instructor the exact error message |
| First line of file is `<!DOCTYPE html>` | Saved the GitHub web page — re-download from the **raw** URL |
| `STOP: Missing balerica-network.env` (teardown) | Not in the folder where the create script ran — `cd` there first |
| `STOP: Dependencies found` (teardown) | VPC not empty — remove the named resource (EC2, RDS subnet group, NAT, custom SG) then rerun |
| `STOP: Cancelled; no resources deleted` | Confirmation not typed exactly — rerun when ready |
| `declare: -A: invalid option` (teardown, macOS) | Bash 3.2 — nothing was touched; use Homebrew Bash 5 or CloudShell |

---

### Advanced: Manual CLI Method (Gate-by-Gate)

Build the same VPC manually using AWS CLI commands — one gate at a time. Use this to understand what `create_balerica_vpc.sh` automates. **Do not run both methods against the same environment.**

#### Gate 01 — Understand the design

VPC CIDR: `10.20.0.0/16` (65,536 addresses). Each /24 has 256 addresses; AWS reserves 5, leaving 251. The third octet encodes tier and AZ — e.g., `10.20.22.47` → database tier, AZ B. AZ letters can map to different physical zones per account.

#### Gate 02 — Prepare your terminal

Use AWS CloudShell in us-east-1, or Bash on Linux/macOS/WSL with AWS CLI v2. Do not paste Bash into PowerShell or CMD.

```bash
aws --version
aws sts get-caller-identity
export AWS_REGION=us-east-1
export AWS_DEFAULT_REGION="$AWS_REGION"
export AWS_PAGER=""
aws ec2 describe-availability-zones \
  --query 'AvailabilityZones[].{AZ:ZoneName,State:State,ID:ZoneId}' \
  --output table
```

Confirm `a`, `b`, and `c` are available. Stop if any command fails.

#### Gate 03 — Define variables once

```bash
PROJECT=balerica
NETWORK_PREFIX=10.20
VPC_CIDR="${NETWORK_PREFIX}.0.0/16"
STATE_FILE="${PROJECT}-network.env"
AZ_A="${AWS_REGION}a"
AZ_B="${AWS_REGION}b"
AZ_C="${AWS_REGION}c"
printf 'Project: %s\nVPC: %s\nRegion: %s\n' "$PROJECT" "$VPC_CIDR" "$AWS_REGION"
aws ec2 describe-vpcs \
  --filters "Name=tag:Name,Values=${PROJECT}-vpc" \
  --query 'Vpcs[].{ID:VpcId,CIDR:CidrBlock}' --output table
ls -l "$STATE_FILE" 2>/dev/null || true
```

> **Warning:** If a matching VPC or state file already exists, stop and inspect it. Do not create duplicates.

Initialize the state file (only after confirming no existing deployment):

```bash
umask 077
( set -o noclobber; : > "$STATE_FILE" )
save() { printf '%s=%q\n' "$1" "$2" >> "$STATE_FILE"; }
save AWS_REGION "$AWS_REGION"
save VPC_CIDR "$VPC_CIDR"
```

#### Gate 04 — Create the VPC

```bash
VPC_ID=$(aws ec2 create-vpc --cidr-block "$VPC_CIDR" \
  --tag-specifications "ResourceType=vpc,Tags=[{Key=Name,Value=${PROJECT}-vpc}]" \
  --query 'Vpc.VpcId' --output text)
echo "$VPC_ID"
```

Confirm a real `vpc-...` ID before proceeding — blank or `None` is not success.

```bash
save VPC_ID "$VPC_ID"
aws ec2 wait vpc-available --vpc-ids "$VPC_ID"
aws ec2 modify-vpc-attribute --vpc-id "$VPC_ID" --enable-dns-support '{"Value":true}'
aws ec2 modify-vpc-attribute --vpc-id "$VPC_ID" --enable-dns-hostnames '{"Value":true}'
aws ec2 describe-vpcs --vpc-ids "$VPC_ID" --output table
```

#### Gate 05 — Create and attach the Internet Gateway

```bash
IGW_ID=$(aws ec2 create-internet-gateway \
  --tag-specifications "ResourceType=internet-gateway,Tags=[{Key=Name,Value=${PROJECT}-igw}]" \
  --query 'InternetGateway.InternetGatewayId' --output text)
echo "$IGW_ID"
```

Confirm `igw-...`, then attach:

```bash
save IGW_ID "$IGW_ID"
aws ec2 attach-internet-gateway --internet-gateway-id "$IGW_ID" --vpc-id "$VPC_ID"
aws ec2 describe-internet-gateways --internet-gateway-ids "$IGW_ID" --output table
```

#### Gate 06 — Create three route tables

Confirm each `rtb-...` ID before saving or continuing.

```bash
PUBLIC_RT_ID=$(aws ec2 create-route-table --vpc-id "$VPC_ID" \
  --tag-specifications "ResourceType=route-table,Tags=[{Key=Name,Value=${PROJECT}-public-rt}]" \
  --query RouteTable.RouteTableId --output text)
echo "$PUBLIC_RT_ID"
save PUBLIC_RT_ID "$PUBLIC_RT_ID"

PRIVATE1_RT_ID=$(aws ec2 create-route-table --vpc-id "$VPC_ID" \
  --tag-specifications "ResourceType=route-table,Tags=[{Key=Name,Value=${PROJECT}-private1-rt}]" \
  --query RouteTable.RouteTableId --output text)
echo "$PRIVATE1_RT_ID"
save PRIVATE1_RT_ID "$PRIVATE1_RT_ID"

PRIVATE2_RT_ID=$(aws ec2 create-route-table --vpc-id "$VPC_ID" \
  --tag-specifications "ResourceType=route-table,Tags=[{Key=Name,Value=${PROJECT}-private2-rt}]" \
  --query RouteTable.RouteTableId --output text)
echo "$PRIVATE2_RT_ID"
save PRIVATE2_RT_ID "$PRIVATE2_RT_ID"

aws ec2 create-route \
  --route-table-id "$PUBLIC_RT_ID" \
  --destination-cidr-block 0.0.0.0/0 \
  --gateway-id "$IGW_ID"
```

#### Gate 07 — Create nine subnets

First run Public A manually and confirm `subnet-...`:

```bash
PUBLIC_A_ID=$(aws ec2 create-subnet --vpc-id "$VPC_ID" \
  --cidr-block "${NETWORK_PREFIX}.1.0/24" --availability-zone "$AZ_A" \
  --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=${PROJECT}-public-a}]" \
  --query Subnet.SubnetId --output text)
echo "$PUBLIC_A_ID"
```

Define the helper, then create the remaining eight subnets:

```bash
make_subnet() {
  aws ec2 create-subnet --vpc-id "$VPC_ID" \
    --cidr-block "${NETWORK_PREFIX}.$2.0/24" --availability-zone "$3" \
    --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=${PROJECT}-$1}]" \
    --query Subnet.SubnetId --output text
}
save PUBLIC_A_ID "$PUBLIC_A_ID"

PUBLIC_B_ID=$(make_subnet public-b 2 "$AZ_B");   echo "$PUBLIC_B_ID"; save PUBLIC_B_ID "$PUBLIC_B_ID"
PUBLIC_C_ID=$(make_subnet public-c 3 "$AZ_C");   echo "$PUBLIC_C_ID"; save PUBLIC_C_ID "$PUBLIC_C_ID"
PRIVATE1_A_ID=$(make_subnet private1-a 11 "$AZ_A"); echo "$PRIVATE1_A_ID"; save PRIVATE1_A_ID "$PRIVATE1_A_ID"
PRIVATE1_B_ID=$(make_subnet private1-b 12 "$AZ_B"); echo "$PRIVATE1_B_ID"; save PRIVATE1_B_ID "$PRIVATE1_B_ID"
PRIVATE1_C_ID=$(make_subnet private1-c 13 "$AZ_C"); echo "$PRIVATE1_C_ID"; save PRIVATE1_C_ID "$PRIVATE1_C_ID"
PRIVATE2_A_ID=$(make_subnet private2-a 21 "$AZ_A"); echo "$PRIVATE2_A_ID"; save PRIVATE2_A_ID "$PRIVATE2_A_ID"
PRIVATE2_B_ID=$(make_subnet private2-b 22 "$AZ_B"); echo "$PRIVATE2_B_ID"; save PRIVATE2_B_ID "$PRIVATE2_B_ID"
PRIVATE2_C_ID=$(make_subnet private2-c 23 "$AZ_C"); echo "$PRIVATE2_C_ID"; save PRIVATE2_C_ID "$PRIVATE2_C_ID"
```

#### Gate 08 — Configure subnet attributes and associations

```bash
configure_subnet() {
  local subnet="$1" rt="$2" visibility="$3" key="$4" assoc
  aws ec2 wait subnet-available --subnet-ids "$subnet" || return 1
  if [[ "$visibility" == public ]]; then
    aws ec2 modify-subnet-attribute --subnet-id "$subnet" --map-public-ip-on-launch || return 1
  else
    aws ec2 modify-subnet-attribute --subnet-id "$subnet" --no-map-public-ip-on-launch || return 1
  fi
  assoc=$(aws ec2 associate-route-table \
    --subnet-id "$subnet" --route-table-id "$rt" \
    --query AssociationId --output text) || return 1
  save "$key" "$assoc"
  echo "$subnet -> $rt ($assoc)"
}

configure_subnet "$PUBLIC_A_ID"   "$PUBLIC_RT_ID"   public  PUBLIC_A_ASSOC_ID
configure_subnet "$PUBLIC_B_ID"   "$PUBLIC_RT_ID"   public  PUBLIC_B_ASSOC_ID
configure_subnet "$PUBLIC_C_ID"   "$PUBLIC_RT_ID"   public  PUBLIC_C_ASSOC_ID
configure_subnet "$PRIVATE1_A_ID" "$PRIVATE1_RT_ID" private PRIVATE1_A_ASSOC_ID
configure_subnet "$PRIVATE1_B_ID" "$PRIVATE1_RT_ID" private PRIVATE1_B_ASSOC_ID
configure_subnet "$PRIVATE1_C_ID" "$PRIVATE1_RT_ID" private PRIVATE1_C_ASSOC_ID
configure_subnet "$PRIVATE2_A_ID" "$PRIVATE2_RT_ID" private PRIVATE2_A_ASSOC_ID
configure_subnet "$PRIVATE2_B_ID" "$PRIVATE2_RT_ID" private PRIVATE2_B_ASSOC_ID
configure_subnet "$PRIVATE2_C_ID" "$PRIVATE2_RT_ID" private PRIVATE2_C_ASSOC_ID
```

#### Gate 09 — Verify

```bash
aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'Subnets[].{Name:Tags[?Key==`Name`]|[0].Value,CIDR:CidrBlock,AZ:AvailabilityZone,PublicIP:MapPublicIpOnLaunch,Free:AvailableIpAddressCount}' \
  --output table
aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'length(Subnets)' --output text
aws ec2 describe-route-tables \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'RouteTables[].{ID:RouteTableId,Routes:Routes,Associations:Associations}' \
  --output json
aws ec2 describe-vpc-attribute --vpc-id "$VPC_ID" --attribute enableDnsSupport
aws ec2 describe-vpc-attribute --vpc-id "$VPC_ID" --attribute enableDnsHostnames
aws ec2 describe-internet-gateways \
  --filters "Name=attachment.vpc-id,Values=$VPC_ID" --output table
```

Expected: 9 subnets; 3 with public IPv4 mapping true, 6 false; 4 route tables (including AWS-created main); only the public table has an IGW default route; 1 attached IGW; both DNS attributes true.

#### Gate 10 — Resume a later session

Inspect the state file before sourcing it:

```bash
cat balerica-network.env
source ./balerica-network.env
export AWS_REGION AWS_DEFAULT_REGION="$AWS_REGION" AWS_PAGER=""
aws sts get-caller-identity
aws ec2 describe-vpcs --vpc-ids "$VPC_ID" --output table
```

> The Private 2 IDs are used in Lab 5 for an Aurora DB subnet group; Private 1 IDs in the ASG lab. Keep this VPC if continuing the course. Network-only resources generally do not incur hourly charges — but later public IPv4, NAT, EC2, ALB, Aurora, and traffic do.

---

## AWS CLI Profiles

Four named profiles are configured for this course — one per AWS Organizations account.

| Profile | Account ID | Access method |
|---------|-----------|---------------|
| `master` | `755905325228` | IAM user `AWSCLI` (direct) |
| `dev` | `932544973202` | `OrganizationAccountAccessRole` (assumed role) |
| `qa` | `199332560469` | `OrganizationAccountAccessRole` (assumed role) |
| `prod` | `076525066515` | `OrganizationAccountAccessRole` (assumed role) |

### Check which account you're currently using

```bash
aws sts get-caller-identity
```

### Check a specific profile

```bash
aws sts get-caller-identity --profile <name>
```

### List all four profiles and their account IDs

```bash
for profile in master dev qa prod; do
  account=$(aws sts get-caller-identity --profile "$profile" --query Account --output text)
  echo "$profile → $account"
done
```

### Switch to a profile for the whole session

```bash
export AWS_PROFILE=dev      # or master, qa, prod
aws sts get-caller-identity  # verify
```

> **Note:** `export AWS_PROFILE` only lasts for the current terminal session. For AWS operations always confirm your active account before running scripts — especially teardown or destructive commands.

### Switch back to master

```bash
export AWS_PROFILE=master
```

---
