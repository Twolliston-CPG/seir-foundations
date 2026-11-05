# Lesson 2 Homework — Seven Alerts, Seven Wins

In class, your EC2 instance sent its first message to Slack. This week you
send seven more, each one a small script you run yourself. By script seven
you will have written a monitoring report generator — the real thing, not a
toy. If you completed the lab, **you can already do all of this.**

> **A word about impostor syndrome:** you watched this work in class and some
> of you still think it was luck, or magic, or someone else's skill. It wasn't.
> The whole point of these seven scripts is that YOU run them, YOU see them
> arrive, seven separate times, until your own evidence outvotes your doubt.
> Nobody is born knowing webhooks. Every senior engineer once stared at a
> terminal thinking "there's no way this works." Then it did. Run the scripts.

## 0. Prerequisites

- The lab is complete: `python slack.py --test` prints
  `SUCCESS: Chewbacca approves!` and you SAW the alert in `#balerica-alerts`.
- You know the nano save dance: `Ctrl+O`, `Enter`, `Ctrl+X` (see `nano_basics.md`).

## 1. One-time setup (about 2 minutes)

**Step 1 — Copy the homework scripts next to `slack.py`.** They import
`send_alert` from `slack.py`, so they must live in the same folder:

```bash
cd ~/SEIR-Foundations && git pull
cp ~/SEIR-Foundations/module1/lesson2_slack/homework/hw*.py /opt/balerica-bank/
cd /opt/balerica-bank
ls hw*.py
```

Expected output:

```text
hw1_hello_slack.py  hw3_server_time.py  hw5_load_check.py    hw7_morning_report.py
hw2_severity_tour.py  hw4_disk_watch.py  hw6_incident_drill.py
```

**Step 2 — Lower your alert threshold for homework.** Most homework alerts are
INFO, and your `.env` from class filters below ERROR. Edit it:

```bash
nano .env
```

Change this line:

```dotenv
SLACK_ALERT_SEVERITY=INFO
```

Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`). This is itself the lesson:
**configuration changes behavior without touching code.**

**Step 3 — Activate the venv** (every new SSH session needs this):

```bash
cd /opt/balerica-bank
source venv/bin/activate
```

## 2. The seven scripts — run them in order

| # | Date | Instance ID | Public DNS | Script | Run | What it teaches |
|---|------|-------------|------------|--------|-----|-----------------|
| 1 | 11.05.2026 1:37:21 am | i-08c65a72965755bed | ec2-3-89-228-59.compute-1.amazonaws.com | [`hw1_hello_slack.py`](screenshots/lesson2_slack_hw1.jpg) | `python hw1_hello_slack.py` | Calling `send_alert()` with your own words (edit `MY_NAME` first — nano!) |
| 2 | 11.05.2026 11:27:58| i-0e3df50b16b502ec2 |ec2-3-90-164-37.compute-1.amazonaws.com | [`hw2_severity_tour.py`](screenshots/lesson2_slack_hw2.a.jpg)[`B.`](screenshots/lesson2_slack_hw2.a.jpg) | `python hw2_severity_tour.py` | All four severities and how the `.env` threshold filters them |
| 3 | 11.05.2026 4:29 PM EST | i-086544e950c0de391 | ec2-54-226-203-251.compute-1.amazonaws.com | [`hw3_server_time.py`](screenshots/lesson2_slack_hw3.jpg) | `python hw3_server_time.py` | Timestamps, and why servers speak UTC |
| 4 | | | | `hw4_disk_watch.py` | `python hw4_disk_watch.py` | A REAL monitor: measure disk, choose severity with if/else |
| 5 | | | | `hw5_load_check.py` | `python hw5_load_check.py` | CPU load average, comparing against a limit |
| 6 | | | | `hw6_incident_drill.py` | `python hw6_incident_drill.py` | Randomized (fake) bank incidents — run it 2–3 times |
| 7 | | | | `hw7_morning_report.py` | `python hw7_morning_report.py` | Capstone: one multi-line report combining everything |

Each script prints what happened in the terminal AND tells you what to look
for in Slack. Read the source of every script before you run it — they are
short on purpose. If any line confuses you, ask Claude Code to explain that
line (not to rewrite the script).

## 3. Experiments that turn runners into engineers

After all seven work, prove you understand the system by predicting, then
testing:

1. Set `SLACK_ALERT_SEVERITY=CRITICAL` in `.env` and rerun script 2.
   **Predict first:** how many of the four messages will arrive?
2. Set `SLACK_ALERTS_ENABLED=false` and run script 1. What happens, and why
   is a kill switch like this useful during maintenance windows?
3. Open `hw4_disk_watch.py` in nano and change the WARNING threshold from 75
   to a number below your current disk usage. Rerun. Did the severity change?
4. Put everything back: `SLACK_ALERT_SEVERITY=INFO`, `SLACK_ALERTS_ENABLED=true`.

## 4. Rules

- **Synthetic messages only.** Never send real passwords, keys, customer
  data, or anything from `.env` to Slack. (Script 6 is clearly marked DRILL.)
- **Don't spam.** Each script sends at most a handful of messages. Running
  the set a few times is fine; a loop firing hundreds of alerts is how real
  teams get paged at dinner and how webhooks get revoked.
- **Keep the interface sacred.** If you edit scripts (encouraged!), keep
  calling `send_alert(agent, severity, message, incident_id)` exactly as is.

## 5. Evidence of completion

Add to your homework repo (same repo and format as previous weeks):

- One screenshot of `#balerica-alerts` showing **at least five different
  homework alerts**, sensitive info hidden.
- One screenshot of your terminal running `hw7_morning_report.py` with the
  ID line from Lesson 1 (`whoami && TZ='Your/Zone' date && ec2-metadata -i`).
- In your notes: answers to the "In your notes:" question each script prints,
  plus your prediction-vs-result from experiment 1.

> **Chewbacca's encouragement:** RRRRAAAWWWRRR! Seven scripts. Seven alerts.
> Seven pieces of proof that it was never magic — it was you. Now the doubt
> can go find someone else to bother.

---

## 6. Notes

### hw1 — Hello from EC2

_Notes:_
The MY_NAME Variable was set to MY_NAME = "Tim Wolliston". this was pretty straight forward.

### hw2 — Which severities arrived, and WHY those?

_Answer:_
When SLACK_ALERT_SEVERITY is set to "INFO" info and errors level messages are sent to slack.

```text
INFO     -> DELIVERED to Slack
WARNING  -> DELIVERED to Slack
ERROR    -> DELIVERED to Slack
CRITICAL -> DELIVERED to Slack
```
When SLACK_ALERT_SEVERITY is set to "ERROR" info messages level are suppressed and only the error messages are sent to slack. These errors were sent to slack.

```text
ERROR    -> DELIVERED to Slack
CRITICAL -> DELIVERED to Slack
```

### hw3 — How many hours apart are server time and YOUR wall clock?

_Answer:_
The Server UTC time for this run was 21:30:58 UTC my local time is 16:30:30
making them 5 hours apart

### hw4 — Why is a quiet INFO here GOOD design, not a failure?

_Answer:_

### hw5 — What would make this number spike on the Balerica bank?

_Answer:_

### hw6 — Which of these fake incidents deserves to wake a human at 3 AM?

_Answer:_

### Section 3, Experiment 1 — Prediction vs result (SLACK_ALERT_SEVERITY=CRITICAL, rerun hw2)

_Prediction:_

_Result:_
