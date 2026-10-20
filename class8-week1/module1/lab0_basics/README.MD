## SEIR Foundations — Module 1, Lab 0

## EC2 Deployment: Launch, Connect, Observe, Repeat

This lab uses the **AWS Management Console** to:

1. Create an EC2 **launch template** with a custom key pair and a custom security group (SSH + HTTP only).
2. Launch **3 EC2 instances** from that template.
3. Connect to **2 instances with EC2 Instance Connect** and **1 instance with SSH**.
4. Show the **SEIR dashboard** (run `seir-dashboard`).
5. Capture **screenshots** as evidence.
6. **Terminate** the instances.

---

## Naming Conventions

| Resource           | Name                  |
|--------------------|-----------------------|
| Key pair           | `lab0-key`            |
| Security group     | `lab0-sg`             |
| Launch template    | `lab0-template`       |
| Instances          | `lab0-ec2-1`, `lab0-ec2-2`, `lab0-ec2-3` |
| Screenshots folder | `lab0-evidence/`      |

## Prerequisites

- An AWS account with permissions for EC2 (launch templates, instances, key pairs, security groups).
- A local terminal with an SSH client (macOS/Linux Terminal, or Windows PowerShell / Windows Terminal).
- Pick one AWS Region (e.g. **us-east-1**) and use it for every step. Check the Region selector at the top-right of the console.
- The default VPC exists in that Region (it does unless it was deleted).

---

## Task 1 – Create the EC2 Launch Template

### 1.1 Open the launch template wizard

1. Sign in to the AWS Console and search for **EC2** in the top search bar. Open **EC2**.
2. In the left navigation pane, under **Instances**, choose **Launch Templates**.
3. Choose **Create launch template**.

### 1.2 Template name and description

1. **Launch template name:** `lab0-template`
2. **Template version description:** `lab0 - SSH and HTTP web server template`


### 1.3 Application and OS Images (AMI)

1. Choose **Quick Start** → **Amazon Linux**.
2. Select **Amazon Linux 2023 AMI** (Free tier eligible).

### 1.4 Instance type

1. Choose **t2.micro** or **t3.micro** (whichever is marked *Free tier eligible* in your Region).

### 1.5 Key pair (custom)

1. Under **Key pair (login)**, choose **Create new key pair**.
2. **Key pair name:** `lab0-key`
3. **Key pair type:** `RSA`
4. **Private key file format:**
   - `.pem` → for OpenSSH (macOS, Linux, Windows PowerShell)
   - `.ppk` → only if you will use PuTTY
5. Choose **Create key pair**. The file `lab0-key.pem` downloads automatically.
   > ⚠️ This is the **only** time you can download the private key. Store it somewhere safe (e.g. `~/.ssh/lab0-key.pem`).
6. Confirm `lab0-key` is now selected in the **Key pair name** dropdown.

### 1.6 Network settings – custom security group

1. **Subnet:** leave as **Don't include in launch template** (the default VPC's subnets auto-assign public IPs).
2. **Firewall (security groups):** choose **Create security group**.
3. **Security group name:** `lab0-sg`
4. **Description:** `lab0 - allow SSH and HTTP inbound`
5. **VPC:** select the **default VPC**.
6. **Inbound security group rules** – make sure there are **exactly two** rules (choose **Add security group rule** for the second one, and remove any extras):

   | # | Type | Protocol | Port range | Source type | Source      | Description  |
   |---|------|----------|-----------|-------------|-------------|--------------|
   | 1 | SSH  | TCP      | 22        | Custom      | `0.0.0.0/0` | lab0 SSH     |
   | 2 | HTTP | TCP      | 80        | Custom      | `0.0.0.0/0` | lab0 HTTP    |

7. **Outbound rules:** do not change anything. The default rule (All traffic → `0.0.0.0/0`) is created automatically.

> 💡 If you'd rather build the security group first: go to **EC2 → Network & Security → Security Groups → Create security group**, apply the same settings above, then in the template choose **Select existing security group** → `lab0-sg`.

### 1.7 Storage

1. Leave the default (8 GiB gp3 root volume).

### 1.8 Resource tags (optional but recommended)

1. Expand **Resource tags** → **Add new tag**.
2. **Key:** `Project` **Value:** `lab0` **Resource types:** Instances, Volumes.

### 1.9 Advanced details
- Course provides a **User data** script that installs the SEIR dashboard, paste it into **Advanced details → User data** now so every instance has it at boot.

