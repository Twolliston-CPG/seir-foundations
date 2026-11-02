#!/usr/bin/env python3
"""
=========================================================
                    BALERICA AI
                Banner Library v1.0
=========================================================

SEIR Foundations

Purpose

Display a common banner for every Balerica AI
agent.

Every agent should begin with:

from banner import show_banner

=========================================================
"""

import os
import random
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------
# Chewbacca says:
#
# "Rrrrrrrrrgh..."
#
# Translation:
#
# First impressions matter.
#
# Engineers appreciate good tools.
# ---------------------------------------------------------


COURSE = "SEIR Foundations"

REGION = os.getenv("AWS_REGION", "Unknown")

MODEL = os.getenv(
    "BEDROCK_MODEL_ID",
    "Not Configured"
)


# ---------------------------------------------------------
# Motivational Messages
# ---------------------------------------------------------

MESSAGES = [

    "Trust telemetry. Question assumptions.",

    "Logs tell stories. Learn to read them.",

    "Every engineer started somewhere.",

    "Small improvements become great systems.",

    "Good engineers verify evidence.",

    "One command at a time.",

    "Every expert once asked how to save in vi.",

    "Cloud engineering is learned by building.",

    "Today's mistake becomes tomorrow's experience.",

    "Engineers solve problems. AI helps."

]


# ---------------------------------------------------------
# Chewbacca Wisdom
# ---------------------------------------------------------

CHEWBACCA = [

    (
        "Rrrrrrrgh...",
        "Gather evidence before making conclusions."
    ),

    (
        "Raaaaagh!",
        "Logs usually know what happened."
    ),

    (
        "RRRRRRAAAGH!",
        "Don't fear Linux. Learn Linux."
    ),

    (
        "Rrrrr...",
        "One function. One responsibility."
    ),

    (
        "Rrrrrrghhh...",
        "Read the error before changing the code."
    )

]


# ---------------------------------------------------------
# Divider
# ---------------------------------------------------------

def divider():

    print("=" * 60)


# ---------------------------------------------------------
# Section
# ---------------------------------------------------------

def section(title, value):

    print(f"{title:<20}: {value}")


# ---------------------------------------------------------
# Banner
# ---------------------------------------------------------

def show_banner(

        agent_name,

        version="1.0"

):

    message = random.choice(MESSAGES)

    chewie = random.choice(CHEWBACCA)

    print()

    divider()

    print("                     BALERICA AI")

    divider()

    print()

    section("Agent", agent_name)

    section("Course", COURSE)

    section("Version", version)

    section("Region", REGION)

    section("Foundation Model", MODEL)

    section(
        "Started",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    print()

    divider()

    print()

    print("Today's Mission")

    print()

    print(f"   {message}")

    print()

    divider()

    print()

    print("Chewbacca says...")

    print()

    print(f'   "{chewie[0]}"')

    print()

    print("Translation")

    print()

    print(f"   {chewie[1]}")

    print()

    divider()

    print()


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

def show_footer():

    print()

    divider()

    print("Analysis Complete.")

    print()

    print("Remember")

    print()

    print("AI provides recommendations.")

    print("Engineers verify evidence.")

    print()

    divider()

    print()


# ---------------------------------------------------------
# Test
# ---------------------------------------------------------

if __name__ == "__main__":

    show_banner(

        agent_name="Banner Test",

        version="1.0"

    )

    show_footer()
