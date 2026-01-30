#!/bin/bash
# OWASP Zombies on Fire - macOS Installation Script
# This script sets up the Tabletop Exercise Portal on macOS

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
echo "║     OWASP Zombies on Fire - macOS Installation Script     ║"
echo "║         Tabletop Exercise Portal Setup                    ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"
print_info "Working directory: $PROJECT_DIR"

# Check for Homebrew
check_homebrew() {
    if ! command -v brew &> /dev/null; then
        print_warning "Homebrew not found. Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

        # Add Homebrew to PATH for Apple Silicon Macs
        if [[ $(uname -m) == "arm64" ]]; then
            eval "$(/opt/homebrew/bin/brew shellenv)"
        fi
    else
        print_success "Homebrew is installed"
    fi
}

# Check for Python 3.11+
check_python() {
    print_info "Checking Python version..."

    # Check if python3 exists
    if ! command -v python3 &> /dev/null; then
        print_warning "Python 3 not found. Installing Python 3.11..."
        brew install python@3.11
    fi

    # Get Python version
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

    if [[ $PYTHON_MAJOR -lt 3 ]] || [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -lt 11 ]]; then
        print_warning "Python $PYTHON_VERSION found. Installing Python 3.11..."
        brew install python@3.11
        # Use the newly installed Python
        PYTHON_CMD="python3.11"
    else
        PYTHON_CMD="python3"
        print_success "Python $PYTHON_VERSION is installed"
    fi
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

# Install dependencies
install_dependencies() {
    print_info "Upgrading pip..."
    pip install --upgrade pip

    print_info "Installing dependencies..."
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

        # Update the secret key in .env (macOS sed syntax)
        sed -i '' "s/your-super-secret-key-change-this-in-production/$SECRET_KEY/" .env

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

# Main installation flow
main() {
    print_info "Starting installation..."
    echo ""

    check_homebrew
    check_python
    create_venv
    install_dependencies
    setup_env
    create_directories

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
