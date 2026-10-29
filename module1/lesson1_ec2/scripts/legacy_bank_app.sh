#!/usr/bin/env bash
#
# legacy_bank_app.sh - run a Linux command by entering its number
#
# Usage:  chmod +x legacy_bank_app.sh && ./legacy_bank_app.sh
#
# To add or change a command, edit the two lists below.
# Keep the same number in both LABELS and COMMANDS.

declare -A LABELS COMMANDS

LABELS[01]="Prove you're really there. Run whoami, pwd";   COMMANDS[01]=" whoami && timedatectl show -p Timezone --value && date && ec2-metadata -i && uptime -p"
LABELS[02]="Get the course code with git";   COMMANDS[02]="sudo dnf install -y git"
LABELS[03]="Now clone the course repository";         COMMANDS[03]="git clone https://github.com/BalericaAI/SEIR-Foundations.git"
LABELS[04]="Look at what you just downloaded";               COMMANDS[04]="ls SEIR-Foundations"
LABELS[05]="Run the installer";             COMMANDS[05]="bash SEIR-Foundations/module1/lesson1_ec2/API/install/install.sh"
LABELS[06]="The installer built your bank at /opt/balerica-bank. Go there";  COMMANDS[06]="cd /opt/balerica-bank"
LABELS[07]="Look around";   COMMANDS[07]="ls"
LABELS[08]="Now run your first COBOL program. It looks up account 100001 in the bank's ledger";  COMMANDS[08]="./cobol/bin/account_lookup 100001"
LABELS[09]="Every program leaves behind a number when it finishes. Ask for the last one";             COMMANDS[09]="echo $?"
LABELS[10]="0 means success. Now look up an account that does not exist, and check the number again";       COMMANDS[10]="./cobol/bin/account_lookup 999999
echo $?"
LABELS[11]="Post your first payment";     COMMANDS[11]="./cobol/bin/payment_post TXN0001 100001 125.50 USD INV-1001"
LABELS[12]="Look at the journal the COBOL program just wrote:";   COMMANDS[12]="cat data/payments.dat"
LABELS[13]="Start the bank's web API";   COMMANDS[13]="cd /opt/balerica-bank
source venv/bin/activate"
LABELS[14]="Start the web server";   COMMANDS[14]="uvicorn app.main:app --host 0.0.0.0 --port 8000"
LABELS[15]="Look around";   COMMANDS[15]="curl http://127.0.0.1:8000/status"
LABELS[16]="And run the most sophisticated diagnostic in enterprise computing:";   COMMANDS[16]="curl http://127.0.0.1:8000/chewbacca"
LABELS[17]="Prove connectivity with SWIFT traffic";   COMMANDS[17]="cd /opt/balerica-bank
python3 swift/traffic_generator.py --count 10"
LABELS[18]="Want to see the raw SWIFT messages?";   COMMANDS[18]="python3 swift/traffic_generator.py --count 3 --show-mt103"
# LABELS[06]="Look around";   COMMANDS[06]="ls"
# LABELS[06]="Look around";   COMMANDS[06]="ls"
# LABELS[06]="Look around";   COMMANDS[06]="ls"


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
