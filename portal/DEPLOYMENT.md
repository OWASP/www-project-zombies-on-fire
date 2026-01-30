# OWASP Zombies on Fire - Deployment Guide

This guide covers deploying the Tabletop Exercise Portal on various platforms.

## Table of Contents

- [Quick Start](#quick-start)
- [Platform-Specific Installation](#platform-specific-installation)
  - [macOS](#macos)
  - [Ubuntu/Debian Linux](#ubuntudebian-linux)
  - [Windows](#windows)
  - [Docker](#docker)
- [Production Deployment](#production-deployment)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites

| Platform | Requirements |
|----------|-------------|
| macOS | macOS 10.15+, Homebrew (optional) |
| Ubuntu/Debian | Ubuntu 20.04+ or Debian 11+ |
| Windows | Windows 10/11, PowerShell 5.1+ |
| Docker | Docker 20.10+, Docker Compose 2.0+ |

All platforms require:
- Python 3.11 or higher
- 2GB RAM minimum (4GB recommended)
- 1GB disk space

---

## Platform-Specific Installation

### macOS

#### Option 1: Automated Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/OWASP/www-project-zombies-on-fire.git
cd www-project-zombies-on-fire/portal

# Run the installation script
chmod +x scripts/install-mac.sh
./scripts/install-mac.sh
```

The script will:
- Install Homebrew (if not present)
- Install Python 3.11+ (if needed)
- Create a virtual environment
- Install all dependencies
- Generate a secure secret key
- Create required directories

#### Option 2: Manual Installation

```bash
# Install Python via Homebrew
brew install python@3.11

# Clone and setup
git clone https://github.com/OWASP/www-project-zombies-on-fire.git
cd www-project-zombies-on-fire/portal

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run the application
python run.py
```

#### Option 3: Using Makefile

```bash
# Setup and install
make install
make setup-env

# Run
make run          # Production mode
make dev          # Development mode with auto-reload
```

---

### Ubuntu/Debian Linux

#### Option 1: Automated Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/OWASP/www-project-zombies-on-fire.git
cd www-project-zombies-on-fire/portal

# Run the installation script
chmod +x scripts/install-ubuntu.sh
./scripts/install-ubuntu.sh
```

The script will:
- Install system dependencies (Python 3.11, build tools)
- Create a virtual environment
- Install all Python dependencies
- Generate a secure secret key
- Optionally create a systemd service for auto-start

#### Option 2: Manual Installation

```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip build-essential libpq-dev

# Clone and setup
git clone https://github.com/OWASP/www-project-zombies-on-fire.git
cd www-project-zombies-on-fire/portal

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run the application
python run.py
```

#### Running as a Service (systemd)

```bash
# Create service file
sudo nano /etc/systemd/system/zombies-on-fire.service
```

Add the following content:

```ini
[Unit]
Description=OWASP Zombies on Fire - Tabletop Exercise Portal
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/portal
Environment="PATH=/path/to/portal/venv/bin"
ExecStart=/path/to/portal/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable zombies-on-fire
sudo systemctl start zombies-on-fire
sudo systemctl status zombies-on-fire
```

---

### Windows

#### Option 1: PowerShell Installation (Recommended)

```powershell
# Clone the repository
git clone https://github.com/OWASP/www-project-zombies-on-fire.git
cd www-project-zombies-on-fire\portal

# Run installation script (may need to adjust execution policy)
powershell -ExecutionPolicy Bypass -File scripts\install-windows.ps1
```

#### Option 2: Batch File Installation

```cmd
# Clone the repository
git clone https://github.com/OWASP/www-project-zombies-on-fire.git
cd www-project-zombies-on-fire\portal

# Run installation script
scripts\install-windows.bat
```

#### Option 3: Manual Installation

1. **Install Python 3.11+** from https://www.python.org/downloads/
   - Check "Add Python to PATH" during installation

2. **Clone and setup:**

```cmd
git clone https://github.com/OWASP/www-project-zombies-on-fire.git
cd www-project-zombies-on-fire\portal

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your settings

# Run the application
python run.py
```

#### Starting the Application

After installation, use one of these methods:

- Double-click `start.bat`
- Run `.\start.ps1` in PowerShell
- Manual: `venv\Scripts\activate` then `python run.py`

---

### Docker

#### Quick Start with Docker Compose

```bash
# Clone the repository
git clone https://github.com/OWASP/www-project-zombies-on-fire.git
cd www-project-zombies-on-fire/portal

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

#### Building the Docker Image Manually

```bash
# Build image
docker build -t zombies-on-fire:latest .

# Run container
docker run -d \
  --name zombies-on-fire \
  -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -e LLM_PROVIDER=mock \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/generated_pdfs:/app/generated_pdfs \
  zombies-on-fire:latest
```

#### Using Makefile (macOS/Linux)

```bash
make docker-build    # Build image
make docker-run      # Start containers
make docker-logs     # View logs
make docker-stop     # Stop containers
```

---

## Production Deployment

For production environments, use the production Docker Compose configuration with PostgreSQL and optional Nginx reverse proxy.

### Production Setup

1. **Create production environment file:**

```bash
# Create .env.prod with production values
cat > .env.prod << EOF
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(64))")
POSTGRES_PASSWORD=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
LLM_PROVIDER=openai
OPENAI_API_KEY=your-production-api-key
LLM_MODEL=gpt-4
EOF
```

2. **Start production stack:**

```bash
# Load environment and start
export $(cat .env.prod | xargs)
docker-compose -f docker-compose.prod.yml up -d
```

### Production with Nginx (HTTPS)

1. **Obtain SSL certificates** (using Let's Encrypt):

```bash
# Install certbot
sudo apt install certbot

# Get certificates
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates
mkdir -p certs
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem certs/
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem certs/
```

2. **Configure nginx.conf** for HTTPS (uncomment SSL section)

3. **Start with Nginx:**

```bash
docker-compose -f docker-compose.prod.yml --profile with-nginx up -d
```

### Production Checklist

- [ ] Generate strong SECRET_KEY (min 64 characters)
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure proper database backups
- [ ] Set DEBUG=False
- [ ] Use HTTPS with valid SSL certificates
- [ ] Configure firewall rules
- [ ] Set up monitoring and logging
- [ ] Configure rate limiting
- [ ] Review CORS settings for production domain

---

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | JWT signing key | - | Yes |
| `DEBUG` | Enable debug mode | `False` | No |
| `DATABASE_URL` | Database connection URL | `sqlite:///./tabletop.db` | No |
| `LLM_PROVIDER` | AI provider (openai, anthropic, mock) | `mock` | No |
| `OPENAI_API_KEY` | OpenAI API key | - | If using OpenAI |
| `ANTHROPIC_API_KEY` | Anthropic API key | - | If using Anthropic |
| `LLM_MODEL` | Model to use | `gpt-4` | No |
| `UPLOAD_DIR` | File upload directory | `./uploads` | No |
| `PDF_OUTPUT_DIR` | PDF output directory | `./generated_pdfs` | No |

### Database Options

**SQLite (Development):**
```
DATABASE_URL=sqlite:///./tabletop.db
```

**PostgreSQL (Production):**
```
DATABASE_URL=postgresql://user:password@localhost:5432/zombies_on_fire
```

### LLM Provider Configuration

**OpenAI:**
```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4
```

**Anthropic:**
```
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
LLM_MODEL=claude-3-sonnet-20240229
```

**Mock (Testing):**
```
LLM_PROVIDER=mock
```

---

## Troubleshooting

### Common Issues

#### Python Version Error

**Problem:** `Python 3.11+ is required`

**Solution:**
- macOS: `brew install python@3.11`
- Ubuntu: Use deadsnakes PPA:
  ```bash
  sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt update
  sudo apt install python3.11
  ```
- Windows: Download from python.org

#### Port Already in Use

**Problem:** `Address already in use` error on port 8000

**Solution:**
```bash
# Find process using port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or use different port
python -m uvicorn app.main:app --port 8001
```

#### Virtual Environment Activation

**Problem:** Virtual environment won't activate

**Solution:**
- macOS/Linux: `source venv/bin/activate`
- Windows CMD: `venv\Scripts\activate.bat`
- Windows PowerShell: `.\venv\Scripts\Activate.ps1`
  - If blocked: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

#### Docker Permission Denied

**Problem:** Permission denied when running Docker commands

**Solution:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and log back in

# Or run with sudo
sudo docker-compose up -d
```

#### Database Migration Issues

**Problem:** Database schema out of sync

**Solution:**
```bash
# Delete SQLite database and restart
rm tabletop.db
python run.py  # Will recreate tables
```

#### LLM API Errors

**Problem:** API calls failing

**Solution:**
1. Verify API key is correct in `.env`
2. Check API key has sufficient credits
3. Verify internet connectivity
4. Use `mock` provider for testing without API

### Getting Help

- GitHub Issues: https://github.com/OWASP/www-project-zombies-on-fire/issues
- OWASP Slack: #project-zombies-on-fire

---

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [OWASP Project Page](https://owasp.org/www-project-zombies-on-fire/)
