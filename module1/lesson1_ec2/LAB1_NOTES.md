# Lab 1 Notes — lesson1_ec2 (Balerica Legacy Bank)

**Name:** Tim Wolliston · **Initials for TXN IDs:** TW · **Time zone:** America/New_York

> Each run: start with run number + Instance ID, write **at least 3 sentences** (what changed, errors hit and fixes, what I newly understood), and paste **at least one exact output line** only that run would have (e.g. the uvicorn `Started server process [PID]` line, or a real error message).

---

## Run 1 — Instance ID: `i-06bac9d9f7b16c1ed`

- **Date / time:** 2026-10-29 / 9:39:04· **Boot time (UTC):** 12:43:00 · **Public DNS:** ec2-54-197-24-174.compute-1.amazonaws.com
- **Screenshot:** [lab1_run1.jpg](screenshots/lab1_run1.jpg)

**What changed this run:**
1. I failed to read thoroughly the instructions for the notes.md and corrected an issue I had with step 8. I got the "offline-knowledge-base" in the responce.

```bash
curl -X POST http://127.0.0.1:8000/ask   -H 'Content-Type: application/json'   -d '{"question": "What does return code 8 mean?"}'
```

```bash
  {"question":"What does return code 8 mean?","response":"COBOL return codes in this lab (the mainframe convention):\n  0  = success (account found / payment POSTED)\n  4  = warning (account not found)\n  8  = business rejection (not ACTIVE, zero amount, insufficient funds)\n  12 = environment failure (missing file, malformed arguments)\nCheck them in the shell with: echo $?\n\nCurrent ledger: 100001 (ACTIVE, 4756.52 USD), 100002 (ACTIVE, 2750.00 USD), 100003 (ACTIVE, 6703.70 USD).\n\nLast 10 transactions: 7 POSTED, 3 other.","source":"offline-knowledge-base"}[ec2-user@ip-172-31-25-242 balerica-bank]$
```
2. I mistakenly skipped capturing a screenshot for step3c. **View the fixed-width payment journal:** cat data/payments.dat


**Errors hit and how I fixed them:**
N/A

**What I newly understood:**
1. For step 4 Why I needed to have the following done in AWS:

1.a I created the IAM role balerica-ec2-bedrock-role with a trust policy for EC2.

1.b I added an inline policy, bedrock-invoke, allowing InvokeModel and InvokeModelWithResponseStream on Anthropic models and this account's inference profiles.

1.c I created the instance profile balerica-ec2-bedrock-profile, added the role to it, and attached it to the instance. The association showed associated.

2. For step 4. Why the web server must be started as the following

**(venv) [ec2-user@ip-172-31-31-78 balerica-bank]$ BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-6 AWS_REGION=us-east-1 uvicorn app.main:app --host 0.0.0.0 --port 8000** instead of **uvicorn app.main:app --host 0.0.0.0 --port 8000** in order for step8 to return an answer from an AI model

3. For step 8. Why the **Ask Balerica AI for help** command needed to invoke an AWS Bedrock Model.

   **This method will not return an answer from AI:**
   ```bash
   curl -X POST http://127.0.0.1:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{"question": "What does return code 8 mean?"}'
  ```

**This method will return an answer from AI:**
```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H 'Content-Type: application/json'   \
  -d '{"question": "What does return code 8 mean?", \
  "model_id": "us.anthropic.claude-sonnet-4-6", \
  "region": "us-east-1"}'
```


**Exact output line only this run would have:**
```text

INFO:     Started server process [38563]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:36980 - "GET /status HTTP/1.1" 200 OK
INFO:     127.0.0.1:56436 - "GET /chewbacca HTTP/1.1" 200 OK
INFO:     127.0.0.1:42120 - "GET /status HTTP/1.1" 200 OK
INFO:     127.0.0.1:42130 - "POST /payments HTTP/1.1" 422 Unprocessable Entity
INFO:     127.0.0.1:42146 - "POST /payments HTTP/1.1" 200 OK
INFO:     127.0.0.1:42162 - "POST /payments HTTP/1.1" 200 OK
INFO:     127.0.0.1:42178 - "POST /payments HTTP/1.1" 422 Unprocessable Entity
INFO:     127.0.0.1:42194 - "POST /payments HTTP/1.1" 422 Unprocessable Entity
INFO:     127.0.0.1:42208 - "POST /payments HTTP/1.1" 200 OK
INFO:     127.0.0.1:42212 - "POST /payments HTTP/1.1" 200 OK
INFO:     127.0.0.1:42218 - "POST /payments HTTP/1.1" 422 Unprocessable Entity
INFO:     127.0.0.1:42220 - "POST /payments HTTP/1.1" 200 OK
INFO:     127.0.0.1:42236 - "POST /payments HTTP/1.1" 200 OK
INFO:     127.0.0.1:39172 - "GET /status HTTP/1.1" 200 OK
INFO:     127.0.0.1:39188 - "POST /payments HTTP/1.1" 200 OK
INFO:     127.0.0.1:39194 - "POST /payments HTTP/1.1" 200 OK
INFO:     127.0.0.1:39200 - "POST /payments HTTP/1.1" 200 OK
INFO:     108.83.255.226:59790 - "GET /docs HTTP/1.1" 200 OK
INFO:     108.83.255.226:59790 - "GET /openapi.json HTTP/1.1" 200 OK
INFO:     108.83.255.226:61389 - "GET /accounts/100001 HTTP/1.1" 200 OK
/opt/balerica-bank/venv/lib64/python3.9/site-packages/boto3/compat.py:89: PythonDeprecationWarning: Boto3 will no longer support Python 3.9 starting April 29, 2026. To continue receiving service updates, bug fixes, and security updates please upgrade to Python 3.10 or later. More information can be found here: https://aws.amazon.com/blogs/developer/python-support-policy-updates-for-aws-sdks-and-tools/
  warnings.warn(warning, PythonDeprecationWarning)
INFO:     127.0.0.1:40488 - "POST /ask HTTP/1.1" 200 OK
INFO:     127.0.0.1:50886 - "POST /ask HTTP/1.1" 200 OK
```

