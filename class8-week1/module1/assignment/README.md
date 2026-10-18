# Class 8 Week 1 Assignment – EC2 Implementation

Launch an EC2 instance from an existing launch template, connect to it over SSH and run basic Linux commands, then launch a second instance whose **user data** script builds a 3-page website with a dynamic calculator page.

---

## Contents

- [Prerequisites](#prerequisites)
- [Part A – Launch and use lab0-ec2-4](#part-a--launch-and-use-lab0-ec2-4)
- [Part B – Website from a user data script](#part-b--website-from-a-user-data-script)
- [Troubleshooting](#troubleshooting)
- [Cleanup](#cleanup)
- [Deliverables checklist](#deliverables-checklist)

---

## Prerequisites

- AWS account with permission to launch EC2 instances and use launch templates
- Launch template **`lab0-template`** in your working region
- The `.pem` key pair the template uses, saved locally (e.g. `~/.ssh/lab0-key.pem`)
- Security group inbound rules:
  - **SSH (TCP 22)** from `0.0.0.0/0`
  - **HTTP (TCP 80)** from `0.0.0.0/0` (Part B only)
- **Terminal** (macOS) or **Git Bash** (Windows)

> **Assumption:** the template uses **Amazon Linux 2023** — SSH user `ec2-user`, package manager `dnf`.
> On Ubuntu, use `ubuntu` and `apt` instead.

---

## Part A – Launch and use lab0-ec2-4

### Task 1 – Launch lab0-ec2-4 from lab0-template

1. In the AWS Console, select the region where `lab0-template` lives.
2. Go to **EC2 → Instances → Launch Templates** and select `lab0-template`.
3. **Actions → Launch instance from template** (keep the default version).
4. Confirm key pair, subnet (public, auto-assign public IP) and security group (SSH 22 from My IP).
5. **Launch instance → View all instances**.
6. Wait for **Running** and **2/2 checks passed**; copy the **Public IPv4 address**.

### Task 2 – Prepare your key file

```bash
cd ~/.ssh
chmod 400 lab0-key.pem    #only if this is the first time using key pair
```

> Git Bash: if SSH still says the key is "too open", copy it into `~/.ssh/` and run `chmod 400` there.

### Task 3 – Connect with SSH

```bash
ssh -i lab0-key.pem ec2-user@13.222.197.100
```

Type `yes` to trust the host. Success looks like `[ec2-user@ip-172-31-44-149 ~]$`.
Tip: **Instance → Connect → SSH client** shows the exact command for your instance.

### Task 4 – Run the required commands

```bash
echo "Hello, World!" > hello.txt    # create a text 
cat hello.txt                        # -> Hello, World!
  Hello, World!
mkdir new_project && cd new_project  # make a folder and move into it
pwd                                  # -> /home/ec2-user/new_project
  /home/ec2-user/new_project/new_project
ls -l ~                              # long listing of the home directory
  total 4
  -rw-r--r--. 1 ec2-user ec2-user 14 Oct 18 03:35 hello.txt
  drwxr-xr-x. 3 ec2-user ec2-user 42 Oct 18 03:59 new_project
```

`ls -l ~` should show `hello.txt` (`-rw-...`) and `new_project` (`drwx...`).

### Task 5 – Try commands of your own

| Command | What it does | Results |
| --- | --- | --- |
| `whoami` | Logged-in user (`ec2-user`) | ec2-user |
| `hostname -I` | Instance's private IP | 172.31.40.122 |
| `uname -a` | Kernel and OS details | Linux ip-172-31-40-122.ec2.internal 6.18.54-121.166.amzn2023.x86_64 #2 SMP PREEMPT_DYNAMIC Tue Oct  6 23:11:34 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux |
| `uptime` | Time running and load average |  04:07:05 up 59 min,  1 user,  load average: 0.00, 0.00, 0.00 |
| `df -h` | Disk usage, human-readable | Filesystem      Size  Used Avail Use% Mounted on|
|||devtmpfs        4.0M     0  4.0M   0% /dev |
|||tmpfs           479M     0  479M   0% /dev/shm |
|||tmpfs           192M  448K  192M   1% /run |
|||/dev/xvda1      8.0G  1.6G  6.4G  20% / |
|||tmpfs           479M     0  479M   0% /tmp  |
|||/dev/xvda128     10M  1.3M  8.7M  13% /boot/efi |
|||tmpfs            96M     0   96M   0% /run/user/1000   |
| `free -h` | Memory usage |                total        used        free      shared  buff/cache   available|
|||Mem:           957Mi       147Mi       560Mi       0.0Ki       249Mi       677Mi |
|||Swap:             0B          0B          0B   |   
| `exit` | |End the SSH session |

### Task 6 – Screenshot and group discussion

1. Screenshot your SSH prompt plus the output of `cat hello.txt`, `pwd` and `ls -l ~`
   (macOS: `Cmd+Shift+4` · Windows: `Win+Shift+S`).
2. Share it with your group and walk through what you did.
3. Discuss:
   - Errors you hit (key permissions, timeouts, wrong username) and how you fixed them
   - Other ways to connect: EC2 Instance Connect, Session Manager, PuTTY, VS Code Remote-SSH
   - What the launch template saved you from configuring

---

## Part B – Website from a user data script

The script installs Apache and PHP and creates three pages:

A bash **user data** script that turns a fresh Amazon EC2 instance into a small working website. It runs once at first boot, installs Apache and PHP, and builds a three-page site.

## Pages

| Page | File | Type | What it does |
| --- | --- | --- | --- |
| Home | `index.html` | Static | Shows the instance's **Instance ID** and **Availability Zone** |
| About | `about.html` | Static | Describes the site and its stack |
| Calculator | `calculator.php` | **Dynamic** | Adds, subtracts, multiplies or divides two numbers on the server with PHP |

All three pages share a nav bar and `style.css`.

### Static vs. dynamic

- **Static** pages are plain HTML files. Apache sends them to the browser exactly as they are saved on disk.
- The **dynamic** page is PHP. Each time you submit the form, the server runs the code, does the math, and builds a new HTML page with the answer. The page also shows the server's hostname and the time it was generated, so you can see it's built fresh on every request.

The home page is static, but the script fills in the Instance ID and AZ when it creates the file at boot. Every instance therefore serves its own values.

### Task 7 – The user data script (`userdata.sh`)

```bash
#!/bin/bash
# EC2 User Data – Apache + PHP site with 3 pages
# Tested target: Amazon Linux 2023 (uses dnf). Runs as root at first boot.
# Log: /var/log/cloud-init-output.log

set -euxo pipefail

# ---------- 1. Install Apache + PHP ----------
dnf update -y
dnf install -y httpd php

systemctl enable --now httpd

# ---------- 2. Get instance metadata (IMDSv2) ----------
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
INSTANCE_ID=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/instance-id)
AZ=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/placement/availability-zone)

WEBROOT=/var/www/html

# ---------- 3. Shared stylesheet ----------
cat > $WEBROOT/style.css <<'EOF'
body { font-family: Arial, sans-serif; margin: 0; background: #f4f6f8; color: #222; }
nav { background: #232f3e; padding: 14px 20px; }
nav a { color: #ff9900; margin-right: 18px; text-decoration: none; font-weight: bold; }
nav a:hover { text-decoration: underline; }
main { max-width: 700px; margin: 30px auto; background: #fff; padding: 24px 30px;
       border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,.1); }
table { border-collapse: collapse; }
td { padding: 6px 12px; border: 1px solid #ddd; }
input, select, button { padding: 6px; font-size: 1rem; margin: 4px; }
button { background: #ff9900; border: none; border-radius: 4px; cursor: pointer; }
.result { font-size: 1.4rem; margin-top: 16px; color: #1a7f37; }
.error  { font-size: 1.1rem; margin-top: 16px; color: #c62828; }
EOF

# ---------- 4. Home page (static, metadata baked in at boot) ----------
cat > $WEBROOT/index.html <<EOF
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Home</title><link rel="stylesheet" href="style.css"></head>
<body>
<nav><a href="index.html">Home</a><a href="about.html">About</a><a href="calculator.php">Calculator</a></nav>
<main>
  <h1>Welcome to my EC2 Website</h1>
  <p>This page is being served by Apache on the following instance:</p>
  <table>
    <tr><td><b>Instance ID</b></td><td>${INSTANCE_ID}</td></tr>
    <tr><td><b>Availability Zone</b></td><td>${AZ}</td></tr>
  </table>
</main>
</body>
</html>
EOF

# ---------- 5. About page (static) ----------
cat > $WEBROOT/about.html <<'EOF'
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>About</title><link rel="stylesheet" href="style.css"></head>
<body>
<nav><a href="index.html">Home</a><a href="about.html">About</a><a href="calculator.php">Calculator</a></nav>
<main>
  <h1>About This Site</h1>
  <p>This website was built automatically by an EC2 <b>user data</b> script at launch.</p>
  <ul>
    <li><b>Home</b> – static HTML showing the instance ID and Availability Zone</li>
    <li><b>About</b> – static HTML (this page)</li>
    <li><b>Calculator</b> – dynamic PHP page; the math is done on the server</li>
  </ul>
  <p>Stack: Amazon Linux 2023, Apache (httpd), PHP.</p>
</main>
</body>
</html>
EOF

# ---------- 6. Calculator (dynamic PHP) ----------
cat > $WEBROOT/calculator.php <<'EOF'
<?php
$a = $_POST['a'] ?? '';
$b = $_POST['b'] ?? '';
$op = $_POST['op'] ?? '+';
$result = null;
$error = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!is_numeric($a) || !is_numeric($b)) {
        $error = "Please enter two valid numbers.";
    } else {
        $x = (float)$a; $y = (float)$b;
        switch ($op) {
            case '+': $result = $x + $y; break;
            case '-': $result = $x - $y; break;
            case '*': $result = $x * $y; break;
            case '/':
                if ($y == 0) { $error = "Cannot divide by zero."; }
                else { $result = $x / $y; }
                break;
            default: $error = "Unknown operation.";
        }
    }
}
$symbols = ['+' => '+', '-' => '−', '*' => '×', '/' => '÷'];
function h($s) { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
?>
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Calculator</title><link rel="stylesheet" href="style.css"></head>
<body>
<nav><a href="index.html">Home</a><a href="about.html">About</a><a href="calculator.php">Calculator</a></nav>
<main>
  <h1>Server-Side Calculator</h1>
  <p>Enter two numbers. PHP on <b><?= h(gethostname()) ?></b> computes the answer.</p>
  <form method="post">
    <input type="text" name="a" value="<?= h($a) ?>" placeholder="First number" required>
    <select name="op">
      <?php foreach ($symbols as $val => $label): ?>
        <option value="<?= h($val) ?>" <?= $op === $val ? 'selected' : '' ?>><?= $label ?></option>
      <?php endforeach; ?>
    </select>
    <input type="text" name="b" value="<?= h($b) ?>" placeholder="Second number" required>
    <button type="submit">=</button>
  </form>
  <?php if ($error): ?>
    <div class="error"><?= h($error) ?></div>
  <?php elseif ($result !== null): ?>
    <div class="result"><?= h($a) ?> <?= $symbols[$op] ?> <?= h($b) ?> = <b><?= h(round($result, 6)) ?></b></div>
  <?php endif; ?>
  <p style="margin-top:24px;color:#666;font-size:.9rem">Generated at <?= date('Y-m-d H:i:s T') ?></p>
</main>
</body>
</html>
EOF

# ---------- 7. Permissions + restart ----------
chown -R apache:apache $WEBROOT
chmod -R 755 $WEBROOT
systemctl restart httpd
```

> **Heredoc note:** `<<'EOF'` (quoted) writes text exactly as typed, so PHP's `$` variables survive.
> The Home page uses `<<EOF` (unquoted) so the shell fills in `${INSTANCE_ID}` and `${AZ}`.

## Requirements

- **AMI:** Amazon Linux 2023 (the script uses `dnf` and the `apache` user)
- **Instance type:** any. `t2.micro` / `t3.micro` (free tier) is fine.
- **Security group:** inbound **HTTP, TCP 80** from your IP or `0.0.0.0/0`
- **Network:** a public subnet with auto-assign public IP, so you can reach the site from a browser

### Task 8 – Launch the web server instance

1. **EC2 → Launch Templates → `lab0-template` → Actions → Launch instance from template**.
2. Add tag `Name` = `lab0-web-1`.
3. Make sure the security group allows **HTTP 80** from `0.0.0.0/0` (and SSH 22 from My IP).
4. **Advanced details → User data** → paste the whole script (`#!/bin/bash` must be line 1).
5. Launch, wait for **2/2 checks passed**, then ~2–3 more minutes for the script to finish.

### Task 9 – Open the website

Browse to `http://<PUBLIC_IP>` — type **`http://`**, not `https://`.
Confirm Home shows the Instance ID and AZ, and the nav reaches About and Calculator.

### Task 10 – Test the dynamic page

| Input | Expected result |
| --- | --- |
| `12 + 30` | `12 + 30 = 42` |
| `7.5 * 4` | `7.5 * 4 = 30` |
| `10 / 0` | "Cannot divide by zero." |
| `abc + 5` | "Please enter two valid numbers." |

The server time changes on every submit — proof the page is generated by the server.

### Task 11 – Verify from inside the instance (optional)

```bash
sudo tail -n 30 /var/log/cloud-init-output.log   # output of the user data script
systemctl status httpd php-fpm --no-pager         # both: active (running)
ls -l /var/www/html                               # index.html, about.html, calculator.php, style.css
curl -s localhost | head                          # fetch the home page locally
```

---


### AWS CLI alternative

```bash
aws ec2 run-instances \
  --image-id <al2023-ami-id> \
  --instance-type t3.micro \
  --key-name <your-key> \
  --security-group-ids <sg-with-port-80-open> \
  --subnet-id <public-subnet-id> \
  --associate-public-ip-address \
  --user-data file://user-data.sh
```

## What the script does

1. Updates the OS and installs `httpd` (Apache) and `php`.
2. Enables and starts Apache.
3. Requests an **IMDSv2** token and uses it to read `instance-id` and `placement/availability-zone` from the metadata service at `169.254.169.254`.
4. Writes `style.css`, `index.html`, `about.html` and `calculator.php` to `/var/www/html`.
5. Sets file ownership to `apache` and restarts Apache.

## Testing the calculator

1. Open `http://<public-ip>/calculator.php`.
2. Enter two numbers, pick `+`, `−`, `×` or `÷`, and press **=**.
3. The answer appears below the form.

The page rejects input that isn't a number and shows an error if you divide by zero.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `UNPROTECTED PRIVATE KEY FILE` | Key readable by others | `chmod 400 your-key.pem` |
| SSH `Connection timed out` | Port 22 closed or no public IP | SG inbound SSH 22 from My IP; public subnet with auto-assign IP |
| `Permission denied (publickey)` | Wrong key or username | Template's key; `ec2-user` (AL2023) / `ubuntu` (Ubuntu) |
| Website won't load | Port 80 closed, or browser forced https | Add HTTP 80 from `0.0.0.0/0`; type `http://` |
| Calculator downloads or shows raw PHP | php-fpm not running | `sudo systemctl enable --now php-fpm && sudo systemctl restart httpd` |
| Blank Instance ID on Home | Metadata call failed | Check `/var/log/cloud-init-output.log`; site still works |
| Script didn't run | No `#!/bin/bash` on line 1, or added after first boot | Fix and launch a new instance (user data runs on first boot only) |
| Metadata `curl` returns 401 | IMDSv2 needs a token | `TOKEN=$(curl -s -X PUT http://169.254.169.254/latest/api/token -H "X-aws-ec2-metadata-token-ttl-seconds: 300")` then add `-H "X-aws-ec2-metadata-token: $TOKEN"` |

| Nothing works | SSH in and run the commands below. |  |

```bash
sudo tail -50 /var/log/cloud-init-output.log   # full log of the script (it runs with set -x)
sudo systemctl status httpd                    # is Apache running?
ls -l /var/www/html                            # were the pages created?
```

User data runs **only on first boot**. To rerun it after editing, launch a new instance.

## Load-balancing demo

1. Launch two or more instances with this script, preferably in different Availability Zones.
2. Register them in a target group behind an **Application Load Balancer**.
3. Open the load balancer's DNS name and refresh the home page.

The Instance ID and AZ change as the load balancer sends requests to different instances.

---

## Cleanup

After review, select `lab0-ec2-4` and `lab0-web-1` → **Instance state → Terminate** to avoid charges.
Keep the launch template and key pair for future labs.

---

## Deliverables checklist

- [ ] `lab0-ec2-4` launched from `lab0-template` and running
- [ ] Connected over SSH from Terminal / Git Bash
- [ ] Ran `echo`, `cat`, `mkdir && cd`, `pwd`, `ls -l ~`
- [ ] Ran at least 3 commands of my own
- [ ] Screenshot shared and discussed with the group
- [ ] User data script written (3 pages, 1 dynamic)
- [ ] Web instance launched; Home, About and Calculator all load
- [ ] Calculator tested, including divide-by-zero
- [ ] Instances terminated after review