1. Scroll all the way to the bottom and add the contents contained in the file below. Starting with `#!/bin/bash` and ending with `echo 'SEIR dashboard installed.'`

lab0_basics/scripts/seir_ec2_userdata.sh

### 1.10 Create

1. Review the **Summary** panel on the right.
2. Choose **Create launch template**.
3. Choose **View launch templates** and confirm `lab0-template` appears.

📸 **Screenshot [`lab0-01-template`](screenshots/lab0-evidence/lab0-01-template.png):** the launch template details page showing the key pair `lab0-key` and security group ID beginning with `sg-`.

📸 **Screenshot [`lab0-02-sg-inbound`](screenshots/lab0-evidence/lab0-02-sg-inbound.png):** **EC2 → Security Groups → `lab0-sg` → Inbound rules** tab showing only the SSH (22) and HTTP (80) rules from `0.0.0.0/0`.

📸 **Screenshot [`lab0-03-sg-outbound`](screenshots/lab0-evidence/lab0-03-sg-outbound.png):** **EC2 → Security Groups → `lab0-sg` → Outbound rules** tab showing only the All Traffic, Protocol (All), and Port Range (All) rules from `0.0.0.0/0`.


---

## Task 2 – Launch EC2 Instances from the Template three times

1. Go to **EC2 → Instances → Launch Templates**.
2. Select **`lab0-template`**.
3. Choose **Actions → Launch instance from template**.
4. **Source template version:** `1 (Default)`.
5. In the **Summary** panel, set **Number of instances** to **`3`** or `1` then launch 2 more times
6. Review the settings – they are inherited from the template (AMI, instance type, `lab0-key`, `lab0-sg`). Do **not** change them.
7. Choose **Launch instance**.
8. Choose **View instance or instances**.

### 2.1 Name the instances

1. In **EC2 → Instances**, find the new instances (Name column is blank).
2. Hover over each **Name** cell, click the ✏️ pencil icon, and enter:
   - `lab0-ec2-1`
   - `lab0-ec2-2`
   - `lab0-ec2-3`
3. Wait until each instance shows **Instance state: Running** and **Status check: 3/3 checks passed** (refresh with the 🔄 button).
4. Note the **Public IPv4 address** of each instance.

📸 **Screenshot [`lab0-04-instances-running`](screenshots/lab0-evidence/lab0-04-instances-running.png):** the Instances list showing all three `lab0-ec2-*` instances **Running** with public IPs.

---

## Task 3 – Connect to the Instances

### 3.1 EC2 Instance Connect – `lab0-ec2-1`

1. In **EC2 → Instances**, select **`lab0-ec2-1`**.
2. Choose **Connect** (top of the page).
3. Select the **EC2 Instance Connect** tab.
4. **Connection type:** `Connect using EC2 Instance Connect` (public IPv4).
5. **Username:** `ec2-user` (default for Amazon Linux).
6. Choose **Connect**. A browser terminal opens in a new tab.
7. Verify you are connected:
   ```bash
   whoami
   hostname
   curl -s http://169.254.169.254/latest/meta-data/instance-id 2>/dev/null || ec2-metadata -i
   ```
   📸 **Screenshot `lab0-ec2-1.png`:** the Instances showing the SEIR Foundations - Amazon Linux 2023 EC2 User Data

### 3.2 EC2 Instance Connect – `lab0-ec2-2`

Repeat the steps in **3.1** for **`lab0-ec2-2`**.

 📸 **Screenshot `lab0-ec2-2.png`:** the Instances showing the SEIR Foundations - Amazon Linux 2023 EC2 User Data

### 3.3 SSH – `lab0-ec2-3`

1. In **EC2 → Instances**, select **`lab0-ec2-3`** and copy its **Public IPv4 address** (or choose **Connect → SSH client** tab, which shows the exact command).
2. Open a terminal on your computer and go to the folder containing `lab0-key.pem`.
3. Restrict the key's permissions (SSH refuses keys that are too open):

   **macOS / Linux**
   ```bash
   chmod 400 lab0-key.pem
   ```

   **Windows PowerShell**
   ```powershell
   icacls .\lab0-key.pem /inheritance:r
   icacls .\lab0-key.pem /grant:r "$($env:USERNAME):(R)"
   ```

