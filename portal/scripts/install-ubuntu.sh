#!/bin/bash
# OWASP Zombies on Fire - Ubuntu/Debian Installation Script
# This script sets up the Tabletop Exercise Portal on Ubuntu/Debian Linux

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Header
echo -e "${GREEN}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   OWASP Zombies on Fire - Ubuntu/Debian Installation      ║"
echo "║         Tabletop Exercise Portal Setup                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"
print_info "Working directory: $PROJECT_DIR"

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_warning "Running as root. Dependencies will be installed system-wide."
        SUDO=""
    else
        SUDO="sudo"
    fi
}

# Update package list and install system dependencies
install_system_deps() {
    print_info "Updating package list..."
    $SUDO apt-get update

    print_info "Installing system dependencies..."
    $SUDO apt-get install -y \
        python3.11 \
        python3.11-venv \
        python3.11-dev \
        python3-pip \
        build-essential \
        libpq-dev \
        curl \
        git

    print_success "System dependencies installed"
}

# Check if Python 3.11+ is available
check_python() {
    print_info "Checking Python version..."

    # Try python3.11 first, then python3
    if command -v python3.11 &> /dev/null; then
        PYTHON_CMD="python3.11"
    elif command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

        if [[ $PYTHON_MAJOR -lt 3 ]] || [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -lt 11 ]]; then
            print_error "Python 3.11+ is required. Found Python $PYTHON_VERSION"
            print_info "Installing Python 3.11..."

            # Add deadsnakes PPA for newer Python versions
            $SUDO apt-get install -y software-properties-common
            $SUDO add-apt-repository -y ppa:deadsnakes/ppa
            $SUDO apt-get update
            $SUDO apt-get install -y python3.11 python3.11-venv python3.11-dev
            PYTHON_CMD="python3.11"
        else
            PYTHON_CMD="python3"
        fi
    else
        print_error "Python 3 not found. Installing..."
        install_system_deps
        PYTHON_CMD="python3.11"
    fi

    print_success "Using $PYTHON_CMD"
}

# Create virtual environment
create_venv() {
    print_info "Creating virtual environment..."

    if [[ -d "venv" ]]; then
        print_warning "Virtual environment already exists. Skipping creation."
    else
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    fi

    # Activate virtual environment
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Install Python dependencies
install_dependencies() {
    print_info "Upgrading pip..."
    pip install --upgrade pip

    print_info "Installing Python dependencies..."
    pip install -r requirements.txt
    print_success "Dependencies installed"
}

# Setup environment file
setup_env() {
    print_info "Setting up environment configuration..."

    if [[ -f ".env" ]]; then
        print_warning ".env file already exists. Skipping."
    else
        cp .env.example .env

        # Generate a random secret key
        SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

        # Update the secret key in .env
        sed -i "s/your-super-secret-key-change-this-in-production/$SECRET_KEY/" .env

        print_success "Environment file created with generated secret key"
        print_warning "Please edit .env to configure your LLM provider API keys"
    fi
}

# Create required directories
create_directories() {
    print_info "Creating required directories..."
    mkdir -p uploads generated_pdfs
    print_success "Directories created"
}

# Create systemd service (optional)
create_systemd_service() {
    print_info "Do you want to create a systemd service for auto-start? (y/N)"
    read -r response

    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        SERVICE_FILE="/etc/systemd/system/zombies-on-fire.service"

        $SUDO tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=OWASP Zombies on Fire - Tabletop Exercise Portal
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

        $SUDO systemctl daemon-reload
        $SUDO systemctl enable zombies-on-fire

        print_success "Systemd service created and enabled"
        print_info "Start with: sudo systemctl start zombies-on-fire"
        print_info "Check status: sudo systemctl status zombies-on-fire"
    fi
}

# Main installation flow
main() {
    print_info "Starting installation..."
    echo ""

    check_root
    install_system_deps
    check_python
    create_venv
    install_dependencies
    setup_env
    create_directories

    echo ""
    create_systemd_service

    echo ""
    echo -e "${GREEN}"
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║              Installation Complete!                       ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    print_info "To start the application:"
    echo ""
    echo "  1. Activate the virtual environment:"
    echo "     source venv/bin/activate"
    echo ""
    echo "  2. Run the application:"
    echo "     python run.py"
    echo ""
    echo "  3. Open http://localhost:8000 in your browser"
    echo ""
    print_warning "Don't forget to configure your LLM API keys in .env!"
    echo ""
}

# Run main function
main "$@"
