#!/usr/bin/env python3

import random
import time

BANNER = r"""
=========================================================
           SEIR ENGINEERING DIAGNOSTICS v1.0
        Systems Engineering & Infrastructure Integration
=========================================================
"""

SKILLS = [
    "Installed Terraform",
    "Built AWS Lambda",
    "Configured IAM Roles",
    "Read CloudWatch Logs",
    "Created API Gateway",
    "Protected APIs with WAF",
    "Used DynamoDB",
    "Integrated Amazon Bedrock",
    "Worked with EventBridge",
    "Configured Cognito",
    "Implemented RBAC",
    "Used Kubernetes",
]

MESSAGES = [
    "CloudWatch is your friend.",
    "Terraform is deterministic.",
    "IAM is strict because security matters.",
    "Every engineer has broken production at least once.",
    "The logs usually know the answer.",
    "You are one debug session away from understanding.",
]

THEO_QUOTES = [
    "Read the logs.",
    "Think first. Google second.",
    "AI should assist your thinking, not replace it.",
    "Observe. Understand. Build. Verify.",
    "If Terraform failed, congratulations—you've found today's lesson.",
]

def slow(text, delay=0.02):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

print(BANNER)

name = input("Student Name: ").strip()

if not name:
    name = "Engineer"

print()
slow("Running engineering diagnostics...\n")

time.sleep(1)

passed = random.randint(8, len(SKILLS))
completed = random.sample(SKILLS, passed)

print("Completed Engineering Milestones")
print("--------------------------------")

for item in completed:
    print(f"  [PASS] {item}")
    time.sleep(0.15)

print()

print("Scanning confidence levels...")
time.sleep(1)

confidence = random.randint(25, 75)
competence = random.randint(80, 99)

print(f"Confidence Level : {confidence}%")
print(f"Competence Level : {competence}%")

print()

if confidence < competence:
    print("WARNING")
    print("--------------------------------")
    print("Confidence does not match demonstrated ability.\n")
    print("Diagnosis:")
    print("    Impostor Syndrome Detected.\n")
else:
    print("Confidence and competence are aligned.\n")

time.sleep(1)

print("Engineering Advice")
print("--------------------------------")
print(f"• {random.choice(MESSAGES)}")
print(f"• {random.choice(MESSAGES)}")
print(f"• Theo says: \"{random.choice(THEO_QUOTES)}\"")

print()

print("Checking Terraform Fear Index...")
time.sleep(2)

fear = random.randint(60, 100)

print(f"Terraform Fear Index : {fear}%")

time.sleep(1)

print("\nAnalyzing...")

time.sleep(2)

print("\nResult:")

print("""
Terraform cannot:

  • Judge you
  • Fire you
  • Ruin your career
  • Know you're nervous

Terraform CAN:

  • Tell you exactly what's wrong
  • Create infrastructure
  • Destroy infrastructure
      (please don't use destroy today...)
""")

print()

print("Cloud Engineering Probability Report")
print("------------------------------------")

print(f"Probability you'll solve today's lab:      {random.randint(92,99)}%")
print(f"Probability CloudWatch has the answer:      99.94%")
print(f"Probability IAM is involved:                87.31%")
print(f"Probability Theo says 'Read the logs':      99.94%")
print(f"Probability Terraform is actually broken:   0.42%")

print()

slow("Final Assessment...\n")

time.sleep(2)

print("==========================================")
print(f"Status : ENGINEER IN TRAINING")
print(f"Student: {name}")
print("==========================================")

print("""
Remember:

Confusion is temporary.
Learning is cumulative.
Every engineer starts exactly where you are.

Now...

Go build something awesome.
""")

print("          — Broken Theo (from bed)")
