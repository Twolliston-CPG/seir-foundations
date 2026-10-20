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

📸 **Screenshot [`assignment-01-EC2_Instance.png`](screenshots/assignment-01-EC2_Instance.png):** the instance details page showing the instance named `lab0-ec2-4`.

### Task 2 – Prepare your key file

```bash
cd ~/.ssh
chmod 400 lab0-key.pem    #only if this is the first time using key pair
```

> Git Bash: if SSH still says the key is "too open", copy it into `~/.ssh/` and run `chmod 400` there.

### Task 3 – Connect with SSH

```bash
ssh -i lab0-key.pem ec2-user@54.174.21.29
```

Type `yes` to trust the host. Success looks like `[ec2-user@ip-172-31-43-96 ~]$`.
Tip: **Instance → Connect → SSH client** shows the exact command for your instance.

📸 **Screenshot `assignment-02-ssh_connection.png`:** of the terminal showing the commands used to connect to ec2 instance using the ssh connection method.

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

📸 **Screenshot [`assignment-03-required_commands.png`](screenshots/assignment-03-required_commands.png):** of the terminal showing the required commands to run in the terminal of the ec2 instance named `lab0-ec2-4


### Task 5 – Try commands of your own

| Command | What it does | Results |
| --- | --- | --- |
| `whoami` | Logged-in user (`ec2-user`) | ec2-user |
| `hostname -I` | Instance's private IP | 172.31.43.96 |
| `uname -a` | Kernel and OS details | Linux ip-172-31-43-96.ec2.internal 6.18.54-121.166.amzn2023.x86_64 #2 SMP PREEMPT_DYNAMIC Tue Oct  6 23:11:34 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux |
| `uptime` | Time running and load average |  01:00:44 up 2:22,  1 user,  load average: 0.00, 0.00, 0.00 |
| `df -h` | Disk usage, human-readable | Filesystem      Size  Used Avail Use% Mounted on|
|||devtmpfs        4.0M     0  4.0M   0% /dev |
|||tmpfs           479M     0  479M   0% /dev/shm |
|||tmpfs           192M  448K  192M   1% /run |
|||/dev/xvda1      8.0G  1.6G  6.3G  22% / |
|||tmpfs           479M     0  479M   0% /tmp  |
|||/dev/xvda128     10M  1.3M  8.7M  13% /boot/efi |
|||tmpfs            96M     0   96M   0% /run/user/1000   |
| `free -h` | Memory usage |                total        used        free      shared  buff/cache   available|
|||Mem:           957Mi       169Mi       318Mi       3.0mi       469Mi       677Mi |
|||Swap:             0B          0B          0B   |   
| `exit` | |End the SSH session |

### Task 6 – Screenshot and group discussion

1. Screenshot your SSH prompt plus the output of `cat hello.txt`, `pwd` and `ls -l ~`
   (macOS: `Cmd+Shift+4` · Windows: `Win+Shift+S`).

📸 **Screenshot [`assignment-04-try_commands_of_your_own.png`](screenshots/assignment-04-try_commands_of_your_own.png):** of the terminal showing the commands you ran on your own.

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

assignment/scripts/class8_wk1_assignment_ec2_userdata.sh

> **Heredoc note:** `<<'EOF'` (quoted) writes text exactly as typed, so PHP's `$` variables survive.
> The Home page uses `<<EOF` (unquoted) so the shell fills in `${INSTANCE_ID}` and `${AZ}`.

---

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

📸 **Screenshot `assignment-05-index.html.png`:** the index webpage.

📸 **Screenshot `assignment-06-about.html.png`:** the about webpage.

📸 **Screenshot `assignment-07-calculator.php.png`:** the calculator webpage.

### Task 10 – Test the dynamic page

| Input | Expected result |
| --- | --- |
| `12 + 30` | `12 + 30 = 42` |
| `7.5 * 4` | `7.5 * 4 = 30` |
| `10 / 0` | "Cannot divide by zero." |
| `abc + 5` | "Please enter two valid numbers." |

The server time changes on every submit — proof the page is generated by the server.

📸 **Screenshot [`assignment-08-calculator.php.png`](screenshots/assignment-08-calculator.php.png):** the calculator webpage.

📸 **Screenshot [`assignment-09-calculator.php.png`](screenshots/assignment-09-calculator.php.png):** the calculator webpage.

📸 **Screenshot [`assignment-10-calculator.php.png`](screenshots/assignment-10-calculator.php.png):** the calculator webpage.

📸 **Screenshot [`assignment-11-calculator.php.png`](screenshots/assignment-11-calculator.php.png):** the calculator webpage.


### Task 11 – Verify from inside the instance (optional)

```bash
sudo tail -n 30 /var/log/cloud-init-output.log   # output of the user data script
systemctl status httpd php-fpm --no-pager         # both: active (running)
ls -l /var/www/html                               # index.html, about.html, calculator.php, style.css
curl -s localhost | head                          # fetch the home page locally
```
📸 **Screenshot [`assignment-12-instance_commands.png`](screenshots/assignment-12-instance_commands.png):** the calculator webpage.

📸 **Screenshot [`assignment-13-instance_commands`](screenshots/assignment-13-instance_commands.png):** the calculator webpage.

📸 **Screenshot [`assignment-14-instance_commands`](screenshots/assignment-14-instance_commands.png):** the calculator webpage.

📸 **Screenshot [`assignment-15-instance_commands`](screenshots/assignment-15-instance_commands.png):** the calculator webpage.

---

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

📸 **Screenshot [`assignment-08-calculator.php.png`](screenshots/assignment-08-calculator.php.png):** the calculator webpage.

📸 **Screenshot [`assignment-09-calculator.php.png`](screenshots/assignment-09-calculator.php.png):** the calculator webpage.

📸 **Screenshot [`assignment-10-calculator.php.png`](screenshots/assignment-10-calculator.php.png):** the calculator webpage.

📸 **Screenshot [`assignment-11-calculator.php.png`](screenshots/assignment-11-calculator.php.png):** the calculator webpage.

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

## Cleanup

After review, select `lab0-ec2-4` and `lab0-web-1` → **Instance state → Terminate** to avoid charges.
Keep the launch template and key pair for future labs.

📸 **Screenshot [`assignment-16-EC2-Instance_terminated.png`](screenshots/assignment-16-EC2-Instance_terminated.png):** the instance details page showing the instance named `lab0-ec2-4` terminated.

---

## Deliverables checklist

- [x] `lab0-ec2-4` launched from `lab0-template` and running
- [x] Connected over SSH from Terminal / Git Bash
- [x] Ran `echo`, `cat`, `mkdir && cd`, `pwd`, `ls -l ~`
- [x] Ran at least 3 commands of my own
- [ ] Screenshot shared and discussed with the group
- [x] User data script written (3 pages, 1 dynamic)
- [x] Web instance launched; Home, About and Calculator all load
- [x] Calculator tested, including divide-by-zero
- [x] Instances terminated after review
