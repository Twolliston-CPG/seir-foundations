# Lesson 3 Notes — Tim Wolliston
**Space:** SEIR-Saga_TimWolliston / SST  
**BAI Project:** wollistonedu.atlassian.net / BAI  

---

## BAM Extra Credit

### Instance IDs (from terminal screenshots)

| BAM item | EC2 Instance ID |
|----------|----------------|
| BAM_5.6 | i-0c4e9d5802bb2e6be |

---

### BAM_5.5 — Integration flow explanation

The full incident pipeline starts in `incident.py`, which acts as the coordinator between Jira and Slack. When `report_incident()` is called, it checks the local SQLite database (`data/incident_state.db`) for the incident_id — if no row exists, it calls `create_incident()` in `jira.py` first to open a Jira ticket and records the returned issue key and URL in the database. Only after the Jira ticket is confirmed does the pipeline call `send_alert()` in `slack.py`, passing the Jira issue URL as part of the alert message so the on-call engineer can jump directly to the ticket. Jira is called before Slack because the Slack message is meant to include the Jira link — posting to Slack first would mean sending an alert with no ticket to investigate. I verified both results by opening the Jira issue from the printed URL and confirming the same ticket appeared in the `#balerica-alerts` Slack channel with a working link.

**Troubleshooting note:** During initial setup, `jira.py --verify` returned HTTP 404 on `GET /rest/api/3/project/BAI`. After confirming the site URL and project key were correct, I ran `GET /rest/api/3/myself` and received 401, which revealed the API token was invalid. I created a fresh plain (unscoped) API token at `id.atlassian.com`, updated `JIRA_API_TOKEN` in `.env` using `read -rs NEWTOKEN && sed -i`, and `--verify` succeeded on the next run.

---

### BAM_5.6 — Duplicate detection proof

**Where the incident ID is stored:**  
`incident.py` maintains a SQLite database at the path set by `INCIDENT_STATE_DB` (default: `data/incident_state.db`). The table `incidents` has `incident_id` as the primary key. When `report_incident()` is called, it first queries `SELECT jira_key, jira_url, slack_sent FROM incidents WHERE incident_id=?`. If a row is found, no new Jira ticket is created — the existing key and URL are returned instead.

**What would happen with a different ID:**  
If `bam_dup_check.py` were run with a different `incident_id` (for example, `BAM-DUP-TW-002` instead of `BAM-DUP-TW-001`), the lookup would find no matching row and `create_incident()` would be called, opening a brand-new Jira ticket. Each unique incident_id maps to exactly one ticket. This is by design: stable IDs prevent alert storms from flooding Jira with duplicate tickets for the same underlying problem, while a genuinely new incident (new ID) always gets its own ticket.

**Proof of deduplication:**  
Both runs of `python3 bam_dup_check.py` returned the same Jira issue key. The second run showed `jira_created: false`, confirming the existing row was found in the database and no second ticket was opened.
