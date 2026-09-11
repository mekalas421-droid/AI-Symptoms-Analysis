#!/bin/bash
# =====================================================================
# MedAssist AI — AWS EC2 Deployment Setup Script (Ubuntu)
# Wires Nginx reverse proxy, MySQL database, and Backend/Frontend services
# =====================================================================

set -e

echo "=== 1. System Updates & Prerequisites ==="
sudo apt-get update -y
sudo apt-get install -y curl gnupg nginx git mysql-server python3-pip python3-venv

# Ensure Node.js 20.x LTS is installed for Next.js 14
if ! command -v node >/dev/null 2>&1 || [ "$(node -v | cut -d'.' -f1 | tr -d 'v')" -lt 18 ]; then
    echo "Installing Node.js 20.x LTS..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

echo "Node version: $(node -v)"
echo "NPM version: $(npm -v)"

echo "=== 2. Setup MySQL database ==="
sudo systemctl start mysql
sudo mysql -e "CREATE DATABASE IF NOT EXISTS medassist_db;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'medassist_user'@'localhost' IDENTIFIED BY 'secure_password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON medassist_db.* TO 'medassist_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

echo "=== 3. Setup Python Backend Environment ==="
cd /home/ubuntu/medassist-ai/backend
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# Run migrations and seed database
export MYSQL_USER=medassist_user
export MYSQL_PASSWORD=secure_password
export MYSQL_DB=medassist_db
export MYSQL_HOST=localhost
export MYSQL_PORT=3306
./venv/bin/python -m app.db.seed || echo "DB seed step finished"

echo "=== 4. Setup Next.js Frontend ==="
cd /home/ubuntu/medassist-ai/frontend
npm install
npm run build

echo "=== 5. Configure Nginx Proxy ==="
sudo cp /home/ubuntu/medassist-ai/deploy/nginx.conf /etc/nginx/sites-available/medassist
sudo ln -sf /etc/nginx/sites-available/medassist /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

echo "=== 6. Configure & Start Systemd Services ==="
# Ensure correct ownership
sudo chown -R ubuntu:ubuntu /home/ubuntu/medassist-ai

sudo cp /home/ubuntu/medassist-ai/deploy/medassist-backend.service /etc/systemd/system/
sudo cp /home/ubuntu/medassist-ai/deploy/medassist-frontend.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable medassist-backend.service
sudo systemctl restart medassist-backend.service

sudo systemctl enable medassist-frontend.service
sudo systemctl restart medassist-frontend.service

echo "=== MedAssist AI Deployment Complete! ==="
echo "Access the platform on HTTP port 80 of your EC2 Public IP."
