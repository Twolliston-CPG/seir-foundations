# Git Workflows

Run all commands from `~/Documents/TheoWAF/seir-foundations`

---

## Starting with a New Repo

Any time you want to work on a repo that belongs to someone else, follow these steps first:

**Step A — Fork on GitHub (browser)**
1. Go to the original repo on GitHub, e.g. `https://github.com/<original-owner>/<repo-name>`
2. Click the **Fork** button (top right)
3. Select your account (`Twolliston-CPG`) as the destination
4. GitHub creates your own copy at `https://github.com/Twolliston-CPG/<repo-name>`

**Step B — Clone your fork to your local machine (terminal)**
```bash
git clone https://github.com/Twolliston-CPG/<repo-name>.git
cd <repo-name>
```

**Step C — Add the original repo as upstream (terminal, one-time)**
```bash
git remote add upstream https://github.com/<original-owner>/<repo-name>.git
git remote -v    # verify both origin and upstream are listed
```

Then use the two workflows below. The URLs are the only things that change between repos.

---

There are two distinct workflows:

| Workflow | When to use |
|----------|-------------|
| **Workflow 1 — Push your changes** | After every lab run, screenshot, or edit — saves your work to GitHub |
| **Workflow 2 — Pull upstream updates** | When the instructor pushes new course content to the original repo |

---

# Workflow 1 — Push Your Own Changes to GitHub

Use this frequently — after completing a lab run, adding screenshots, updating notes, or making any edits you want saved to your fork.

```bash
cd ~/Documents/TheoWAF/seir-foundations
git status                          # see what changed
git add <files>                     # stage the files you want
git commit -m "your message"        # commit
git push origin main                # push to your fork on GitHub
```

> **Remotes:**
> - `origin` → your fork: `https://github.com/Twolliston-CPG/seir-foundations.git`

---

## Verify Your Work — Run After Either Workflow

Four commands to confirm everything is clean and on GitHub:

```bash
git status                          # clean working tree?
git log --oneline -5                # latest commits in history?
git remote -v                       # origin and upstream still configured?
gh api "repos/Twolliston-CPG/seir-foundations/commits" --jq '.[0:3] | .[] | {sha: .sha[:7], message: (.commit.message | split("\n")[0]), email: .commit.author.email}'   # changes on GitHub?
```

---

# Workflow 2 — Pull Updates from the Original Course Repo

Use this when the instructor pushes new content to `BalericaAI/SEIR-Foundations` and you want to bring it into your fork without losing your own changes.

Run these from `~/Documents/TheoWAF/seir-foundations`

> **Remotes:**
> - `upstream` → original repo: `https://github.com/BalericaAI/SEIR-Foundations.git`

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

## Step 3 — Review Changes Before Merging ✅ Done

```bash
git log --oneline main..upstream/main        # their new commits since your branches diverged
git diff --stat main...upstream/main         # files they changed
git diff main..upstream/main                 # full line-by-line diff
```

The three-dot form (`...`) shows only what upstream changed since your branches split.

> ⚠️ **Security review — do not skip this step.**
> You are pulling code from an external repo. Before merging, inspect any new or changed files, especially:
> - Shell scripts (`.sh`) — run on your EC2 instance
> - Python files (`.py`) — especially in `API/` or `python/`
> - Install scripts (`install.sh`) — run as root on your server
>
> `git fetch` is always safe — nothing is applied to your files until `git merge`. Use the diff commands above as your inspection step. If anything looks unexpected, read the file before merging.

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