---

## Run 2 — Instance ID: `i-i-03654eddcd51d549f`

- **Date / time:** 2026-10-29 / 15:36:32 · **Boot time (UTC):** 15:15 · **Public DNS:** ec2-13-222-163-199.compute-1.amazonaws.com
- **Screenshot:** [lab1_run2.jpg](screenshots/lab1_run2.jpg)

**What changed this run:**
1. I failed to set the time zone after sshing into the 2nd run ec2 instance. This caused the times to be UTC time instead of the time for my actual time zone as seen in [lab1_run2.jpg](screenshots/lab1_run2.jpg)

```bash 
sudo timedatectl set-timezone America/New_York
```

**Errors hit and how I fixed them:**
[ec2-user@ip-172-31-31-78 balerica-bank]$ aws sts get-caller-identity

  aws: [ERROR]: An error occurred (NoCredentials): Unable to locate credentials. You can configure credentials by running "aws login".
  [ec2-user@ip-172-31-31-78 balerica-bank]$

**What I newly understood:**
I have to attach the newly crreated profile to every new instance. To avoid this next time, I must choose **balerica-ec2-bedrock-profile** profile when you launch it. Found under the advance section.

**Exact output line only this run would have:**
```text
INFO:     Started server process [36236]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:34072 - "GET /status HTTP/1.1" 200 OK
INFO:     127.0.0.1:35610 - "GET /chewbacca HTTP/1.1" 200 OK
INFO:     127.0.0.1:39490 - "GET /status HTTP/1.1" 200 OK
INFO:     127.0.0.1:39496 - "POST /payments HTTP/1.1" 200 OK
INFO:     127.0.0.1:39504 - "POST /payments HTTP/1.1" 422 Unprocessable Entity
INFO:     127.0.0.1:39516 - "POST /payments HTTP/1.1" 422 Unprocessable Entity
INFO:     127.0.0.1:39530 - "POST /payments HTTP/1.1" 200 OK
INFO:     127.0.0.1:39534 - "POST /payments HTTP/1.1" 422 Unprocessable Entity
INFO:     127.0.0.1:39550 - "POST /payments HTTP/1.1" 422 Unprocessable Entity
INFO:     127.0.0.1:39562 - "POST /payments HTTP/1.1" 200 OK
INFO:     127.0.0.1:39564 - "POST /payments HTTP/1.1" 422 Unprocessable Entity
INFO:     127.0.0.1:39576 - "POST /payments HTTP/1.1" 200 OK
INFO:     127.0.0.1:39580 - "POST /payments HTTP/1.1" 200 OK
INFO:     127.0.0.1:49886 - "GET /status HTTP/1.1" 200 OK
INFO:     127.0.0.1:49902 - "POST /payments HTTP/1.1" 422 Unprocessable Entity
INFO:     127.0.0.1:49914 - "POST /payments HTTP/1.1" 200 OK
INFO:     127.0.0.1:49930 - "POST /payments HTTP/1.1" 200 OK
INFO:     108.83.255.226:49800 - "GET /docs HTTP/1.1" 200 OK
INFO:     108.83.255.226:54836 - "GET /docs HTTP/1.1" 200 OK
INFO:     108.83.255.226:54836 - "GET /openapi.json HTTP/1.1" 200 OK
INFO:     108.83.255.226:49663 - "GET /accounts/100001 HTTP/1.1" 200 OK
/opt/balerica-bank/venv/lib64/python3.9/site-packages/boto3/compat.py:89: PythonDeprecationWarning: Boto3 will no longer support Python 3.9 starting April 29, 2026. To continue receiving service updates, bug fixes, and security updates please upgrade to Python 3.10 or later. More information can be found here: https://aws.amazon.com/blogs/developer/python-support-policy-updates-for-aws-sdks-and-tools/
  warnings.warn(warning, PythonDeprecationWarning)
INFO:     127.0.0.1:42008 - "POST /ask HTTP/1.1" 200 OK

```

