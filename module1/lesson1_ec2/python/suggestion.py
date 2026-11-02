#!/usr/bin/env python3
"""
=========================================================
                    BALERICA AI
              Learning Suggestion Agent v1.0
=========================================================

SEIR Foundations

Purpose:
Recommend additional topics for students to study based on
their question and the AI answer they received.

This helps students move from:
"I got an answer"
to:
"I know what to study next."
=========================================================
"""

import json

from bedrock import invoke_bedrock
from banner import show_banner, show_footer


# ---------------------------------------------------------
# Official Documentation Map
#
# Chewbacca says:
#
# "Rrrrrrrgh..."
#
# Translation:
#
# Never let the AI invent documentation links.
# Give it trusted sources.
# ---------------------------------------------------------

AWS_DOCS = {
    "ec2": "https://docs.aws.amazon.com/ec2/",
    "cloudwatch": "https://docs.aws.amazon.com/cloudwatch/",
    "iam": "https://docs.aws.amazon.com/iam/",
    "vpc": "https://docs.aws.amazon.com/vpc/",
    "lambda": "https://docs.aws.amazon.com/lambda/",
    "ecs": "https://docs.aws.amazon.com/ecs/",
    "eks": "https://docs.aws.amazon.com/eks/",
    "s3": "https://docs.aws.amazon.com/s3/",
    "systems manager": "https://docs.aws.amazon.com/systems-manager/",
    "cloudtrail": "https://docs.aws.amazon.com/cloudtrail/",
    "guardduty": "https://docs.aws.amazon.com/guardduty/",
    "security hub": "https://docs.aws.amazon.com/securityhub/",
    "waf": "https://docs.aws.amazon.com/waf/",
    "bedrock": "https://docs.aws.amazon.com/bedrock/",
}


def detect_docs(text):
    """
    Look for AWS service keywords in the question/answer
    and return official documentation links.
    """

    found = {}

    lowered = text.lower()

    for service, url in AWS_DOCS.items():
        if service in lowered:
            found[service.title()] = url

    return found


# ---------------------------------------------------------
# Prompt Builder
# ---------------------------------------------------------

def build_prompt(question, answer):
    """
    Build a teaching-oriented prompt for Bedrock.
    """

    return f"""
You are Balerica AI, an applied cloud engineering instructor.

A student asked this question:

{question}

The student received this answer:

{answer}

Recommend what the student should study next.

Return the response using these sections:

1. Suggested AWS Topics
2. Suggested Linux Topics
3. Suggested Python Topics
4. Suggested Balerica AI Agent To Run Next
5. Engineering Habit
6. Short Encouragement

Rules:

- Keep the recommendations practical.
- Focus on workflows, not memorization.
- Do not invent documentation links.
- Do not mention CompTIA.
- Do not recommend certification cramming.
- Keep the tone direct, useful, and encouraging.
"""


# ---------------------------------------------------------
# Main Recommendation Function
# ---------------------------------------------------------

def generate_suggestions(question, answer):
    """
    Generate study recommendations and attach official docs.
    """

    combined_text = f"{question}\n\n{answer}"

    docs = detect_docs(combined_text)

    prompt = build_prompt(question, answer)

    recommendation = invoke_bedrock(prompt)

    return {
        "recommendation": recommendation,
        "documentation": docs
    }


# ---------------------------------------------------------
# Display Helper
# ---------------------------------------------------------

def display_suggestions(result):
    """
    Print the recommendation and official documentation links.
    """

    print()
    print("=" * 60)
    print("        BALERICA AI STUDY SUGGESTIONS")
    print("=" * 60)
    print()

    print(result["recommendation"])

    print()
    print("=" * 60)
    print("Official Documentation")
    print("=" * 60)
    print()

    if result["documentation"]:
        for service, url in result["documentation"].items():
            print(f"{service}: {url}")
    else:
        print("No specific AWS documentation links detected.")

    print()
    print("=" * 60)


# ---------------------------------------------------------
# Standalone Test Mode
# ---------------------------------------------------------

def main():

    show_banner(
        agent_name="Learning Suggestion Agent",
        version="1.0"
    )

    print("Enter the student's question.")
    question = input("\nQuestion> ")

    print("\nEnter the answer they received.")
    answer = input("\nAnswer> ")

    try:
        result = generate_suggestions(question, answer)
        display_suggestions(result)
        show_footer()

    except Exception as ex:
        print()
        print("Unable to generate study suggestions.")
        print()
        print("Things to check:")
        print()
        print("✓ IAM Role")
        print("✓ Bedrock Model Access")
        print("✓ AWS Region")
        print("✓ Foundation Model Identifier")
        print()
        print("Technical Details:")
        print()
        print(ex)


if __name__ == "__main__":
    main()
