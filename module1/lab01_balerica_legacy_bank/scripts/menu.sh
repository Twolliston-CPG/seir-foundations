#!/usr/bin/env bash
#
# menu.sh - run a Linux command by entering its number
#
# Usage:  chmod +x menu.sh && ./menu.sh
#
# To add or change a command, edit the two lists below.
# Keep the same number in both LABELS and COMMANDS.

declare -A LABELS COMMANDS

LABELS[01]="Show current date and time";   COMMANDS[01]="date"
LABELS[02]="Show who is logged in";         COMMANDS[02]="who && whoami"
LABELS[03]="Show who is logged in";         COMMANDS[03]="pwd"
LABELS[04]="Show disk usage";               COMMANDS[04]="df -h"
LABELS[05]="Show memory usage";             COMMANDS[05]="free -h"
LABELS[06]="List files in current folder";  COMMANDS[06]="ls -la"
LABELS[07]="Show system uptime and load";   COMMANDS[07]="uptime"
LABELS[08]="Show top 10 processes by CPU";  COMMANDS[08]="ps aux --sort=-%cpu | head -n 11"
LABELS[09]="Show IP addresses";             COMMANDS[09]="ip -brief address"
LABELS[10]="Show kernel and OS info";       COMMANDS[10]="uname -a"
LABELS[11]="Ping google.com (4 times)";     COMMANDS[11]="ping -c 4 google.com"
LABELS[12]="Hostname";     COMMANDS[12]="hostname"
LABELS[13]="To see your public IPv4 address in Linux, use the curl command with an external IP-reporting service like";     COMMANDS[13]="curl -4 ifconfig.me"
LABELS[14]="Using dig (DNS query method)";     COMMANDS[14]="dig -4 @ns1-1.akamaitech.net -t a whoami.akamai.net +short
"


show_menu() {
    echo
    echo "========== Command Menu =========="
    for key in $(printf '%s\n' "${!LABELS[@]}" | sort); do
        printf "  %s) %s\n" "$key" "${LABELS[$key]}"
    done
    echo "   q) Quit"
    echo "=================================="
}

while true; do
    show_menu
    read -rp "Enter a number: " choice

    # Allow quitting
    if [[ "$choice" =~ ^[qQ]$ ]]; then
        echo "Goodbye."
        exit 0
    fi

    # Accept "1" as well as "01"
    if [[ "$choice" =~ ^[0-9]+$ ]]; then
        choice=$(printf "%02d" "$((10#$choice))")
    fi

    if [[ -n "${COMMANDS[$choice]}" ]]; then
        echo
        echo ">>> ${LABELS[$choice]}  ($ ${COMMANDS[$choice]})"
        echo "----------------------------------"
        eval "${COMMANDS[$choice]}"
        rc=$?
        echo "----------------------------------"
        echo "Exit code: $rc"
    else
        echo "Invalid choice: '$choice'. Try again."
    fi

    read -rp "Press Enter to continue..." _
done