---

## Run 3 — Instance ID: `i-________________`

- **Date / time:** ____ · **Boot time (UTC):** ____ · **Public DNS:** ____
- **Screenshot:** [lab1_run3.jpg](screenshots/lab1_run3.jpg)

**What changed this run:**

**Errors hit and how I fixed them:**

**What I newly understood:**

**Exact output line only this run would have:**
```text

```

---

## Run 4 — Instance ID: `i-________________`

- **Date / time:** ____ · **Boot time (UTC):** ____ · **Public DNS:** ____
- **Screenshot:** [lab1_run4.jpg](screenshots/lab1_run4.jpg)

**What changed this run:**

**Errors hit and how I fixed them:**

**What I newly understood:**

**Exact output line only this run would have:**
```text

```

---

## Run 5 — Instance ID: `i-________________`

- **Date / time:** ____ · **Boot time (UTC):** ____ · **Public DNS:** ____
- **Screenshot:** [lab1_run5.jpg](screenshots/lab1_run5.jpg)

**What changed this run:**

**Errors hit and how I fixed them:**

**What I newly understood:**

**Exact output line only this run would have:**
```text

```

---

## Run 6 — Instance ID: `i-________________`

- **Date / time:** ____ · **Boot time (UTC):** ____ · **Public DNS:** ____
- **Screenshot:** [lab1_run6.jpg](screenshots/lab1_run6.jpg)

**What changed this run:**

**Errors hit and how I fixed them:**

**What I newly understood:**

**Exact output line only this run would have:**
```text

```

---

## Run 7 — Instance ID: `i-________________`

- **Date / time:** ____ · **Boot time (UTC):** ____ · **Public DNS:** ____
- **Screenshot:** [lab1_run7.jpg](screenshots/lab1_run7.jpg)

**What changed this run:**

**Errors hit and how I fixed them:**

**What I newly understood:**

**Exact output line only this run would have:**
```text

```

---

## COBOL practice

- **Run used:** Run __ · **Instance ID:** `i-________________`
- **Folder:** `/opt/balerica-bank`

### Return code 0 — success ([cobol_rc0.jpg](screenshots/cobol_rc0.jpg))
```text
$ ./cobol/bin/payment_post TXN-XX-0001 100001 25.00 USD XX-RC0
(paste exact output)
$ echo $?
0
```

### Return code 4 — account not found ([cobol_rc4.jpg](screenshots/cobol_rc4.jpg))
```text
$ ./cobol/bin/payment_post TXN-XX-0002 999999 25.00 USD XX-RC4
(paste exact output)
$ echo $?
4
```

### Return code 8 — business rejection, zero amount ([cobol_rc8.jpg](screenshots/cobol_rc8.jpg))
```text
$ ./cobol/bin/payment_post TXN-XX-0003 100001 0.00 USD XX-RC8
(paste exact output)
$ echo $?
8
```

### Return code 12 — environment failure, wrong folder ([cobol_rc12.jpg](screenshots/cobol_rc12.jpg))
```text
$ cd ~ && /opt/balerica-bank/cobol/bin/account_lookup 100001
(paste exact output — expect ERROR=CANNOT OPEN data/accounts.dat / FILE-STATUS=35)
$ echo $?
12
```

### Alice's balance decoded by hand ([cobol_ledger_decode.jpg](screenshots/cobol_ledger_decode.jpg))
```text
$ grep '^100001' data/accounts.dat | cut -c45-56
(paste — e.g. 000000500000)
```
Columns 45–56 are `PIC 9(10)V99` → the last two digits are cents → **Alice's balance = ________**

### Journal lines for my TXN IDs
```text
$ grep 'TXN-XX-' data/payments.dat
(paste exact lines)
```
**Did the balance change?** ____
_(Expected: no — `payment_post` only reads the ledger and appends to the journal; balances are deducted only via the API's `POST /payments`, which updates SQLite and re-exports accounts.dat. RC 12 wrote no journal line.)_

---

## Mistakes I made
- 
- 
- 

## Commands I now know by heart
- `whoami && TZ='America/New_York' date && ec2-metadata -i && uptime -s`
- `ssh -i key.pem ec2-user@<public-dns>`
- `git clone https://github.com/BalericaAI/SEIR-Foundations.git`
- `cd /opt/balerica-bank && source venv/bin/activate`
- `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- `echo $?`
- `cut -c45-56 data/accounts.dat`
- 
