import json
from incident import report_incident

incidents = [
    dict(agent="health-monitor",  severity="INFO",     message="EC2 instance health check passed",         incident_id="BAI-INFO-001",  evidence="All system services running normally",  recommendation="No action required"),
    dict(agent="disk-monitor",    severity="WARNING",  message="Disk usage at 78% on /dev/xvda1",          incident_id="BAI-WARN-001",  evidence="df -h: 78% used, 4.2GB remaining",     recommendation="Archive logs older than 30 days"),
    dict(agent="app-monitor",     severity="ERROR",    message="HTTP 500 errors spiking: 38 in 2 minutes", incident_id="BAI-ERR-001",   evidence="access.log: 38 x 500 in last 120s",    recommendation="Check application logs immediately"),
    dict(agent="memory-monitor",  severity="CRITICAL", message="Available memory below 50MB",              incident_id="BAI-CRIT-001",  evidence="free -m: 48MB available",              recommendation="Restart application services now"),
    dict(agent="cpu-monitor",     severity="CRITICAL", message="CPU at 99% — system unresponsive",         incident_id="BAI-CRIT-002",  evidence="top: 99.1% user, load avg 7.2",        recommendation="Immediate process kill or reboot"),
]

for inc in incidents:
    result = report_incident(**inc)
    print(json.dumps(result, indent=2)
    print("---")