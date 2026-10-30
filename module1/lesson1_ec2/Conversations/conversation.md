# Lesson 1 (EC2) — Working Session with Claude Code

A written record of one working session between me and Claude Code (an AI coding assistant) while doing the Balerica Legacy Bank lab on EC2. It is written for peer review, so it is organized by topic and not as a raw chat log.

**How to read this:** each section gives the problem, what was done, the commands used, and the outcome. Things that did *not* work are included on purpose.

> **Note on accuracy:** this is a summary of the session, not a verbatim transcript. Commands were either run by Claude from my Mac, or run by me on the EC2 instance. Each section says which. The AWS account ID, public hostnames and public IPs are replaced with placeholders.

---

## Contents

1. [Fixing `menu.sh`](#1-fixing-menush)
2. [Checking Amazon Bedrock access](#2-checking-amazon-bedrock-access)
3. [Testing which Claude models are usable](#3-testing-which-claude-models-are-usable)
4. [Starting the API with the model ID and region](#4-starting-the-api-with-the-model-id-and-region)
5. [Why `/ask` stayed offline, and the fix](#5-why-ask-stayed-offline-and-the-fix)
6. [Same problem on a new instance](#6-same-problem-on-a-new-instance)
7. [Triggering COBOL return codes 8 and 12](#7-triggering-cobol-return-codes-8-and-12)
8. [Reading the fixed-width ledger with `cut`](#8-reading-the-fixed-width-ledger-with-cut)
9. [Cloning the homework repo onto EC2](#9-cloning-the-homework-repo-onto-ec2)
10. [Summary of everything that changed in AWS](#10-summary-of-everything-that-changed-in-aws)

---

## 1. Fixing `menu.sh`

**Problem.** Running `./menu.sh` on the EC2 instance failed:

```text
./menu.sh: line 32: `COMMANDS[15]': not a valid identifier
./menu.sh: line 51: syntax error near unexpected token `)'
```

**Cause** (found by Claude reading the script):
- The `COMMANDS[15]` value was wrapped in double quotes but contained more double quotes inside, so bash ended the string early. The value also ran across several lines.
- Lines 38–44 were a leftover `if ... fi"` block that had spilled outside the string, causing the second error.
- The EC2 metadata URLs were truncated (`http://169.254.169` instead of `http://169.254.169.254/latest/...`).

**Fix.**
- Entry 14: removed the embedded newline.
- Entry 15: rewritten as a single-quoted one-liner that returns the public IPv4 using IMDSv2 (the EC2 metadata service that needs a token), with full URLs.
- Entry 16 (new): returns the public DNS name from `meta-data/public-hostname`.
- Checked with `bash -n menu.sh` (syntax only). It was **not** run on EC2 by Claude.

**Git.** The fix was left uncommitted at my request. `menu.sh` was staged in its original (broken) form, so it needed `git add` again before committing.

---

## 2. Checking Amazon Bedrock access

**Question.** Does the IAM user `iamadmin` have access to Bedrock?

**What Claude checked** (from its own CLI session, which is signed in as a different IAM user, `AWSCLI`):

| Check | Result |
|---|---|
| Policies on `iamadmin` | `AdministratorAccess` attached directly, no groups |
| Permissions boundary | None |
| Policy simulator: `bedrock:InvokeModel` | allowed |
| AWS Organizations / SCPs | Account is not in an organization, so no SCPs apply |

**Conclusion.** IAM-wise, yes. A separate, account-level issue showed up next: which *models* are enabled.

---

## 3. Testing which Claude models are usable

Claude listed the Bedrock catalog in `us-east-1` (about 110 models) and then invoked individual Claude models with the Converse API:

```bash
aws bedrock-runtime converse --region us-east-1 \
  --model-id us.anthropic.claude-sonnet-4-6 \
  --messages '[{"role":"user","content":[{"text":"Reply with the single word: pong"}]}]' \
  --inference-config '{"maxTokens":20}'
```

**Results.**

| Model | Result |
|---|---|
| Haiku 4.5 | Works |
| Sonnet 4.5 | Works |
| Opus 4.5 | Works |
| Sonnet 4.6 | Works |
| Opus 4.6 | Works |
| Opus 4.7 | Blocked |
| Opus 4.8 | Blocked |
| Opus 5.5 | Blocked |
| Sonnet 5.5 | Blocked |
| Haiku 5.5 | Blocked |

The blocked ones returned `AccessDeniedException: ... is not available for this account`. This is an account-level restriction and **not** an IAM problem, so it can't be fixed with a policy. Sonnet 5, Opus 5, and Fable 5 / 5.1 were not tested.

**Model ID.** Newer models need an *inference profile* ID (prefix `us.` or `global.`) and not the bare model ID. I used:

```text
us.anthropic.claude-sonnet-4-6
```

Commands to look it up:

```bash
aws bedrock list-inference-profiles --region us-east-1 \
  --query "inferenceProfileSummaries[?contains(inferenceProfileId,'sonnet-4-6')].inferenceProfileId" --output text
```

---

## 4. Starting the API with the model ID and region

The model ID and region are read from **environment variables when the server starts**. Putting them in the `curl` request does nothing (I tried adding `model_id` and `region` to the JSON body and the app ignored them).

```bash
BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-6 AWS_REGION=us-east-1 \
  uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The request used to test it, run from a second terminal:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{"question": "What does return code 8 mean?"}'
```

**How to tell where an answer came from:** the response has a `source` field. `"source": "offline-knowledge-base"` means the app fell back to its built-in notes and did **not** call Bedrock.

---

## 5. Why `/ask` stayed offline, and the fix

**Symptom.** Every `/ask` response said `"source": "offline-knowledge-base"`, even after setting the variables.

**How the app decides** (from the lab README): Bedrock only answers if all three are true:
1. An IAM role is attached to the EC2 instance with Bedrock permissions.
2. `AWS_REGION` is set correctly.
3. `BEDROCK_MODEL_ID` is a real inference-profile ID.

**Finding.** Claude looked up the instance and found it had **no IAM instance profile**. With no role there are no credentials, so the app silently fell back to offline mode.

```bash
aws ec2 describe-instances --region us-east-1 \
  --filters Name=private-ip-address,Values=<instance-private-ip> \
  --query 'Reservations[].Instances[].[InstanceId,State.Name,IamInstanceProfile.Arn]' --output text
# -> instance running, IamInstanceProfile = None
```

I couldn't test from inside the instance (no SSM agent, no SSH from Claude's side), so the diagnosis came from AWS-side checks.

**Fix (done by Claude, with my approval).**

| # | Action | Result |
|---|---|---|
| 1 | Checked for existing roles / instance profiles | None found |
| 2 | Created role `balerica-ec2-bedrock-role` with an EC2 trust policy | Created |
| 3 | Added inline policy `bedrock-invoke` | Allows `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream` on Anthropic models and this account's inference profiles |
| 4 | Created instance profile `balerica-ec2-bedrock-profile` | Created |
| 5 | Added the role to the profile | Done |
| 6 | Attached the profile to the instance | State: `associated` |

**Verification (run by me on the instance).**

```bash
aws sts get-caller-identity
# Arn: .../assumed-role/balerica-ec2-bedrock-role/<instance-id>   <- role is working

aws bedrock-runtime converse --region us-east-1 \
  --model-id us.anthropic.claude-sonnet-4-6 \
  --messages '[{"role":"user","content":[{"text":"Reply with the single word: pong"}]}]' \
  --inference-config '{"maxTokens":20}'
# -> "pong"  (latency 690 ms)
```

One early attempt failed because of a copy/paste slip (a stray `"` and a second command pasted into it). It was cancelled with Ctrl+C and was not an AWS error.

After restarting uvicorn with the variables set, `/ask` answered from Bedrock. This is the part the peer reviewer should check first: **the missing instance profile was the real cause.** I don't know whether the earlier restarts had the variables set, so I can't say how much they contributed.

**Rollback** (if ever needed): `disassociate-iam-instance-profile`, then `remove-role-from-instance-profile`, `delete-instance-profile`, `delete-role-policy`, `delete-role`.

---

## 6. Same problem on a new instance

**Symptom.** On a freshly launched instance:

```text
aws: [ERROR]: An error occurred (NoCredentials): Unable to locate credentials.
```

**Cause.** The profile is not automatic. A new instance starts with no profile attached.

**Fix.** Claude looked up the new instance, confirmed it had no profile and that `balerica-ec2-bedrock-profile` still contained the role, then attached it:

```bash
aws ec2 associate-iam-instance-profile --region us-east-1 \
  --instance-id <new-instance-id> \
  --iam-instance-profile Name=balerica-ec2-bedrock-profile
```

**Tip to avoid repeating this:** when launching an instance, pick `balerica-ec2-bedrock-profile` under *Advanced details → IAM instance profile*.

---

## 7. Triggering COBOL return codes 8 and 12

I asked Claude to read the instructor's repo (`BalericaAI/SEIR-Foundations`) and explain how to trigger return codes 8 and 12. Claude cloned it into a throw-away folder under `/tmp` and only **read** the files (it ran no code from the repo).

**What the return codes mean** (from the README and the `.cob` source):

| Code | Meaning |
|---|---|
| 0 | Success (payment POSTED / account found) |
| 4 | Warning (account not found) |
| 8 | Business rejection (not ACTIVE, zero amount, insufficient funds) |
| 12 | Environment failure (missing or unwritable file, malformed arguments) |

### Return code 8 (run from `/opt/balerica-bank`)

```bash
./cobol/bin/payment_post TXN0101 100001 0 USD ZERO-TEST          # zero amount
./cobol/bin/payment_post TXN0102 100001 99999999 USD BIG-TEST    # insufficient funds
./cobol/bin/account_lookup                                       # no account ID
echo $?                                                          # prints 8 after each
```

A non-ACTIVE account also gives 8, but only if you edit `data/accounts.dat` by hand (status is columns 37–44).

### Return code 12 — the first idea didn't work through the API

Claude's first suggestion was to run a COBOL program from the wrong folder so `data/accounts.dat` can't be found. That works on the command line:

```bash
cd ~
/opt/balerica-bank/cobol/bin/account_lookup 100001
echo $?        # 12, with FILE-STATUS=35
```

But I run the API server from the correct folder, and `cobol_bridge.py` runs COBOL with `cwd=BANK_HOME` and rewrites `accounts.dat` before every call. So this route can't be triggered through the web UI.

### Return code 12 — what worked

`payment_post` returns 12 when it can't open `data/payments.dat` for appending. The bridge only runs `touch` on that file, which still succeeds on a read-only file the user owns.

```bash
# 1. make the journal read-only
chmod 444 /opt/balerica-bank/data/payments.dat

# 2. in the browser at /docs, POST /payments:
#    {"reference":"TEST-12","account_id":"100001","amount":10,"currency":"USD"}
#    expected: HTTP 422, "cobol_return_code": 12, reason "CANNOT OPEN data/payments.dat"

# 3. restore it, or every later payment will fail
chmod 644 /opt/balerica-bank/data/payments.dat
```

**Result:** it worked for me. The failed attempts also appear in the transactions table as `REJECTED`, which is expected.

A second idea (sending an `account_id` of six spaces and a `currency` of three spaces to create a malformed request) was derived from the code but **never tested**, and it would save a row with a blank account ID, so I didn't use it.

---

## 8. Reading the fixed-width ledger with `cut`

`data/accounts.dat` has no delimiters. Every record is 59 characters at fixed positions:

| Field | Columns | Width |
|---|---|---|
| Account ID | 1–6 | 6 |
| Customer name | 7–36 | 30 |
| Status | 37–44 | 8 |
| Balance | 45–56 | 12 digits, implied decimal |
| Currency | 57–59 | 3 |

```bash
cd /opt/balerica-bank
cut -c1-6   data/accounts.dat    # account IDs
cut -c7-36  data/accounts.dat    # names
cut -c45-56 data/accounts.dat    # raw balance digits

grep '^100001' data/accounts.dat | cut -c45-56     # one account's raw balance
grep '^100001' data/accounts.dat | cut -c45-56 | awk '{printf "%.2f\n", $1/100}'
```

**Decoding the balance.** The COBOL picture `PIC 9(10)V99` means 10 digits, an *implied* decimal point (`V`, not stored), then 2 digits. So the last two digits are cents:

```text
000000475652  ->  0000004756.52  ->  4756.52
```

**Two mistakes worth noting for reviewers:**
- `printf("Account ID" + cut -c1-6 data/accounts.dat)` does not work. That is C/Python syntax and the shell can't concatenate that way. Use `echo "Account ID: $(cut -c1-6 data/accounts.dat)"` or pipe through `awk`.
- `grep 'TXN-XX-' data/payments.dat` returns nothing, because the app's transaction IDs are `TXN` plus 17 digits with no dashes. `TXN-XX-` is a placeholder in the lab text.

---

## 9. Cloning the homework repo onto EC2

```bash
sudo dnf install -y git
cd ~
git clone https://github.com/Twolliston-CPG/seir-foundations.git
ls -la seir-foundations/module1
# screenshot the terminal as git_clone.jpg
```

Notes: the clone only works without a login if the repo is public, and only committed and pushed files appear on the instance.

---

## 10. Summary of everything that changed in AWS

These are the only changes made to my AWS account during the session, all made by Claude with my approval:

| Resource | Name / ID | Purpose |
|---|---|---|
| IAM role | `balerica-ec2-bedrock-role` | Lets EC2 instances call Bedrock |
| Inline policy | `bedrock-invoke` | `InvokeModel` and `InvokeModelWithResponseStream` on Anthropic models and this account's inference profiles |
| Instance profile | `balerica-ec2-bedrock-profile` | Wrapper that attaches the role to an EC2 instance |
| Profile association | first EC2 instance | Fixed `/ask` falling back to offline |
| Profile association | second (new) EC2 instance | Fixed `NoCredentials` |

**Not changed:** no Bedrock model access settings, no security groups, no existing IAM users or policies. Nothing was committed to git.

### Key lessons

1. `source: "offline-knowledge-base"` means Bedrock was **not** called. The usual cause is no credentials, and no IAM role on the instance is the most likely reason.
2. Model ID and region are environment variables read at **startup**, so they belong on the `uvicorn` command and not in the `curl` request.
3. Blocked models were an **account-level** restriction, separate from IAM permissions.
4. New EC2 instances don't inherit the instance profile, so attach it at launch.
5. To trigger a COBOL return code through the API, work out which step of the code runs and which file or argument it depends on, because the bridge resets some conditions on every call.
