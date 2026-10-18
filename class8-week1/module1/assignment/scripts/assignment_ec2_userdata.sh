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
