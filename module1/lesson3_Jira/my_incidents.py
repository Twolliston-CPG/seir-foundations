#!/usr/bin/env python3
"""Balerica AI incident coordinator: Jira ticket first, Slack alert second.

Run: python incident.py --dry-run | --test
Uses existing jira.py and slack.py. Never send secrets or customer data.
"""
import argparse
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
from jira import create_incident, JiraError  # noqa: E402
from slack import send_alert  # noqa: E402

# YO STUDENT: CONFIGURE JIRA AND SLACK FIRST, OR CHEWBACCA BITES YOU!
# Your .env holds the secrets. Do NOT paste webhooks or API tokens here.
STATE_DB = Path(os.getenv('INCIDENT_STATE_DB', 'data/incident_state.db'))
SEVERITIES = {'INFO', 'WARNING', 'ERROR', 'CRITICAL'}


def _db():
    STATE_DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(STATE_DB, timeout=15)
    conn.execute('''CREATE TABLE IF NOT EXISTS incidents (
        incident_id TEXT PRIMARY KEY,
        jira_key TEXT NOT NULL,
        jira_url TEXT NOT NULL,
        slack_sent INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    )''')
    conn.commit()
    return conn


def report_incident(*, agent, severity, message, incident_id,
                    evidence='', recommendation=''):
    """Create at most one Jira issue per incident_id in sequential use.

    If Slack fails, a later call with the same ID retries Slack only.
    This is a teaching implementation, not a distributed lock/queue.
    """
    if not all(isinstance(x, str) and x.strip() for x in (agent, message, incident_id)):
        raise ValueError('agent, message, and stable incident_id are required')
    severity = severity.upper().strip()
    if severity not in SEVERITIES:
        raise ValueError('Invalid severity')
    with _db() as conn:
        row = conn.execute('SELECT jira_key, jira_url, slack_sent FROM incidents WHERE incident_id=?',
                           (incident_id,)).fetchone()
        created = False
        if row is None:
            jira_result = create_incident(agent=agent, severity=severity, message=message,
                                          incident_id=incident_id, evidence=evidence,
                                          recommendation=recommendation)
            conn.execute('INSERT INTO incidents VALUES (?, ?, ?, ?, ?)',
                         (incident_id, jira_result['key'], jira_result['url'], 0,
                          datetime.now(timezone.utc).isoformat()))
            conn.commit()
            jira_key, jira_url, slack_sent = jira_result['key'], jira_result['url'], 0
            created = True
        else:
            jira_key, jira_url, slack_sent = row

        slack_status = 'already_sent' if slack_sent else 'pending'
        if not slack_sent:
            # Slack only gets a brief sanitized incident summary and a Jira link.
            # Never include raw logs, secrets, account numbers, or customer records.
            alert = f'{message[:400]}\nJira: {jira_url}\nReview ticket for details.'
            try:
                sent = send_alert(agent=agent, severity=severity, message=alert,
                                  incident_id=incident_id)
                if sent:
                    conn.execute('UPDATE incidents SET slack_sent=1 WHERE incident_id=?',
                                 (incident_id,))
                    conn.commit()
                    slack_status = 'sent'
                else:
                    slack_status = 'filtered_or_disabled'
            except Exception as exc:
                # Avoid logging exception details: upstream HTTP errors may expose URLs.
                slack_status = f'failed_{type(exc).__name__}'
        return {'incident_id': incident_id, 'jira_key': jira_key, 'jira_url': jira_url,
                'jira_created': created, 'slack_status': slack_status}


EXTRA_INCIDENTS = {
    'test2': dict(
        agent='health-monitor',
        severity='INFO',
        message='EC2 instance health check passed',
        incident_id='BAI-INFO-001',
        evidence='All services running normally',
        recommendation='No action required',
    ),
    'test3': dict(
        agent='disk-monitor',
        severity='WARNING',
        message='Disk usage at 78 percent on /dev/xvda1',
        incident_id='BAI-WARN-001',
        evidence='df -h: 78% used, 4.2GB remaining',
        recommendation='Archive logs older than 30 days',
    ),
    'test4': dict(
        agent='app-monitor',
        severity='ERROR',
        message='HTTP 500 errors spiking: 38 in 2 minutes',
        incident_id='BAI-ERR-001',
        evidence='access.log: 38 x 500 in last 120s',
        recommendation='Check application logs immediately',
    ),
    'test5': dict(
        agent='memory-monitor',
        severity='CRITICAL',
        message='Available memory below 50MB',
        incident_id='BAI-CRIT-001',
        evidence='free -m: 48MB available',
        recommendation='Restart application services now',
    ),
    'test6': dict(
        agent='cpu-monitor',
        severity='CRITICAL',
        message='CPU at 99 percent - system unresponsive',
        incident_id='BAI-CRIT-002',
        evidence='top: 99.1% user, load avg 7.2',
        recommendation='Immediate process kill or reboot',
    ),
}

def main():
    parser = argparse.ArgumentParser(
        description='Balerica AI: Jira + Slack incident workflow')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--dry-run', action='store_true',
        help='Show workflow; no API calls')
    group.add_argument(
        '--test', action='store_true',
        help='Original integration test')
    group.add_argument(
        '--test2', action='store_true',
        help='INFO: EC2 health check passed')
    group.add_argument(
        '--test3', action='store_true',
        help='WARNING: Disk usage at 78 percent')
    group.add_argument(
        '--test4', action='store_true',
        help='ERROR: HTTP 500 errors spiking')
    group.add_argument(
        '--test5', action='store_true',
        help='CRITICAL: Memory below 50MB')
    group.add_argument(
        '--test6', action='store_true',
        help='CRITICAL: CPU at 99 percent')
    args = parser.parse_args()
    if args.dry_run:
        print('EC2 -> my_incidents.py -> Jira -> Slack')
        print('--test2 INFO | --test3 WARNING | --test4 ERROR')
        print('--test5 CRITICAL | --test6 CRITICAL')
        print('No API calls made.')
        return 0
    if args.test:
        ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
        inc = dict(
            agent='my_incidents.py',
            severity='ERROR',
            message='SEIR Foundations integration test',
            incident_id='SEIR-TEST-' + ts,
            evidence='Synthetic test only; no customer data',
            recommendation='Confirm Jira issue and Slack message.',
        )
    else:
        flags = ['test2','test3','test4','test5','test6']
        flag = next(f for f in flags if getattr(args, f))
        inc = EXTRA_INCIDENTS[flag]
    try:
        result = report_incident(**inc)
        print(json.dumps(result, indent=2))
        ok = result['slack_status'] in ('sent', 'already_sent')
        return 0 if ok else 1
    except (JiraError, ValueError, OSError, sqlite3.Error) as exc:
        print(f'Incident failed: {type(exc).__name__}.')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())