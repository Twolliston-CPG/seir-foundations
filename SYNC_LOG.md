# Sync Log

History of upstream sync runs. Add a new entry each time you run Workflow 2.

---

## 2026-11-27

**Step 2 — Pull Updates**
Fetched upstream. 1 new commit since last merge: `fcaca27` — "Fix route-table inventory query so VPC teardown can actually delete custom route tables (#30)".

**Step 3 — Review Changes**
Reviewed the upstream fix. Upstream PR #30 addresses the same JMESPath negation bug we independently discovered and patched in commit `a30cf13` today. Our fix uses an equivalent approach. No new course content.

**Step 4 — Merge**
Not merged. Our route table fix (`a30cf13`) is equivalent to upstream's. Will merge upstream on the next content update to avoid a spurious conflict.

---

## 2026-11-26

**One-Time Setup**
`upstream` remote configured and pointing to `https://github.com/BalericaAI/SEIR-Foundations.git`.

**Step 1 — Get Ready**
Confirmed on `main`. Uncommitted changes were stashed before proceeding.

**Step 2 — Pull Updates**
Fetched all branches from upstream. 98 new commits downloaded.

**Step 3 — Review Changes**
Reviewed 98 upstream commits. 162 files changed. Confirmed no critical conflicts with local work before merging.

**Step 4 — Merge**
Merge complete. One conflict in root `README.md` resolved by keeping both versions. `module1/lesson1_ec2/README.md` (707 lines) preserved. Changes pushed to `origin/main` with `git push --force origin main` after rewriting commit history to replace personal email with GitHub noreply address.
