# SEIR Foundations — Module 1, Lesson 1 Homework

## Balerica Legacy Bank: Repeat It, Break It (Safely), Research It

**Course:** SEIR Foundations  
**Lesson:** Module 1 / Lesson 1 — EC2 + Balerica Legacy Bank (FastAPI with a COBOL core)  
**Difficulty:** Beginner  
**Format:** Individual homework + spotter check-in + optional "Be A Man" extra credit  
**Homework deadline:** **Tuesday, November 3, 2026, at 12:00 PM Central Time** (1:00 PM Eastern / 10:00 AM Pacific / 6:00 PM London)  
**Submission methods:** Send to the SEIR Foundations FB chat, or to Theo via FB DM or email  
**Reference course:** Stéphane Maarek's AWS Udemy course  
**Lab runbook:** [Balerica Legacy Bank — Student Runbook](https://github.com/BalericaAI/SEIR-Foundations/blob/main/module1/lesson1_ec2/API/runbook.md)

> **Chewbacca's message:** RRRRAAAWWWRRR! Once is luck. Seven times is skill. Run the bank until your fingers know the way.

---

## 1. Purpose

In class, most of you reached **Step 4** of the runbook: the COBOL core is compiled and the FastAPI server is running. This week you will:

- **Repeat** Steps 0–4 seven times, on seven fresh EC2 instances, across at least three days, until the process is muscle memory.
- **Practice** talking directly to the COBOL core and reading its return codes.
- **Clone your own homework repo** onto an EC2 instance.
- **Research** databases, COBOL, SWIFT, and APIs — the four building blocks of the bank you just ran — using reading, video, and AI.
- **(Optional)** Explore beyond Step 4: connect Bedrock, bake the lab into your launch template, and build a golden AMI.

**Why this matters for next week:** the next lab turns Balerica AI into a platform with FastAPI (`app.py`). You will see `GET` vs `POST`, JSON request bodies, Pydantic validation, and the `/docs` console. The API research below prepares you for that.

&nbsp;

> ⚠️⚠️⚠️ **WARNING: THE SCREENSHOT DAILY LIMIT IS STRICT** ⚠️⚠️⚠️
>
> 🚨 **No more than 3** of your 7 lab-run screenshots may show the same date (your local time). **4 or more on the same date is an AUTOMATIC FAILURE FOR THIS WEEK.** 🚨
>
> 📅 That means you need **at least 3 separate days**. Start early. Waiting until Monday night means you cannot pass.

&nbsp;

---

## 2. Folder structure (required)

Add this folder to your existing homework repo (same repo and format as Lab 0.5 — see [Aaron's example HW Repo](https://github.com/aaron-dm-mcdonald/seir-foundations-homework)).

```
seir-foundations-homework/
└── module1/
    ├── lab0_basics/
    ├── lab0.5_basics_contd/
    └── lesson1_ec2/
        ├── README.md                      (your evidence tables — Sections 3 and 9)
        ├── lab1_notes.md                  (your personal notes)
        ├── ai_review_YourNameHere.txt
        ├── ai_review_transcript_YourNameHere.txt   (only if you did not use a share link)
        ├── spotter_YourNameHere.txt
        ├── AI_enabled_study_lab1.0.txt
        └── screenshots/
            ├── lab1_run1.jpg  …  lab1_run7.jpg
            ├── Maarek_Section21_quiz.jpg
            ├── Maarek_Section23_quiz.jpg
            ├── Maarek_Section25_quiz.jpg
            ├── cobol_rc0.jpg
            ├── cobol_rc4.jpg
            ├── cobol_rc8.jpg
            ├── cobol_rc12.jpg
            ├── cobol_ledger_decode.jpg
            ├── git_clone.jpg
            ├── BAM_2.1.jpg      (extra credit)
            ├── BAM_2.2.jpg      (extra credit)
            └── BAM_2.3.jpg      (extra credit)
```

Replace `Tim Wolliston` with your name. Use these file names exactly — they are how your work gets checked.

---

## 3. Required — Complete the lab seven times

### 3.1 What counts as one run

One run = **one brand-new EC2 instance** taken from launch through **Step 4** of the runbook (Steps 0, 1, 2, 3, 4), done by hand.

- Launch from your saved launch template (or the console), SSH in, and follow the runbook.
- Instances built from a baked launch template or a golden AMI (BAM_2.2 / BAM_2.3) **do not count** toward the seven. The point is to do the steps yourself.
- When the run is done: `Ctrl+C` the server, **terminate the instance**, and check **EC2 → Volumes** and **Elastic IPs** for leftovers. **Keep your launch template.**

### 3.2 What the screenshot must show — the ID line

Right **before** you start uvicorn in Step 4, run the **ID line**. It proves who you are, when you ran it (in your own time zone), which instance you are on, and when that instance booted:

```bash
whoami && TZ='America/Chicago' date && ec2-metadata -i && uptime -s
```
Optional alternative:

```bash
 clear && seir-dashboard && whoami && timedatectl show -p Timezone --value && date && ec2-metadata -i && curl -s http://checkip.amazonaws.com && uptime -p && TZ=UTC who -b 
 ```

- Use your own zone: `America/New_York`, `America/Chicago`, `America/Denver`, `America/Los_Angeles`, `Europe/London`, etc. (Amazon Linux shows UTC by default.)
- `ec2-metadata -i` prints the **Instance ID**. If the command is missing, run `sudo dnf install -y ec2-utils` first.
- `uptime -s` prints when the instance **booted** (in UTC).

**Every screenshot in this homework must include the ID line** — lab runs, COBOL practice, git clone, and BAM.

Then start the server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Optional: 
Use below option only if you've made the necessary configuration changes to your aws account allowing for AWS Bedrock to be reached.

```bash
BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-6 AWS_REGION=us-east-1 uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Take the screenshot when you see [`Application startup complete.`](screenshots/application_startup_complete.jpg) It must show, in one image:

1. The full ID line output: `ec2-user`, the local date and time, the Instance ID, and the boot time
2. The uvicorn startup lines, including `Application startup complete.`

Save as `screenshots/lab1_run1.jpg` through `screenshots/lab1_run7.jpg`.

### 3.3 Daily limit

| Rule | Result |
|------|--------|
| 1–3 lab-run screenshots on the same local date | OK |
| **4 or more** lab-run screenshots on the same local date | **Automatic failure** for the week |
| The date in the screenshot does not match the date in your table | That run does not count |
| The Instance ID in the screenshot does not match the Instance ID in your table | That run does not count |
| The boot time is after the screenshot time, or more than 24 hours before it | That run does not count |
| Two runs share the same Public DNS / Instance ID | Only one of them counts |
| Your Instance ID appears in another student's submission | Both submissions are reviewed by Theo |

The daily limit applies **only** to the seven `lab1_run` screenshots. COBOL practice, git clone, quiz, and BAM screenshots do not count toward it.

### 3.4 Evidence table (put this in your [`lesson1_ec2/README.md`](module1/lesson1_ec2/readme.md))

Find the **Public IPv4 DNS** and **Instance ID** in **EC2 → Instances → (your instance) → Details**.


| Run | Date      | Time zone | Instance ID    | Boot time (UTC)    | Public IPv4 DNS | Screenshot | Terminated? |
|-----|-----------|-----------|----------------|--------------------|-------------------------------------------------|------------|-------------|
| 1 | 2026-10-29 | America/New_York | i-06bac9d9f7b16c1ed | 2026-10-29 12:43:00 | ec2-54-197-24-174.compute-1.amazonaws.com | [lab1_run1.jpg](screenshots/lab1_run1.jpg) | Yes |
| 2 |2026-10-29 | | i-03654eddcd51d549f | 2026-10-29 15:15:00| | [lab1_run2.jpg](screenshots/lab1_run2.jpg) | |
| 3 | 2026-10-29| America/New_York |i-0d8a2c7ba9fd28649 |2026-10-29 16:45:00 |ec2-54-163-49-37.compute-1.amazonaws.com | [lab1_run3.jpg](screenshots/lab1_run3.jpg) | |
| 4 |2026-11-01 |America/New_York |i-035d7e71aca00a5a0 |2026-11-01 20:49 |ec2-100-55-46-159.compute-1.amazonaws.com | [lab1_run4.jpg](screenshots/lab1_run4.jpg) | |
| 5 | 2026-11-01|America/New_York |i-0f8eb643ba9d52a6b |2026-11-01 21:39 |ec2-107-21-165-40.compute-1.amazonaws.com | [lab1_run5.jpg](screenshots/lab1_run5.jpg) | |
| 6 |2026-11-01 |America/New_York |i-02ce7e8c9b2b58d5b |2026-11-01 22:10 |ec2-18-215-152-252.compute-1.amazonaws.com | [lab1_run6.jpg](screenshots/lab1_run6.jpg) | |
| 7 | 2026-11-02|America/New_York |i-0ec5903c2839f1edf |2026-11-02 17:15  | | [lab1_run7.jpg](screenshots/lab1_run7.jpg) | |


(Row 1 is an example — replace it with your real values. The Instance ID and boot time must match your screenshot exactly. Boot time is in UTC, so in the evening in the US it may already show the next calendar day — that is expected.)

### 3.5 Personal notes — [`lab1_notes.md`](module1/lesson1_ec2/LAB1_NOTES.md)

For **each run**, start with the run number and Instance ID, then write at least **3 sentences**:

- What went differently this time?
- What error (if any) did you hit, and what fixed it?
- What did you understand this time that you did not understand before?

Also paste **at least one exact output line from that run** that only your run would have, such as the PID from [`Started server process [12345]`](screenshots/step4-uvicorn-running.png), or an error message you actually got.

End the file with a **"Mistakes I made"** list (at least 3 items) and a **"Commands I now know by heart"** list.

---

## 4. Required — Maarek quizzes

| Section | Deliverable |
|---------|-------------|
| Section 21 | Screenshot of the **completed** quiz, uploaded as [`Maarek_Section21_quiz.jpg`](screenshots/Maarek_section21_quiz.jpg) |
| Section 23 | Screenshot of the **completed** quiz, uploaded as [`Maarek_Section23_quiz.jpg`](screenshots/Maarek_section23_quiz.jpg) |
| Section 25 | Screenshot of the **completed** quiz, uploaded as [`Maarek_Section25_quiz.jpg`](screenshots/Maarek_section25_quiz.jpg) |

---

## 5. Required — [`ai_review_tim_wolliston.txt]`(https://github.com/Twolliston-CPG/seir-foundations/blob/main/module1/lesson1_ec2/ai_review_tim_wolliston.txt)

Review the Lesson 1 runbook with the AI of your choice (Claude, ChatGPT, Gemini, etc.). Ask it to explain the parts you did not fully understand.

**You must submit the real conversation**, in one of two ways:

- A **share link** to the conversation (most AI apps have a "Share" button), pasted at the top of the file, **or**
- An **exported or copy-pasted transcript**, uploaded as `ai_review_transcript_tim_wollitston.txt`(https://github.com/Twolliston-CPG/seir-foundations/blob/main/module1/lesson1_ec2/ai_review_transcript_tim_wolliston.txt) (or `.pdf`).

Your summary must match the conversation. The most important part, and what is graded most heavily, is **how you checked** each answer.

Use this format:

```
AI used = BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-6 
Conversation share link = (https://github.com/Twolliston-CPG/seir-foundations/blob/main/module1/lesson1_ec2/ai_review_transcript_tim_wolliston.txt) [`or see ai_review_transcript_tim_wolliston`](module1/lesson1_ec2/ai_review_transcript_tim_wolliston.txt)

Q1: ("Please review with me this runbook:
  https://github.com/BalericaAI/SEIR-Foundations/blob/main/module1/lesson1_ec2/API/runbook.md. explain
  for me what are the necesarry step needed for AWS Bedrocks anthropic model to return a answer to
  {"question": "What does return code 8 mean?"} found in step8.Be as clear and percise as much as
  possible. Step by step intructions are welcomed. place your explanation in this file
  module1/lesson1_ec2/ai_review_tim_wolliston.txt")
AI's answer, in my own words:

There are three requirements
1 — IAM Role with Bedrock Permission attached to the EC2 instance
2 — AWS_REGION matches where you enabled Bedrock model access
3 — BEDROCK_MODEL_ID is set to a valid model or inference-profile ID

After which follow the enhanced startup procedure

How I checked it (I asked ai to produce the commands and make the necessary configuration afterwhich I logged into my AWS account and reviwed all the changes ai made on my behalf. 

ran a command, re-read the runbook, asked my spotter, etc.):

(minimum 5 questions)

Q2: ...
### YOU - 2026-10-28 23:24:02 UTC

does iamadmin have access to amazon bedrock?

### COMMAND / TOOL CALL (Bash) - 2026-10-28 23:24:04 UTC

```bash
which aws && aws sts get-caller-identity 2>&1; aws iam list-attached-user-policies --user-name iamadmin 2>&1; aws iam list-groups-for-user --user-name iamadmin 2>&1
```

### OUTPUT - 2026-10-28 23:24:07 UTC

```text
/usr/local/bin/aws
{
    "UserId": "<AWS-UNIQUE-ID>",
    "Account": "<AWS-ACCOUNT-ID>",
    "Arn": "arn:aws:iam::<AWS-ACCOUNT-ID>:user/AWSCLI"
}
{
    "AttachedPolicies": [
        {
            "PolicyName": "AdministratorAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/AdministratorAccess"
        }
    ]
}
{
    "Groups": []
}
```

Q3: ...
### YOU - 2026-10-28 23:25:12 UTC

Check if an SCP blocks Bedrock

### COMMAND / TOOL CALL (Bash) - 2026-10-28 23:25:13 UTC

```bash
aws organizations describe-organization 2>&1 | head -20; echo ---; aws organizations list-policies-for-target --target-id <AWS-ACCOUNT-ID> --filter SERVICE_CONTROL_POLICY 2>&1 | head -20
```

### OUTPUT - 2026-10-28 23:25:15 UTC

```text
aws: [ERROR]: An error occurred (AWSOrganizationsNotInUseException) when calling the DescribeOrganization operation: Your account is not a member of an organization.
---

aws: [ERROR]: An error occurred (AWSOrganizationsNotInUseException) when calling the ListPoliciesForTarget operation: Your account is not a member of an organization.
```

### CLAUDE - 2026-10-28 23:25:17 UTC

No SCP blocks Bedrock, because account `<AWS-ACCOUNT-ID>` isn't part of an AWS Organization. Both Organizations calls returned `AWSOrganizationsNotInUseException`, so no SCPs apply.

The IAM side was already clear, since `iamadmin` has `AdministratorAccess` and no permissions boundary. The one thing left is Bedrock model access. Some models, such as the Anthropic ones, may need first-time access or use-case approval in the Bedrock console. Running `aws bedrock list-foundation-models --region us-east-1` will show what's available.



Q4: ...
### YOU - 2026-10-28 23:25:47 UTC

Check which Bedrock models are available

### COMMAND / TOOL CALL (Bash) - 2026-10-28 23:25:49 UTC

```bash
aws bedrock list-foundation-models --region us-east-1 --query 'modelSummaries[].[providerName,modelId]' --output text 2>&1 | sort | head -150; echo ---; aws bedrock list-inference-profiles --region us-east-1 --query 'inferenceProfileSummaries[?contains(inferenceProfileId,`anthropic`)].inferenceProfileId' --output text 2>&1 | tr '\t' '\n' | head -40
```

### OUTPUT - 2026-10-28 23:25:51 UTC

```text
AI21 Labs	ai21.jamba-1-5-large-v1:0
AI21 Labs	ai21.jamba-1-5-mini-v1:0
Amazon	amazon.nova-2-5-sonic
Amazon	amazon.nova-2-lite-v1:0
Amazon	amazon.nova-2-lite-v1:0:256k
Amazon	amazon.nova-2-multimodal-embeddings-v1:0
Amazon	amazon.nova-2-sonic-v1:0
Amazon	amazon.nova-lite-v1:0
Amazon	amazon.nova-lite-v1:0:24k
Amazon	amazon.nova-lite-v1:0:300k
Amazon	amazon.nova-micro-v1:0
Amazon	amazon.nova-micro-v1:0:128k
Amazon	amazon.nova-micro-v1:0:24k
Amazon	amazon.nova-pro-v1:0
Amazon	amazon.nova-pro-v1:0:24k
Amazon	amazon.nova-pro-v1:0:300k
Amazon	amazon.titan-embed-g1-text-02
Amazon	amazon.titan-embed-image-v1
Amazon	amazon.titan-embed-image-v1:0
Amazon	amazon.titan-embed-text-v1
Amazon	amazon.titan-embed-text-v1:2:8k
Amazon	amazon.titan-embed-text-v2:0
Amazon	amazon.titan-embed-text-v2:0:8k
Anthropic	anthropic.claude-fable-5
Anthropic	anthropic.claude-fable-5-1
Anthropic	anthropic.claude-haiku-4-5-20251001-v1:0
Anthropic	anthropic.claude-haiku-5-5
Anthropic	anthropic.claude-opus-4-1-20250805-v1:0
Anthropic	anthropic.claude-opus-4-5-20251101-v1:0
Anthropic	anthropic.claude-opus-4-6-v1
Anthropic	anthropic.claude-opus-4-7
Anthropic	anthropic.claude-opus-4-8
Anthropic	anthropic.claude-opus-5
Anthropic	anthropic.claude-opus-5-5
Anthropic	anthropic.claude-sonnet-4-5-20250929-v1:0
Anthropic	anthropic.claude-sonnet-4-6
Anthropic	anthropic.claude-sonnet-5
Anthropic	anthropic.claude-sonnet-5-5
Cohere	cohere.embed-english-v3
Cohere	cohere.embed-english-v3:0:512
Cohere	cohere.embed-multilingual-v3
Cohere	cohere.embed-multilingual-v3:0:512
Cohere	cohere.embed-v4:0
Cohere	cohere.rerank-v3-5:0
DeepSeek	deepseek.r1-v1:0
DeepSeek	deepseek.v3.2
Google	google.gemma-3-12b-it
Google	google.gemma-3-27b-it
Google	google.gemma-3-4b-it
Meta	meta.llama3-1-70b-instruct-v1:0
Meta	meta.llama3-1-8b-instruct-v1:0
Meta	meta.llama3-3-70b-instruct-v1:0
Meta	meta.llama3-70b-instruct-v1:0
Meta	meta.llama3-8b-instruct-v1:0
Meta	meta.llama4-maverick-17b-instruct-v1:0
Meta	meta.llama4-scout-17b-instruct-v1:0
MiniMax	minimax.minimax-m2
MiniMax	minimax.minimax-m2.1
MiniMax	minimax.minimax-m2.5
Mistral AI	mistral.devstral-2-123b
Mistral AI	mistral.magistral-small-2509
Mistral AI	mistral.ministral-3-14b-instruct
Mistral AI	mistral.ministral-3-3b-instruct
Mistral AI	mistral.ministral-3-8b-instruct
Mistral AI	mistral.mistral-7b-instruct-v0:2
Mistral AI	mistral.mistral-large-2402-v1:0
Mistral AI	mistral.mistral-large-3-675b-instruct
Mistral AI	mistral.mistral-small-2402-v1:0
Mistral AI	mistral.mixtral-8x7b-instruct-v0:1
Mistral AI	mistral.pixtral-large-2502-v1:0
Mistral AI	mistral.voxtral-mini-3b-2507
Mistral AI	mistral.voxtral-small-24b-2507
Moonshot AI	moonshot.kimi-k2-thinking
Moonshot AI	moonshotai.kimi-k2.5
Moonshot AI	moonshotai.kimi-k3
NVIDIA	nvidia.nemotron-nano-12b-v2
NVIDIA	nvidia.nemotron-nano-3-30b
NVIDIA	nvidia.nemotron-nano-9b-v2
NVIDIA	nvidia.nemotron-super-3-120b
OpenAI	openai.gpt-5.4
OpenAI	openai.gpt-5.5
OpenAI	openai.gpt-5.6-luna
OpenAI	openai.gpt-5.6-sol
OpenAI	openai.gpt-5.6-terra
[... 2568 more characters omitted from this tool result ...]
```

### CLAUDE - 2026-10-28 23:25:57 UTC

Bedrock lists about 110 foundation models in `us-east-1`, from 17 providers. This is the catalog of models offered in the region, as a signed-in user sees it. It doesn't prove each model is enabled for your account. To confirm that, run one `bedrock-runtime invoke-model` call against the model you want.

| Provider | Models |
|---|---|
| **Anthropic** | Fable 5 and 5.1; Opus 4.1, 4.5, 4.6, 4.7, 4.8, 5 and 5.5; Sonnet 4.5, 4.6, 5 and 5.5; Haiku 4.5 and 5.5 |
| **Amazon** | Nova 2 Lite, Nova Lite, Nova Micro, Nova Pro, Nova 2 Sonic, plus Titan and Nova embedding models |
| **OpenAI** | GPT-5.4, 5.5 and 5.6 variants; GPT-6 and 6.1 variants; gpt-oss 120b and 20b (and the safeguard versions) |
| **Meta** | Llama 3, 3.1 and 3.3; Llama 4 Maverick and Scout |
| **Mistral AI** | Mistral Large 3, Devstral 2, Magistral, Ministral, Pixtral, Voxtral, Mixtral and Mistral 7B |
| **Others** | AI21 Jamba, Cohere (embeddings and rerank), DeepSeek (R1, V3.2), Google Gemma 3, MiniMax, Moonshot Kimi, NVIDIA Nemotron, Qwen, Stability AI image tools, TwelveLabs, Writer Palmyra, Z.AI GLM, xAI Grok |

Most newer Anthropic models can't be called by their bare model ID. They need an inference profile, so use the `us.` or `global.` prefix (for example `us.anthropic.claude-sonnet-5-5` or `global.anthropic.claude-opus-5-5`). Profiles exist for most of the Anthropic list. I only listed profiles for Anthropic, so check the others separately if you need them.

I only checked `us-east-1`, so other regions may differ.

Q5: ...

### YOU - 2026-10-28 23:26:04 UTC

Test invoking Claude Sonnet 5.5 on Bedrock

### COMMAND / TOOL CALL (Bash) - 2026-10-28 23:26:06 UTC

```bash
cd /tmp && aws bedrock-runtime converse --region us-east-1 --model-id us.anthropic.claude-sonnet-5-5 --messages '[{"role":"user","content":[{"text":"Reply with the single word: pong"}]}]' --inference-config '{"maxTokens":20}' --query '{text:output.message.content[0].text,stop:stopReason,usage:usage}' 2>&1
```

### OUTPUT - 2026-10-28 23:26:08 UTC

```text
Exit code 254

aws: [ERROR]: An error occurred (AccessDeniedException) when calling the Converse operation: anthropic.claude-sonnet-5-5 is not available for this account. You can explore other available models on Amazon Bedrock. For additional access options, contact AWS Sales at https://aws.amazon.com/contact-us/sales-support/
```

### CLAUDE - 2026-10-28 23:26:12 UTC

The invocation failed with `AccessDeniedException: anthropic.claude-sonnet-5-5 is not available for this account`.

- **Not an IAM problem:** The call was signed as the `AWSCLI` user, not `iamadmin`. Neither is the cause, since `AdministratorAccess` allows the action and no SCP applies. The error is Bedrock refusing the model for this account, so the model isn't enabled for it.
- **Likely fixes:** In the Bedrock console, open Model access (or the model catalog) for `us-east-1`. Request or enable Anthropic's models, and submit the first-time use-case form if it asks. New or recently created accounts are sometimes restricted from newer models until they have billing history. If it still says unavailable after enabling, the AWS Sales contact in the error message is the remaining route.
- **Other models:** I can test other Anthropic models, such as Haiku 4.5 or Sonnet 4.5, to see whether the whole Anthropic family is blocked or just this one. Running the test again as `iamadmin` isn't needed to answer that.

Do you want me to run those tests?

### YOU - 2026-10-28 23:26:54 UTC

does this iamadmin user have acess to aws bedrock?

### CLAUDE - 2026-10-28 23:26:58 UTC

Yes for permissions, but model access is a separate question, and Sonnet 5.5 is currently blocked.

- **Permissions:** `iamadmin` has `AdministratorAccess`, no permissions boundary and no SCP, and the policy simulator showed `bedrock:InvokeModel` as allowed. IAM won't stop it from using Bedrock.
- **Models:** The Sonnet 5.5 call failed with "not available for this account". That block is on the account, so `iamadmin` would hit it too.
- **What I haven't tested:** I never made a call as `iamadmin`. My CLI is signed in as `AWSCLI`, and I judged `iamadmin` only from its policies. To test it directly, run the call with `iamadmin`'s credentials or profile.

I haven't tried any other model, so I can't say whether anything else on Bedrock is usable from this account yet.

### YOU - 2026-10-28 23:27:17 UTC

Test invoking Claude Haiku 4.5 on Bedrock

### COMMAND / TOOL CALL (Bash) - 2026-10-28 23:27:18 UTC

```bash
cd /tmp && aws bedrock-runtime converse --region us-east-1 --model-id us.anthropic.claude-haiku-4-5-20251001-v1:0 --messages '[{"role":"user","content":[{"text":"Reply with the single word: pong"}]}]' --inference-config '{"maxTokens":20}' --query '{text:output.message.content[0].text,stop:stopReason,usage:usage}' 2>&1
```

### OUTPUT - 2026-10-28 23:27:20 UTC

```text
{
    "text": "pong",
    "stop": "end_turn",
    "usage": {
        "inputTokens": 15,
        "outputTokens": 5,
        "totalTokens": 20,
        "cacheReadInputTokens": 0,
        "cacheWriteInputTokens": 0
    }
}
Shell cwd was reset to /Users/Twolliston/Documents/TheoWAF/seir-foundations
```

### CLAUDE - 2026-10-28 23:27:22 UTC

Haiku 4.5 works on Bedrock. The call to `us.anthropic.claude-haiku-4-5-20251001-v1:0` in `us-east-1` returned `pong` (15 input tokens, 5 output).

Anthropic access on this account is therefore not blocked as a whole, and only Sonnet 5.5 was refused. The call ran as the `AWSCLI` user, not `iamadmin`.

I can test the other models you care about, such as Sonnet 4.5, Sonnet 4.6, Opus 4.5 or Haiku 5.5, to see which ones are enabled and which are blocked like Sonnet 5.5.

### YOU - 2026-10-28 23:27:45 UTC

Test invoking Claude Sonnet 4.5 on Bedrock

### COMMAND / TOOL CALL (Bash) - 2026-10-28 23:27:46 UTC

```bash
cd /tmp && aws bedrock-runtime converse --region us-east-1 --model-id us.anthropic.claude-sonnet-4-5-20250929-v1:0 --messages '[{"role":"user","content":[{"text":"Reply with the single word: pong"}]}]' --inference-config '{"maxTokens":20}' --query '{text:output.message.content[0].text,stop:stopReason,usage:usage}' 2>&1
```

### OUTPUT - 2026-10-28 23:27:49 UTC

```text
{
    "text": "pong",
    "stop": "end_turn",
    "usage": {
        "inputTokens": 15,
        "outputTokens": 5,
        "totalTokens": 20,
        "cacheReadInputTokens": 0,
        "cacheWriteInputTokens": 0
    }
}
Shell cwd was reset to /Users/Twolliston/Documents/TheoWAF/seir-foundations
```

### CLAUDE - 2026-10-28 23:27:51 UTC

Sonnet 4.5 works on Bedrock. The call to `us.anthropic.claude-sonnet-4-5-20250929-v1:0` in `us-east-1` returned `pong` (15 input tokens, 5 output). It ran as the `AWSCLI` user, as before.

Results so far:

| Model | Result |
|---|---|
| Haiku 4.5 | Works |
| Sonnet 4.5 | Works |
| Sonnet 5.5 | Blocked: "not available for this account" |

The 4.5 models work and the newer 5.5 one is blocked. The block may cover the newer 5.x family, but I've only tested Sonnet 5.5. I can test Sonnet 5, Haiku 5.5, Opus 5.5 and Sonnet 4.6 to see where the line falls.

### YOU - 2026-10-28 23:27:56 UTC

Test invoking Claude Haiku 5.5 on Bedrock

### COMMAND / TOOL CALL (Bash) - 2026-10-28 23:27:57 UTC

```bash
cd /tmp && aws bedrock-runtime converse --region us-east-1 --model-id us.anthropic.claude-haiku-5-5 --messages '[{"role":"user","content":[{"text":"Reply with the single word: pong"}]}]' --inference-config '{"maxTokens":20}' --query '{text:output.message.content[0].text,stop:stopReason,usage:usage}' 2>&1
```

### OUTPUT - 2026-10-28 23:27:58 UTC

```text
Exit code 254

aws: [ERROR]: An error occurred (AccessDeniedException) when calling the Converse operation: anthropic.claude-haiku-5-5 is not available for this account. You can explore other available models on Amazon Bedrock. For additional access options, contact AWS Sales at https://aws.amazon.com/contact-us/sales-support/
```

### CLAUDE - 2026-10-28 23:28:01 UTC

Haiku 5.5 is blocked the same way as Sonnet 5.5. The error was `AccessDeniedException: anthropic.claude-haiku-5-5 is not available for this account`.

| Model | Result |
|---|---|
| Haiku 4.5 | Works |
| Sonnet 4.5 | Works |
| Sonnet 5.5 | Blocked |
| Haiku 5.5 | Blocked |

The pattern points to the 5.x family being unavailable to this account, while the 4.5 models work. I haven't tested the other 5.x models (Sonnet 5, Opus 5, Opus 5.5, Fable 5 and 5.1) or the 4.x models in between (Sonnet 4.6, Opus 4.5 to 4.8). I can run those to see exactly where the cutoff is.

### YOU - 2026-10-28 23:28:21 UTC

Test invoking Claude Opus 4.5 on Bedrock

### COMMAND / TOOL CALL (Bash) - 2026-10-28 23:28:22 UTC

```bash
cd /tmp && aws bedrock-runtime converse --region us-east-1 --model-id us.anthropic.claude-opus-4-5-20251101-v1:0 --messages '[{"role":"user","content":[{"text":"Reply with the single word: pong"}]}]' --inference-config '{"maxTokens":20}' --query '{text:output.message.content[0].text,stop:stopReason,usage:usage}' 2>&1
```

### OUTPUT - 2026-10-28 23:28:25 UTC

```text
{
    "text": "pong",
    "stop": "end_turn",
    "usage": {
        "inputTokens": 15,
        "outputTokens": 5,
        "totalTokens": 20,
        "cacheReadInputTokens": 0,
        "cacheWriteInputTokens": 0
    }
}
Shell cwd was reset to /Users/Twolliston/Documents/TheoWAF/seir-foundations
```

### CLAUDE - 2026-10-28 23:28:26 UTC

Opus 4.5 works on Bedrock. The call to `us.anthropic.claude-opus-4-5-20251101-v1:0` in `us-east-1` returned `pong` (15 input tokens, 5 output).

| Model | Result |
|---|---|
| Haiku 4.5 | Works |
| Sonnet 4.5 | Works |
| Opus 4.5 | Works |
| Sonnet 5.5 | Blocked |
| Haiku 5.5 | Blocked |

All three 4.5 models work and both 5.5 models I tried are blocked. I haven't tested the other 5.x models or the 4.6 to 4.8 models, so I can't say yet where the cutoff falls. I can test those next.

### YOU - 2026-10-28 23:28:30 UTC

Test invoking Claude Sonnet 4.6 on Bedrock

### COMMAND / TOOL CALL (Bash) - 2026-10-28 23:28:31 UTC

```bash
cd /tmp && aws bedrock-runtime converse --region us-east-1 --model-id us.anthropic.claude-sonnet-4-6 --messages '[{"role":"user","content":[{"text":"Reply with the single word: pong"}]}]' --inference-config '{"maxTokens":20}' --query '{text:output.message.content[0].text,stop:stopReason,usage:usage}' 2>&1
```

### OUTPUT - 2026-10-28 23:28:33 UTC

```text
{
    "text": "pong",
    "stop": "end_turn",
    "usage": {
        "inputTokens": 15,
        "outputTokens": 5,
        "totalTokens": 20,
        "cacheReadInputTokens": 0,
        "cacheWriteInputTokens": 0
    }
}
Shell cwd was reset to /Users/Twolliston/Documents/TheoWAF/seir-foundations
```

### CLAUDE - 2026-10-28 23:28:35 UTC

Sonnet 4.6 works on Bedrock. The call to `us.anthropic.claude-sonnet-4-6` in `us-east-1` returned `pong` (15 input tokens, 5 output).

| Model | Result |
|---|---|
| Haiku 4.5 | Works |
| Sonnet 4.5 | Works |
| Opus 4.5 | Works |
| Sonnet 4.6 | Works |
| Sonnet 5.5 | Blocked |
| Haiku 5.5 | Blocked |

The cutoff is somewhere after 4.6. I haven't tested Opus 4.6, 4.7 or 4.8, or Sonnet 5, Opus 5, Opus 5.5 and Fable 5 and 5.1. I can run those to narrow it down.

### YOU - 2026-10-28 23:28:39 UTC

Test invoking Claude Opus 4.8 on Bedrock

### COMMAND / TOOL CALL (Bash) - 2026-10-28 23:28:40 UTC

```bash
cd /tmp && aws bedrock-runtime converse --region us-east-1 --model-id us.anthropic.claude-opus-4-8 --messages '[{"role":"user","content":[{"text":"Reply with the single word: pong"}]}]' --inference-config '{"maxTokens":20}' --query '{text:output.message.content[0].text,stop:stopReason,usage:usage}' 2>&1
```

### OUTPUT - 2026-10-28 23:28:41 UTC

```text
Exit code 254

aws: [ERROR]: An error occurred (AccessDeniedException) when calling the Converse operation: anthropic.claude-opus-4-8 is not available for this account. You can explore other available models on Amazon Bedrock. For additional access options, contact AWS Sales at https://aws.amazon.com/contact-us/sales-support/
```

### CLAUDE - 2026-10-28 23:28:43 UTC

Opus 4.8 is blocked. The error was `AccessDeniedException: anthropic.claude-opus-4-8 is not available for this account`.

| Model | Result |
|---|---|
| Haiku 4.5 | Works |
| Sonnet 4.5 | Works |
| Opus 4.5 | Works |
| Sonnet 4.6 | Works |
| Opus 4.8 | Blocked |
| Sonnet 5.5 | Blocked |
| Haiku 5.5 | Blocked |

So the cutoff is between 4.6 and 4.8. The untested models in that gap are Opus 4.6 and Opus 4.7. Everything above 4.8 (Sonnet 5, Opus 5, Opus 5.5, Fable 5 and 5.1) is also untested, though it's likely blocked too. I can test Opus 4.6 and 4.7 to pin down the exact line.

### YOU - 2026-10-28 23:28:46 UTC

Test invoking Claude Opus 4.7 on Bedrock

### COMMAND / TOOL CALL (Bash) - 2026-10-28 23:28:48 UTC

```bash
cd /tmp && aws bedrock-runtime converse --region us-east-1 --model-id us.anthropic.claude-opus-4-7 --messages '[{"role":"user","content":[{"text":"Reply with the single word: pong"}]}]' --inference-config '{"maxTokens":20}' --query '{text:output.message.content[0].text,stop:stopReason,usage:usage}' 2>&1
```

### OUTPUT - 2026-10-28 23:28:49 UTC

```text
Exit code 254

aws: [ERROR]: An error occurred (AccessDeniedException) when calling the Converse operation: anthropic.claude-opus-4-7 is not available for this account. You can explore other available models on Amazon Bedrock. For additional access options, contact AWS Sales at https://aws.amazon.com/contact-us/sales-support/
```

### CLAUDE - 2026-10-28 23:28:51 UTC

Opus 4.7 is blocked too. The error was `AccessDeniedException: anthropic.claude-opus-4-7 is not available for this account`.

| Model | Result |
|---|---|
| Haiku 4.5 | Works |
| Sonnet 4.5 | Works |
| Opus 4.5 | Works |
| Sonnet 4.6 | Works |
| Opus 4.7 | Blocked |
| Opus 4.8 | Blocked |
| Sonnet 5.5 | Blocked |
| Haiku 5.5 | Blocked |

The cutoff is now between Sonnet 4.6 (works) and Opus 4.7 (blocked). Opus 4.6 is the one model left in that gap. The 5.x models other than Sonnet 5.5 and Haiku 5.5 are still untested. I can test Opus 4.6 to finish narrowing it down.

### YOU - 2026-10-28 23:28:55 UTC

Test invoking Claude Opus 4.6 on Bedrock

### COMMAND / TOOL CALL (Bash) - 2026-10-28 23:28:56 UTC

```bash
cd /tmp && aws bedrock-runtime converse --region us-east-1 --model-id us.anthropic.claude-opus-4-6-v1 --messages '[{"role":"user","content":[{"text":"Reply with the single word: pong"}]}]' --inference-config '{"maxTokens":20}' --query '{text:output.message.content[0].text,stop:stopReason,usage:usage}' 2>&1
```

### OUTPUT - 2026-10-28 23:28:59 UTC

```text
{
    "text": "pong",
    "stop": "end_turn",
    "usage": {
        "inputTokens": 15,
        "outputTokens": 5,
        "totalTokens": 20,
        "cacheReadInputTokens": 0,
        "cacheWriteInputTokens": 0
    }
}
Shell cwd was reset to /Users/Twolliston/Documents/TheoWAF/seir-foundations
```

### CLAUDE - 2026-10-28 23:29:02 UTC

Opus 4.6 works on Bedrock. The call to `us.anthropic.claude-opus-4-6-v1` in `us-east-1` returned `pong` (15 input tokens, 5 output).

| Model | Result |
|---|---|
| Haiku 4.5 | Works |
| Sonnet 4.5 | Works |
| Opus 4.5 | Works |
| Sonnet 4.6 | Works |
| Opus 4.6 | Works |
| Opus 4.7 | Blocked |
| Opus 4.8 | Blocked |
| Sonnet 5.5 | Blocked |
| Haiku 5.5 | Blocked |

So every Anthropic model up to 4.6 works, and everything from 4.7 up that I tested is blocked. Opus 4.1 is the only older model I haven't tried.


Where the AI was wrong, vague, or out of date:
(at least one example, and how you found out)

N/A

```

> 🔒 **Never paste private keys (`.pem` contents), AWS access keys, passwords, or tokens into an AI prompt.**

---

## 6. Required — `spotter_koffi_aleki.txt` (`spotter did not produce upon request`)

This file has **two halves**: one about your spotter, and one about the person you spot for. They are cross-checked: what you write about your spotter must match what your spotter writes in **their** file about you.

```
Spotter = ?   (the person who spots YOU)
5 things my spotter learned while working on the lab / homework:
1. ?
2. ?
3. ?
4. ?
5. ?

I am the spotter for = ?   (the person YOU spot)
5 things I learned that I shared with them:
1. ?
2. ?
3. ?
4. ?
5. ?
```

**How the cross-check works:** if Jane is Alex's spotter, then the 5 points in Alex's first half (about Jane) should match the 5 points in Jane's second half (shared with Alex). Agree on your 5 points together, in your own words. They do not need to be word-for-word, but they must be the same 5 lessons.

Be specific. Ask your spotter directly — these are **their** lessons, not yours.

`No feedback from spotter`

- ✅ "Learned that return code 4 means the account was not found, and the program does not crash."
- ❌ "Learned a lot about EC2."

---

## 7. Required — Talk to the COBOL core

Do this on **any one** of your lab-run instances (before Step 4, after stopping the server, or in a second SSH window). Start in the bank folder:

```bash
cd /opt/balerica-bank
```

Each screenshot must also show the **ID line** from Section 3.2. Use a **lab-run instance from your table**, and say which run number in your notes.

**Use your own transaction IDs.** Every `TXN` you post must start with your initials, for example `TXN-JD-0001` for Jane Doe. Do not copy the IDs in the examples below.

Screenshot as Screenshot as [`payment-post`](screenshots/step3-payment-post.png).

### 7.1 Find your customers

```bash
cat data/accounts.dat
```

How many accounts are there? Write down every account ID.

```text
100001Alice Johnson                 ACTIVE  000000275936USD
100002Robert Smith                  ACTIVE  000000127165USD
100003Maria Garcia                  ACTIVE  000000606698USD
```


### 7.2 Trigger every return code on purpose

Run each command, then immediately run `echo $?` to see the return code.

| Screenshot | Goal | Command to try |
|------------|------|----------------|
| [`cobol_rc0.jpg`](screenshots/cobol_rc0.jpg) | **0** — success | `./cobol/bin/account_lookup 100001` |
| [`cobol_rc4.jpg`](screenshots/cobol_rc4.jpg) | **4** — account not found | `./cobol/bin/account_lookup 999999` |
| [`cobol_rc8.jpg`](screenshots/cobol_rc8.jpg) | **8** — business rejection | `./cobol/bin/payment_post TXN-XX-0001 100001 0.00 USD TEST-ZERO` (zero amount, with your initials in place of `XX`) — then try an amount bigger than the balance |
| [`cobol_rc12.jpg`](screenshots/cobol_rc12.jpg) | **12** — environment failure | `cd ~` then `/opt/balerica-bank/cobol/bin/account_lookup 100001` (wrong folder) |

After the rc 12 test, go back with `cd /opt/balerica-bank`.

**Bonus:** if one of the accounts from 7.1 is not `ACTIVE`, try posting a payment to it. What return code and `REASON=` do you get?

### 7.3 Decode the fixed-width ledger by hand

Use the column layout from the runbook's Reference section:

```bash
cut -c1-6   data/accounts.dat    # account id
cut -c7-36  data/accounts.dat    # customer name
cut -c37-44 data/accounts.dat    # status
cut -c45-56 data/accounts.dat    # balance (implied decimal!)
cut -c57-59 data/accounts.dat    # currency
```

```text
Columns  1-6   account id       PIC X(6)
Columns  7-36  customer name    PIC X(30)
Columns 37-44  status           PIC X(8)
Columns 45-56  balance          PIC 9(10)V99   (implied decimal)
Columns 57-59  currency         PIC X(3)
```
Screenshot as [`decode-fixed-with-ledger`](screenshots/decode-fixed-width-ledger.jpg)


### 7.4 Write it up (add a "COBOL practice" section to `lab1_notes.md`)(https://github.com/Twolliston-CPG/seir-foundations/blob/main/module1/lesson1_ec2/LAB1_NOTES.md)

- Which run (and Instance ID) you used.
- For each return code: the command you ran, the **exact** output lines (copy-paste them, including `ERROR=` or `STATUS=` / `REASON=`), and what the code means.
- Decode Alice's balance by hand: what are the raw 12 characters, and what dollar amount do they mean? Why is there no decimal point in the file?
- Run `cat data/payments.dat`. Copy-paste **the journal lines for your own `TXN` IDs**. Then look up account `100001` again. Did the balance change after your payments? Write down what you see and your best guess why.

**Optional:** check if the SQLite command-line tool is installed with `which sqlite3`. If it is, run `sqlite3 data/bank.db ".tables"` and `sqlite3 data/bank.db ".schema"`, and describe what tables the bank keeps.

---

## 8. Required — Clone your own homework repo onto EC2

On any lab-run instance:

```bash
cd ~
whoami && TZ='Your/Zone' date && ec2-metadata -i && uptime -s
git clone https://github.com/YOUR-GITHUB-USERNAME/seir-foundations-homework.git
ls seir-foundations-homework/module1
```

Screenshot as [`git_clone.jpg`](screenshots/git_clone.jpg).

- Your homework repo must be **public** for this to work without logging in.
- **Clone only. Do not push from the EC2 instance**, and do not put a GitHub token or password on the server for this assignment.

---

## 9. Required — `AI_enabled_study_lab1.0.txt`

For each of the 5 topics below, you will use **three sources**:

1. **Read** the listed source.
2. **Watch** the listed video.
3. **Ask an AI** (your choice) the research points the reading and video did not answer.

Then write **one paragraph per topic, minimum 5 sentences**, in your own words.

### Rules

- **Every number needs a source and a year.** Example: "about X billion lines of COBOL (source: ___, 2022)." COBOL and banking statistics are repeated all over the internet without dates, and many disagree. If two sources disagree, say so.
- If the AI gives you a number, ask it where the number comes from, then try to find that source yourself.
- Do not paste the AI's answer. Your paragraph must be your own writing.

### File format

```
=== Topic 1: Databases ===
Read:    (title + link)
Watched: (title + link)
AI used: ?
Prompt(s) I asked the AI:
One thing the AI said that I double-checked, and what I found:

Paragraph (minimum 5 sentences):

Numbers + sources:
- (number) — (source, year)

=== Topic 2: COBOL ===
...
```

### Topic 1 — Database basics

| Read | Watch |
|------|-------|
| [AWS: What's the Difference Between Relational and Non-relational Databases?](https://aws.amazon.com/compare/the-difference-between-relational-and-non-relational-databases/) | [IBM Technology: SQL vs. NoSQL — What's the difference?](https://www.youtube.com/watch?v=Q5aTUc7c4jg) (6 min) |

Research points:

- What is a database, and why does nearly every application need one?
- Types of databases (relational, key-value, document, graph, etc.).
- How do you choose one database over another?
- What do SQL and NoSQL mean? How are they represented in the cloud? (Example: Amazon RDS / Aurora vs. DynamoDB.)
- Which databases are the de facto standards? Compare SQLite, Microsoft SQL Server, MariaDB/MySQL, and PostgreSQL.
- Strengths and weaknesses of PostgreSQL.
- **Lab hook:** Balerica's system of record is SQLite (`data/bank.db`). Why might a teaching lab choose SQLite, and why would a real bank probably not?

### Topic 2 — COBOL basics

| Read | Watch |
|------|-------|
| [Wikipedia: COBOL](https://en.wikipedia.org/wiki/COBOL) | [Fireship: COBOL in 100 Seconds](https://www.youtube.com/watch?v=7d7-etf-wNI) (2 min) |

Research points:

- What is COBOL, and who introduced it?
- How was it first integrated into infrastructure (mainframes, government, banks)?
- How many systems use COBOL today?
- What is the value of the systems that run on COBOL (transactions, money, records)?
- What is the average age of COBOL engineers, and why does it matter?
- How much effort would replacing COBOL take, and why have so many replacement projects struggled?
- **Lab hook:** In `payments.dat`, 125.50 is stored as `000000012550`. Why would a 1959 business language store money with an *implied* decimal instead of a decimal point?

### Topic 3 — SWIFT basics (the financial payment messaging network)

> **Note:** This is **SWIFT, the Society for Worldwide Interbank Financial Telecommunication** — the network banks use to send payment instructions. It is **not** Apple's Swift programming language.

| Read | Watch |
|------|-------|
| [Wikipedia: SWIFT](https://en.wikipedia.org/wiki/SWIFT) | [a16z: Foreign Exchange 101 — What Happens When You Send Money Abroad?](https://www.youtube.com/watch?v=eoXdyO9oGJc) (6 min) |

Research points:

- What is SWIFT, who introduced it, and when?
- Does SWIFT actually move money, or does it move *messages* about money? What are correspondent banks?
- How is SWIFT used day to day? Who uses it?
- Close competitors and alternatives (for example: CIPS, SPFS, Ripple, real-time payment systems).
- How much effort would replacing SWIFT take?
- **ISO 20022 deep dive:**
  - What is ISO 20022, and how is it different from the older MT message format?
  - What is an **MT103**? What is an **MT202**? How are they different?
  - What replaced them? (Look up **pacs.008** and **pacs.009**.)
  - When did the MT/ISO 20022 "coexistence period" end for cross-border payment instructions? Confirm the date on Swift's own FAQ: [Swift ISO 20022 FAQs — Implementation](https://www.swift.com/standards/iso-20022/iso-20022-faqs/implementation).
  - Which MT messages are still in use after that date, and why do old formats survive so long?
- **Lab hook:** Your traffic generator sends **MT103** messages — a format that is now retired for cross-border payment instructions. Why might a training lab still teach MT103? What would change if Balerica switched to pacs.008?

### Topic 4 — API basics

| Read | Watch |
|------|-------|
| [MDN: An overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview) | [IBM Technology: What is a REST API?](https://www.youtube.com/watch?v=lsMQRaeKNDk) (9 min) |

Research points:

- What is an API, and who introduced the idea (and the REST style)?
- How many systems use APIs today? How are they used?
- Close competitors and alternatives: REST vs. SOAP vs. GraphQL vs. gRPC.
- Why are APIs important for AI adoption? (Hint: how does your EC2 talk to Amazon Bedrock?)
- Why is securing API communications difficult? (Look up authentication, TLS, input validation, and the OWASP API Security Top 10.)
- **Next-lab prep:**
  - What is the difference between `GET` and `POST`?
  - What is JSON, and why do APIs use it?
  - Why should an API never trust incoming data, even from a "friendly" client?
- **Lab hook:** Look at the runbook's API endpoints table. Which Balerica endpoints are `GET` and which are `POST`? Why does `/payments` need to be `POST`?

### Topic 5 — Where COBOL, SWIFT, APIs, and databases meet

| Read | Watch |
|------|-------|
| [US GAO (2025): Agencies Need to Plan for Modernizing Critical Decades-Old Legacy Systems](https://files.gao.gov/reports/GAO-25-107795/index.html) | [Modernizing COBOL: From Mainframe to API](https://www.youtube.com/watch?v=-CI8hb-077E) (6 min) |

Research points:

- Trace one payment through Balerica in your own words: SWIFT message → FastAPI → COBOL program → fixed-width file → SQLite. Which piece is old, which is new, and why keep both?
- Why do organizations often **wrap** legacy systems with APIs instead of replacing them?
- How do these four technologies matter to different industries: **financial, medical/healthcare, academic, and government**? Give at least one real example per industry.
- What risks does the GAO report describe for systems that are decades old?
- How is AI being used today to understand or modernize COBOL systems, and what are its limits?

---

## 10. "Be A Man" (BAM) extra credit

Steps 5–8 of the runbook are now fair game. Each screenshot must show the **ID line** from Section 3.2. Add a **BAM** section to `lab1_notes.md` with the Instance ID from each BAM screenshot.

### BAM_2.1 — Make `/ask` answer with Bedrock

**Submission:** `BAM_2.1.jpg`

**Student Challenge:** make the Balerica AI helper answer from a real Claude model instead of `offline-knowledge-base`.

> 📢 **Updated instructions:** AWS retired the Bedrock **Model Access** page. Serverless models are now available automatically in your Region. **Anthropic (Claude) models still require a one-time usage form** the first time you use them in your account.

All three requirements from the runbook's "Why `/ask` might silently stay offline" section must be true:

1. **IAM role:** create an IAM role with Bedrock invoke permission and attach it to your instance. Use `iam/PERMISSIONS.md` in the lab's `API` folder as your guide. (In your own AWS account, you are the admin.) **Do not put AWS access keys on the instance.**
2. **Region:** `AWS_REGION` must match the Region where you will call Bedrock.
3. **Model ID:** `BEDROCK_MODEL_ID` must be a real **inference profile ID**. Newer Claude models need the inference profile ID (it starts with `us.`), not the base model ID. Find it in the Bedrock console.

Set the variables in **Window 1**, in the same terminal, **before** starting uvicorn:

```bash
cd /opt/balerica-bank
source venv/bin/activate
export AWS_REGION=us-east-1
export BEDROCK_MODEL_ID=us.YOUR-INFERENCE-PROFILE-ID
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Then in **Window 2**, ask a question with `curl` (Step 8). Your screenshot must show a response whose `source` is **not** `offline-knowledge-base`.

In your notes, record the **IAM role name** you attached and the **inference profile ID** you used. Ask a question that only your ledger can answer, and copy-paste the full response, for example: "What payments did TXN-XX-0001 produce?" with your own TXN ID.

Bedrock calls are billed per use. A few test questions cost very little, but do not loop it.

### BAM_2.2 — Bake it in (launch template User Data)

**Submission:** `BAM_2.2.jpg`

Create a **new** launch template (for example `seir-lesson1-baked`) whose User Data installs the whole lab at boot, so a new instance is ready for Step 3 without you typing the install steps. **Do not overwrite your Lab 0 template.**

Starting point (you may need to debug it — that is the challenge):

```bash
#!/bin/bash
dnf install -y git
cd /home/ec2-user
sudo -u ec2-user git clone https://github.com/BalericaAI/SEIR-Foundations.git
sudo -u ec2-user bash SEIR-Foundations/module1/lesson1_ec2/API/install/install.sh
```

Launch an instance from it, wait a few minutes, then SSH in. Your screenshot must show:

- `sudo tail -n 20 /var/log/cloud-init-output.log` showing `Installation complete.`
- `cd /opt/balerica-bank && ./cobol/bin/account_lookup 100001` working — without you running the installer.

In `lab1_notes.md`, record the **launch template ID** (starts with `lt-`) and version number, and paste your final User Data script. Then explain: what did you have to fix (if anything), and why does User Data run as `root` by default?

### BAM_2.3 — Build a golden AMI

**Submission:** `BAM_2.3.jpg`

Turn a successfully configured instance into a reusable image.

1. On an instance where Steps 0–4 worked, stop the server (`Ctrl+C`).
2. **EC2 → Instances → (your instance) → Actions → Image and templates → Create image.** Name it something like `seir-balerica-golden-v1`. (By default AWS reboots the instance to take a clean image.)
3. Wait until the AMI shows **Available** under **EC2 → AMIs**.
4. Launch a **new** instance from your AMI, SSH in, and go straight to Step 4:

```bash
cd /opt/balerica-bank
source venv/bin/activate
whoami && TZ='Your/Zone' date && ec2-metadata -i && uptime -s
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Your screenshot must show `Application startup complete.` on the AMI-launched instance, with no installer run.

In `lab1_notes.md`, record:

- The **AMI ID** (starts with `ami-`) and the **snapshot ID** behind it (starts with `snap-`, found under **EC2 → Snapshots**).
- The Instance ID of the instance you **built the AMI from**, and the Instance ID of the instance you **launched from the AMI**.

Then answer:

- Were your earlier test payments still in `data/payments.dat` on the new instance? Why?
- What is the difference between a launch template (BAM_2.2) and an AMI (BAM_2.3)? When would you use each?

**Cost warning:** an AMI keeps an **EBS snapshot**, and snapshots are billed while they exist. Unless Theo tells you to keep it, **deregister the AMI** when you are done, then delete its snapshot under **EC2 → Snapshots**. Deregistering does not delete the snapshot for you.

### Extra credit evidence table

| Item | Requirement | Screenshot | Done? |
|------|-------------|------------|-------|
| BAM_2.1 | `/ask` answered by Bedrock (not `offline-knowledge-base`) | `screenshots/BAM_2.1.jpg` | Yes / No |
| BAM_2.2 | Baked launch template; cloud-init log + COBOL lookup with no manual install | `screenshots/BAM_2.2.jpg` | Yes / No |
| BAM_2.3 | Golden AMI; uvicorn starts on AMI instance with no installer | `screenshots/BAM_2.3.jpg` | Yes / No |

**Screenshot guidance:** Do not expose private keys, passwords, AWS access keys, tokens, or other secrets in any screenshot.

---

## 11. Definition of done

&nbsp;

> ⚠️⚠️⚠️ **WARNING: THE SCREENSHOT DAILY LIMIT IS STRICT** ⚠️⚠️⚠️
>
> 🚨 **4 or more** lab-run screenshots on the same local date is an **AUTOMATIC FAILURE FOR THIS WEEK.** 🚨
>
> ❌ No exceptions. Spread your seven runs over at least three days.

&nbsp;

**Required**
- [ ] I completed Steps 0–4 on **seven** fresh EC2 instances, with **no more than 3** on any one local date.
- [ ] Every screenshot shows the full ID line: `whoami`, local `date`, `ec2-metadata -i`, and `uptime -s`.
- [ ] Each `lab1_run` screenshot also shows `Application startup complete.`
- [ ] My `lesson1_ec2/README.md` has the run table with seven unique Instance IDs, boot times, and Public DNS names that match my screenshots.
- [ ] I terminated every lab instance and checked for leftover volumes and Elastic IPs. My launch template still exists.
- [ ] I uploaded `lab1_notes.md` with notes for every run (each with its Instance ID and one exact output line), a "Mistakes I made" list, and a "COBOL practice" section with my own TXN IDs and exact output lines.
- [ ] I completed the Maarek Section 21, 23, and 25 quizzes and uploaded the screenshots.
- [ ] I uploaded `ai_review_YourNameHere.txt` with a share link or transcript, at least 5 questions, how I checked each one, and one place the AI was wrong or vague.
- [ ] I uploaded `spotter_YourNameHere.txt` with both halves filled in: my spotter + 5 things they learned, and the person I spot + 5 things I shared with them.
- [ ] I triggered return codes 0, 4, 8, and 12 and decoded the ledger, with screenshots.
- [ ] I cloned my own homework repo onto EC2 (clone only, no push) and uploaded `git_clone.jpg`.
- [ ] I uploaded `AI_enabled_study_lab1.0.txt` with one paragraph (minimum 5 sentences) for each of the 5 topics, using all three sources per topic, with a source and year for every number.
- [ ] I committed and pushed everything to my GitHub repository by **Tuesday, November 3, 2026, 12:00 PM Central Time**.

**Extra credit**
- [ ] `BAM_2.1.jpg` — `/ask` answered by Bedrock.
- [ ] `BAM_2.2.jpg` — baked launch template works.
- [ ] `BAM_2.3.jpg` — golden AMI works.
- [ ] I deregistered unused AMIs, deleted their snapshots, and checked for leftover billable resources.

> **Chewbacca's final assessment:** RRRRAAAWWWRRR! Seven banks opened. Four return codes triggered on purpose. A legacy core you can read by hand. Next week, it becomes a platform.
