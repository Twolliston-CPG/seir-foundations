#!/usr/bin/env python3
"""
=========================================================
                    BALERICA AI
              Amazon Bedrock Library v1.0
=========================================================

SEIR Foundations

Purpose:

Provide a simple interface for communicating with
Amazon Bedrock.

Every Balerica AI agent should import this module
instead of talking to Bedrock directly.

Example:

from bedrock import invoke_bedrock

response = invoke_bedrock(prompt)

=========================================================
"""

import boto3
import json

# ---------------------------------------------------------
# Student Challenge
#
# Replace 4.X with the Foundation Model version
# you enabled inside Amazon Bedrock.
#
# AWS Console
#
# Amazon Bedrock
# -> Model Access
#
# ---------------------------------------------------------

REGION = "us-east-1"

MODEL_ID = "anthropic.claude-sonnet-4.X"

MAX_TOKENS = 1000


# ---------------------------------------------------------
# Chewbacca says:
#
# "Rrrrrrrgh..."
#
# Translation:
#
# Build the connection once.
#
# Reuse it everywhere.
# ---------------------------------------------------------

def create_client():

    return boto3.client(

        service_name="bedrock-runtime",

        region_name=REGION

    )


# ---------------------------------------------------------
# Chewbacca says:
#
# "Raaaagh!"
#
# Translation:
#
# A bad prompt usually produces
# a bad answer.
#
# Validate your inputs.
# ---------------------------------------------------------

def validate_prompt(prompt):

    if prompt is None:

        raise ValueError("Prompt cannot be None.")

    if len(prompt.strip()) == 0:

        raise ValueError("Prompt cannot be empty.")


# ---------------------------------------------------------
# Build Request
# ---------------------------------------------------------

def build_request(prompt):

    return {

        "anthropic_version": "bedrock-2023-05-31",

        "max_tokens": MAX_TOKENS,

        "messages": [

            {

                "role": "user",

                "content": prompt

            }

        ]

    }


# ---------------------------------------------------------
# Chewbacca says:
#
# "RRRRRAAAAGH!"
#
# Translation:
#
# Computers speak JSON.
#
# Humans prefer English.
# ---------------------------------------------------------

def parse_response(response):

    body = json.loads(

        response["body"].read()

    )

    return body["content"][0]["text"]


# ---------------------------------------------------------
# Main Bedrock Function
# ---------------------------------------------------------

def invoke_bedrock(prompt):

    validate_prompt(prompt)

    client = create_client()

    print()

    print("----------------------------------------------")
    print("Amazon Bedrock")
    print("----------------------------------------------")
    print(f"Region : {REGION}")
    print(f"Model  : {MODEL_ID}")
    print("----------------------------------------------")
    print()

    request = build_request(prompt)

    response = client.invoke_model(

        modelId=MODEL_ID,

        body=json.dumps(request)

    )

    return parse_response(response)


# ---------------------------------------------------------
# Simple Test
# ---------------------------------------------------------

if __name__ == "__main__":

    print()

    print("=" * 60)
    print("             BALERICA AI")
    print("        Amazon Bedrock Test")
    print("=" * 60)

    print()

    prompt = input("Ask Bedrock something:\n\n> ")

    try:

        answer = invoke_bedrock(prompt)

        print()

        print("=" * 60)

        print(answer)

        print("=" * 60)

    except Exception as ex:

        print()

        print("Unable to communicate with Amazon Bedrock.\n")

        print("Things to verify:\n")

        print("✓ IAM Role")

        print("✓ Bedrock Model Access")

        print("✓ AWS Region")

        print("✓ Foundation Model Identifier")

        print()

        print("Technical Details:\n")

        print(ex)