4. Connect (replace `<PUBLIC_IP>`):
   ```bash
   ssh -i lab0-key.pem ec2-user@54.83.149.249
   ```
5. Type `yes` when prompted to trust the host fingerprint.
6. Verify:
   ```bash
   whoami
   hostname
   ```
 📸 **Screenshot `lab0-ec2-3.png`:** the Instances showing the SEIR Foundations - Amazon Linux 2023 EC2 User Data

### Troubleshooting connections

| Symptom | Fix |
|---|---|
| `Connection timed out` | Confirm `lab0-sg` has SSH (22) from `0.0.0.0/0` and the instance has a public IPv4 address. |
| `Permission denied (publickey)` | Wrong username (use `ec2-user`), wrong key, or key permissions too open (redo the `chmod`/`icacls` step). |
| EC2 Instance Connect fails | Instance must be **Running** with 3/3 checks passed, have a public IP, and port 22 open. Wait 1–2 minutes after launch and retry. |
| No public IP | The subnet does not auto-assign public IPs. Re-launch with **Network settings → Advanced network configuration → Auto-assign public IP: Enable**. |

---

## Task 4 – Show the SEIR Dashboard

On **each** connected instance (both Instance Connect browser sessions and the SSH session), run:

```bash
seir-dashboard
```

- Leave the dashboard output visible on screen for the screenshots in Task 5.
- If you get `command not found`, the dashboard isn't installed on the AMI. Install it using the script/instructions provided with your course materials (or add that script to the template's **User data** in step 1.9 and relaunch), then run `seir-dashboard` again.

---

## Task 5 – Capture Evidence Screenshots

| Instance       | Private IPv4 address  |Connection method |Screenshot |Instance Terminated|
|----------------|-----------------------|--------------|-----------|----------------|
| `lab0-ec2-1`   | 172.31.46.71  |EC2 Instance Connect  |screenshots/lab0-evidence/lab0-ec2-1|Yes
| `lab0-ec2-2`   | 172.31.47.75  |EC2 Instance Connect  |screenshots/lab0-evidence/lab0-ec2-2|Yes
| `lab0-ec2-3`   | 172.31.37.127 |SSH from local terminal (`lab0-key.pem`) |screenshots/lab0-evidence/lab0-ec2-3|Yes


## Task 6 – Terminate the Instances

1. Exit the sessions:
   - Instance Connect: close the browser tabs (or type `exit`).
   - SSH: type `exit`.
2. Go to **EC2 → Instances**.
3. Select the checkboxes for **`lab0-ec2-1`**, **`lab0-ec2-2`**, and **`lab0-ec2-3`**.
4. Choose **Instance state → Terminate (delete) instance**.
5. In the confirmation dialog, choose **Terminate (delete)**.
6. Refresh until all three show **Instance state: Terminated** (they disappear from the list after about an hour).

📸 **Screenshot [`lab0-05-terminated`](screenshots/lab0-evidence/lab0-05-terminated.png):** the Instances list showing all three `lab0-ec2-*` instances **Terminated**.

### 6.1 Optional full cleanup

Do this only if the lab doesn't require you to keep these resources:

1. **Launch template:** EC2 → Launch Templates → select `lab0-template` → **Actions → Delete template**.
2. **Security group:** EC2 → Security Groups → select `lab0-sg` → **Actions → Delete security groups** (works only after the instances are fully terminated).
3. **Key pair:** EC2 → Key Pairs → select `lab0-key` → **Actions → Delete**, then delete `lab0-key.pem` from your computer.

---

## Lab0 Completion Checklist

- [x] `lab0-template` created with custom key pair `lab0-key`
- [x] `lab0-sg` has exactly two inbound rules (SSH 22, HTTP 80 from `0.0.0.0/0`) and the default outbound rule
- [x] 3 instances launched from `lab0-template`
- [x] `lab0-ec2-1` and `lab0-ec2-2` connected via EC2 Instance Connect
- [x] `lab0-ec2-3` connected via SSH with `lab0-key.pem`
- [x] `seir-dashboard` shown on each instance
- [x] Screenshots `lab0-01` through `lab0-07` saved in `screenshots/lab0-evidence/`
- [x] All 3 instances terminated

> ⚠️ **Security note:** `0.0.0.0/0` on port 22 exposes SSH to the entire internet. It's acceptable for this short-lived lab, but in real environments restrict SSH to your own IP (`My IP`) or use Session Manager.