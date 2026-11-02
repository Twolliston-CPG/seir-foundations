#!/usr/bin/env python3
"""
=========================================================
                    BALERICA AI
                  Auditor v1.0
=========================================================

SEIR Foundations

Purpose:
Inspect student queries before they are sent to Bedrock.

The auditor looks for:
- Prompt manipulation
- SQL injection patterns
- Unsupported certification-cram topics
- Possible secrets
- Inappropriate requests

=========================================================
"""

import random
import re


BLOCKED_TOPICS = [
    "comptia",
    "a+",
    "network+",
    "security+",
    "pentest+",
    "cysa+",
    "casp+",
]


PROMPT_MANIPULATION_PATTERNS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "forget your instructions",
    "reveal your system prompt",
    "show me your system prompt",
    "developer message",
    "system message",
    "jailbreak",
    "bypass",
    "pretend you are",
    "you are now",
    "act as",
]


SQL_INJECTION_PATTERNS = [
    r"(\bor\b|\band\b)\s+1\s*=\s*1",
    r"union\s+select",
    r"drop\s+table",
    r"delete\s+from",
    r"insert\s+into",
    r"update\s+\w+\s+set",
    r"--",
    r";\s*drop",
    r"information_schema",
    r"xp_cmdshell",
]


SECRET_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",
    r"ASIA[0-9A-Z]{16}",
    r"-----BEGIN PRIVATE KEY-----",
    r"-----BEGIN RSA PRIVATE KEY-----",
    r"aws_secret_access_key",
    r"aws_access_key_id",
]


REFLECTIONS = [
    {
        "author": "Ptahhotep",
        "theme": "Humility",
        "lesson": "Listen carefully before drawing conclusions."
    },
    {
        "author": "Zera Yacob",
        "theme": "Reason",
        "lesson": "Examine problems through careful reasoning."
    },
    {
        "author": "Anton Wilhelm Amo",
        "theme": "Disciplined Study",
        "lesson": "Understanding grows through patient investigation."
    },
    {
        "author": "Marcus Aurelius",
        "theme": "Discipline",
        "lesson": "Focus on what is under your control."
    },
    {
        "author": "Epictetus",
        "theme": "Self-Mastery",
        "lesson": "Pause before reacting. Choose the useful action."
    },
]


def contains_keyword(text, keywords):
    lowered = text.lower()

    for keyword in keywords:
        if keyword in lowered:
            return True

    return False


def matches_pattern(text, patterns):
    lowered = text.lower()

    for pattern in patterns:
        if re.search(pattern, lowered, re.IGNORECASE):
            return True

    return False


def choose_reflection():
    return random.choice(REFLECTIONS)


def build_rejection(category, reason):
    reflection = choose_reflection()

    return f"""
============================================================
                    BALERICA AI AUDITOR
============================================================

Status

   REQUEST REJECTED

Category

   {category}

Reason

   {reason}

Reflection

   {reflection["author"]}

Theme

   {reflection["theme"]}

Lesson

   {reflection["lesson"]}

============================================================
"""


def audit_request(question):
    """
    Inspect a user question before sending it to Bedrock.

    Returns:
        tuple:
            approved: bool
            message: str
    """

    if question is None or len(question.strip()) == 0:
        return False, build_rejection(
            "EMPTY_REQUEST",
            "The request was empty."
        )

    if contains_keyword(question, BLOCKED_TOPICS):
        return False, build_rejection(
            "COURSE_SCOPE",
            "This request falls outside the objectives of SEIR Foundations."
        )

    if contains_keyword(question, PROMPT_MANIPULATION_PATTERNS):
        return False, build_rejection(
            "PROMPT_MANIPULATION",
            "Prompt manipulation attempt detected."
        )

    if matches_pattern(question, SQL_INJECTION_PATTERNS):
        return False, build_rejection(
            "SQL_INJECTION_PATTERN",
            "Possible SQL injection pattern detected."
        )

    if matches_pattern(question, SECRET_PATTERNS):
        return False, build_rejection(
            "POSSIBLE_SECRET",
            "Possible credential or private key detected. Remove secrets before continuing."
        )

    return True, "APPROVED"


if __name__ == "__main__":
    print()
    print("Balerica AI Auditor Test")
    print()

    question = input("Question> ")

    approved, message = audit_request(question)

    print(message)
