# Production Deployment & Host Isolation Guide: BARINCAIRO.COM

> **Target**: Secure deployment on Ubuntu host server co-located with active WordPress and Symfony applications, using containerized Docker isolation and zero-exposure GitHub Actions SSH CD.

---

## 🔒 Security Principles

1. **No Credentials in Source Control**: Database passwords, secrets, and private SSH keys are stored strictly in local `.env` files or GitHub Encrypted Secrets.
2. **Host Co-location Safety**: Docker containers bind ports internally (`127.0.0.1:3000` and `127.0.0.1:8000`). PostGIS is NOT exposed publicly. Host Nginx acts as the single reverse-proxy entry point.
3. **Isolated SSH Permissions**: GitHub Actions authenticates via a dedicated ed25519 SSH key pair restricted to repository deployment.

---

## 🛠️ Step-by-Step Server Setup Guide

### Step 1: Generate a Dedicated SSH Key Pair on Server
Log into your Ubuntu server via SSH:

```bash
# Generate key pair for GitHub Actions deployment
ssh-keygen -t ed25519 -C "github-actions-barincairo" -f ~/.ssh/barincairo_deploy_key -N ""

# Authorize the public key on your server
cat ~/.ssh/barincairo_deploy_key.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Display the private key (you will copy this into GitHub Secrets):

```bash
cat ~/.ssh/barincairo_deploy_key
```

---

### Step 2: Configure GitHub Repository Secrets
Go to your GitHub repository: **https://github.com/alexseif/barincairo**  
Navigate to **Settings** $\rightarrow$ **Secrets and variables** $\rightarrow$ **Actions** $\rightarrow$ **New repository secret**:



---

### Step 3: Clone Repository & Setup Environment on Server

Log into your server and prepare the directory:

```bash
# Ensure directory exists and permissions are set
sudo mkdir -p /var/www/barincairo.com
sudo chown -R $USER:$USER /var/www/barincairo.com

# Clone the repository
git clone git@github.com:alexseif/barincairo.git /var/www/barincairo.com
cd /var/www/barincairo.com

# Create the secret environment file
cp .env.example .env
```

Edit `.env` using `nano .env` and set strong generated secrets:

```env
POSTGRES_DB=barincairo_db
POSTGRES_USER=barincairo_user
POSTGRES_PASSWORD=YOUR_STRONG_GENERATED_PASSWORD_HERE
SECRET_KEY=YOUR_STRONG_GENERATED_JWT_SECRET_HERE
NEXT_PUBLIC_API_URL=https://api.barincairo.com
```

---

### Step 4: Configure Host Nginx & Certbot SSL

Copy the provided Nginx configuration template:

```bash
# Create Nginx site configuration
sudo cp /var/www/barincairo.com/nginx.conf.example /etc/nginx/sites-available/barincairo.conf

# Enable the site via symlink
sudo ln -s /etc/nginx/sites-available/barincairo.conf /etc/nginx/sites-enabled/

# Test Nginx syntax safety (ensures WordPress/Symfony sites are NOT broken)
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

Obtain free SSL certificates via Certbot:

```bash
sudo certbot --nginx -d barincairo.com -d www.barincairo.com -d api.barincairo.com
```

---

### Step 5: Test Container Spin-up & CI/CD Pipeline

Build and launch containers locally on the server for the first time:

```bash
cd /var/www/barincairo.com
docker compose up -d --build
```

Verify containers are running cleanly:

```bash
docker compose ps
```

Now, any future `git push` to `main` will trigger `.github/workflows/deploy.yml`, which will:
1. Run linting and build checks inside GitHub Actions runners.
2. Authenticate securely via SSH into your server using `SSH_PRIVATE_KEY`.
3. Pull updates and execute `docker compose up -d --build` automatically with zero downtime.
