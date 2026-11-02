#!/usr/bin/env python3
"""
=========================================================
                    BALERICA AI
                Telemetry Library v1.0
=========================================================

SEIR Foundations

Purpose:
Collect Linux telemetry from an EC2 instance.

This module is shared by all Balerica AI agents.

Examples:

health.py
ask.py
analyze_logs.py

=========================================================
"""

import platform
import subprocess
from datetime import datetime
from urllib.request import urlopen


# ---------------------------------------------------------------------
# Chewbacca says:
#
# "Rrrrrrghhh..."
#
# Translation:
#
# One function.
# One responsibility.
#
# Small functions are easier to test,
# easier to understand,
# and easier to reuse.
# ---------------------------------------------------------------------


def run_command(command):

    """
    Execute a Linux command safely.
    """

    try:

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        return result.stdout.strip()

    except Exception as ex:

        return str(ex)


# ---------------------------------------------------------------------
# Host Information
# ---------------------------------------------------------------------


def get_hostname():

    return run_command("hostname")


def get_username():

    return run_command("whoami")


def get_os():

    return platform.platform()


def get_kernel():

    return run_command("uname -r")


def get_current_time():

    return str(datetime.now())


def get_uptime():

    return run_command("uptime")


# ---------------------------------------------------------------------
# System Resources
# ---------------------------------------------------------------------


def get_cpu():

    return run_command("top -bn1 | head -5")


def get_memory():

    return run_command("free -h")


def get_disk():

    return run_command("df -h")


# ---------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------


def get_failed_services():

    return run_command(
        "systemctl --failed --no-pager"
    )


def get_running_services():

    return run_command(
        "systemctl list-units --type=service --state=running --no-pager"
    )


# ---------------------------------------------------------------------
# Networking
# ---------------------------------------------------------------------


def get_ip_addresses():

    return run_command("hostname -I")


def get_listening_ports():

    return run_command("ss -tuln")


def get_routes():

    return run_command("ip route")


# ---------------------------------------------------------------------
# AWS Instance Metadata
#
# Uses IMDSv2 if available.
#
# Foundations Version:
# Falls back gracefully if metadata cannot be reached.
# ---------------------------------------------------------------------


def get_instance_metadata(path):

    try:

        token = subprocess.run(

            [
                "curl",
                "-s",
                "-X",
                "PUT",
                "http://169.254.169.254/latest/api/token",
                "-H",
                "X-aws-ec2-metadata-token-ttl-seconds: 21600"
            ],

            capture_output=True,
            text=True

        ).stdout.strip()

        value = subprocess.run(

            [
                "curl",
                "-s",
                "-H",
                f"X-aws-ec2-metadata-token: {token}",
                f"http://169.254.169.254/latest/meta-data/{path}"
            ],

            capture_output=True,
            text=True

        ).stdout.strip()

        return value

    except:

        return "Unavailable"


def get_instance_id():

    return get_instance_metadata("instance-id")


def get_instance_type():

    return get_instance_metadata("instance-type")


def get_availability_zone():

    return get_instance_metadata(
        "placement/availability-zone"
    )


# ---------------------------------------------------------------------
# Chewbacca says:
#
# "RRRAAAAAAGHHH!"
#
# Translation:
#
# Good engineers collect evidence once.
#
# Every AI agent can then reuse it.
# ---------------------------------------------------------------------


def collect_telemetry():

    telemetry = {

        "Hostname": get_hostname(),

        "Current User": get_username(),

        "Operating System": get_os(),

        "Kernel": get_kernel(),

        "Current Time": get_current_time(),

        "Uptime": get_uptime(),

        "CPU": get_cpu(),

        "Memory": get_memory(),

        "Disk": get_disk(),

        "Failed Services": get_failed_services(),

        "IP Addresses": get_ip_addresses(),

        "Listening Ports": get_listening_ports(),

        "Routes": get_routes(),

        "Instance ID": get_instance_id(),

        "Instance Type": get_instance_type(),

        "Availability Zone": get_availability_zone()

    }

    return telemetry


# ---------------------------------------------------------------------
# Quick Test
# ---------------------------------------------------------------------

if __name__ == "__main__":

    import json

    print(json.dumps(
        collect_telemetry(),
        indent=4
    ))

# ---------------------------------------------------------
# Chewbacca says:
#
# "Rrrrr..."
#
# Translation:
#
# Recent logs usually explain
# what just happened.
# ---------------------------------------------------------

def get_recent_journal(lines=100):

    command = (
        f"journalctl -n {lines} --no-pager"
    )

    return run_command(command)


# ---------------------------------------------------------

def get_recent_auth(lines=50):

    command = (
        f"journalctl -u sshd -n {lines} --no-pager"
    )

    return run_command(command)


# ---------------------------------------------------------

def get_recent_kernel(lines=30):

    command = (
        f"dmesg | tail -{lines}"
    )

    return run_command(command)
