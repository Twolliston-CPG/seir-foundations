# Lab 1 Notes — lesson1_ec2 (Balerica Legacy Bank)

**Name:** _________ · **Initials for TXN IDs:** XX · **Time zone:** America/New_York

> Each run: start with run number + Instance ID, write **at least 3 sentences** (what changed, errors hit and fixes, what I newly understood), and paste **at least one exact output line** only that run would have (e.g. the uvicorn `Started server process [PID]` line, or a real error message).

---

## Run 1 — Instance ID: `i-________________`

- **Date / time:** ____ · **Boot time (UTC):** ____ · **Public DNS:** ____
- **Screenshot:** [lab1_run1.jpg](screenshots/lab1_run1.jpg)

**What changed this run:**
_(e.g. first time through; followed the runbook line by line.)_

**Errors hit and how I fixed them:**
_(e.g. `ec2-metadata: command not found` → ran `sudo dnf install -y ec2-utils`.)_

**What I newly understood:**
_(e.g. why the venv must be activated in each terminal.)_

**Exact output line only this run would have:**
```text
INFO:     Started server process [_____]
```

---

## Run 2 — Instance ID: `i-________________`

- **Date / time:** ____ · **Boot time (UTC):** ____ · **Public DNS:** ____
- **Screenshot:** [lab1_run2.jpg](screenshots/lab1_run2.jpg)

**What changed this run:**

**Errors hit and how I fixed them:**

**What I newly understood:**

**Exact output line only this run would have:**
```text

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
