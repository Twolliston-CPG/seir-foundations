# Syncing Updates from the Original Repo

Use this workflow to pull down changes from the original upstream repo into your fork without losing your own changes.

Run these from `~/Documents/TheoWAF/seir-foundations`

---

## One-Time Setup ✅ Done

Add the original repo as the `upstream` remote. You only need to do this once.

```bash
git remote add upstream https://github.com/BalericaAI/SEIR-Foundations.git
```

Verify it was added:

```bash
git remote -v
```

> **Status:** `upstream` remote is configured and pointing to `https://github.com/BalericaAI/SEIR-Foundations.git`.

---

## Step 1 — Get Ready ✅ Done

```bash
cd ~/Documents/TheoWAF/seir-foundations
git checkout main
git status -sb
```

Should be clean with no ahead/behind. If you have uncommitted work, stash or commit it first:

```bash
git stash
# or
git add <files> && git commit -m "your message"
```

> **Status:** Confirmed on `main`. Uncommitted changes were stashed before proceeding.

---

## Step 2 — Pull Updates from the Original Repo ✅ Done

```bash
git fetch upstream
```

This only downloads their changes into `upstream/*`. It does not change your files.

> **Status:** Fetched all branches from upstream. 98 new commits downloaded.

---

## Step 3 — See the Differences Before Merging ✅ Done

```bash
git log --oneline main..upstream/main        # their new commits since your branches diverged
git diff --stat main...upstream/main         # files they changed
git diff main..upstream/main                 # full line-by-line diff
```

The three-dot form (`...`) shows only what upstream changed since your branches split.

> **Status:** Reviewed 98 upstream commits. 162 files changed. Confirmed no critical conflicts with local work before merging.

---

## Step 4 — Merge Their Changes into Yours ✅ Done

```bash
git merge --allow-unrelated-histories upstream/main
```

Git keeps your changes and brings in theirs. If there are conflicts, Git will flag them so you can resolve file by file, then:

```bash
git add <resolved-files>
git commit
```

> **Status:** Merge complete. One conflict in root `README.md` resolved by keeping both versions. `module1/lesson1_ec2/README.md` (707 lines) preserved. Changes pushed to `origin/main` with `git push --force origin main` after rewriting commit history to replace personal email with GitHub noreply address.
