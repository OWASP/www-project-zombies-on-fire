# OWASP Zombies on Fire - Windows Installation Script (PowerShell)
# This script sets up the Tabletop Exercise Portal on Windows
# Run with: powershell -ExecutionPolicy Bypass -File install-windows.ps1

#Requires -Version 5.1

param(
    [switch]$SkipPythonInstall,
    [switch]$Force
)

# Colors and formatting
$Host.UI.RawUI.ForegroundColor = "White"

function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Info($message) {
    Write-Host "[INFO] " -ForegroundColor Blue -NoNewline
    Write-Host $message
}

function Write-Success($message) {
    Write-Host "[SUCCESS] " -ForegroundColor Green -NoNewline
    Write-Host $message
}

function Write-Warning($message) {
    Write-Host "[WARNING] " -ForegroundColor Yellow -NoNewline
    Write-Host $message
}

function Write-Error($message) {
    Write-Host "[ERROR] " -ForegroundColor Red -NoNewline
    Write-Host $message
}

# Header
Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║    OWASP Zombies on Fire - Windows Installation Script    ║" -ForegroundColor Green
Write-Host "║         Tabletop Exercise Portal Setup                    ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Get script directory and project root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Split-Path -Parent $ScriptDir

Set-Location $ProjectDir
Write-Info "Working directory: $ProjectDir"

# Check for winget (Windows Package Manager)
function Test-Winget {
    try {
        $null = Get-Command winget -ErrorAction Stop
        return $true
    }
    catch {
        return $false
    }
}

# Check for Python
function Test-Python {
    try {
        $pythonVersion = & python --version 2>&1
        if ($pythonVersion -match "Python (\d+)\.(\d+)") {
            $major = [int]$Matches[1]
            $minor = [int]$Matches[2]
            if ($major -ge 3 -and $minor -ge 11) {
                return $true
            }
        }
        return $false
    }
    catch {
        return $false
    }
}

# Install Python using winget
function Install-Python {
    Write-Info "Installing Python 3.11..."

    if (Test-Winget) {
        Write-Info "Using winget to install Python..."
        winget install Python.Python.3.11 --accept-source-agreements --accept-package-agreements

        # Refresh PATH
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    }
    else {
        Write-Warning "winget not found. Please install Python 3.11+ manually from https://www.python.org/downloads/"
        Write-Warning "Make sure to check 'Add Python to PATH' during installation."

        # Open Python download page
        Start-Process "https://www.python.org/downloads/"

        Write-Host ""
        Write-Host "Press any key after installing Python to continue..." -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

        # Refresh PATH
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    }
}

# Check Python installation
function Confirm-Python {
    Write-Info "Checking Python version..."

    if (-not (Test-Python)) {
        if (-not $SkipPythonInstall) {
            Install-Python

            # Verify installation
            if (-not (Test-Python)) {
                Write-Error "Python 3.11+ installation failed or not found in PATH"
                Write-Info "Please install Python 3.11+ manually and run this script again"
                exit 1
            }
        }
        else {
            Write-Error "Python 3.11+ is required but not found"
            exit 1
        }
    }

    $pythonVersion = & python --version 2>&1
    Write-Success "Python installed: $pythonVersion"
}

# Create virtual environment
function New-VirtualEnvironment {
    Write-Info "Creating virtual environment..."

    if (Test-Path "venv") {
        if ($Force) {
            Write-Warning "Removing existing virtual environment..."
            Remove-Item -Recurse -Force "venv"
        }
        else {
            Write-Warning "Virtual environment already exists. Use -Force to recreate."
            return
        }
    }

    & python -m venv venv

    if (-not (Test-Path "venv")) {
        Write-Error "Failed to create virtual environment"
        exit 1
    }

    Write-Success "Virtual environment created"
}

# Activate virtual environment and install dependencies
function Install-Dependencies {
    Write-Info "Activating virtual environment..."

    # Activate virtual environment
    $activateScript = Join-Path $ProjectDir "venv\Scripts\Activate.ps1"

    if (-not (Test-Path $activateScript)) {
        Write-Error "Virtual environment activation script not found"
        exit 1
    }

    & $activateScript

    Write-Info "Upgrading pip..."
    & python -m pip install --upgrade pip

    Write-Info "Installing dependencies..."
    & pip install -r requirements.txt

    Write-Success "Dependencies installed"
}

# Setup environment file
function Initialize-Environment {
    Write-Info "Setting up environment configuration..."

    $envFile = Join-Path $ProjectDir ".env"
    $envExample = Join-Path $ProjectDir ".env.example"

    if (Test-Path $envFile) {
        Write-Warning ".env file already exists. Skipping."
        return
    }

    if (-not (Test-Path $envExample)) {
        Write-Error ".env.example not found"
        exit 1
    }

    Copy-Item $envExample $envFile

    # Generate a random secret key
    $secretKey = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | ForEach-Object {[char]$_})

    # Update secret key in .env
    $content = Get-Content $envFile -Raw
    $content = $content -replace "your-super-secret-key-change-this-in-production", $secretKey
    Set-Content $envFile $content

    Write-Success "Environment file created with generated secret key"
    Write-Warning "Please edit .env to configure your LLM provider API keys"
}

# Create required directories
function New-RequiredDirectories {
    Write-Info "Creating required directories..."

    $dirs = @("uploads", "generated_pdfs")

    foreach ($dir in $dirs) {
        $path = Join-Path $ProjectDir $dir
        if (-not (Test-Path $path)) {
            New-Item -ItemType Directory -Path $path | Out-Null
        }
    }

    Write-Success "Directories created"
}

# Create Windows startup script
function New-StartupScript {
    Write-Info "Creating startup scripts..."

    $startScript = Join-Path $ProjectDir "start.bat"
    $startContent = @"
@echo off
echo Starting OWASP Zombies on Fire - Tabletop Exercise Portal...
cd /d "%~dp0"
call venv\Scripts\activate.bat
python run.py
pause
"@

    Set-Content $startScript $startContent
    Write-Success "Created start.bat"

    $startPsScript = Join-Path $ProjectDir "start.ps1"
    $startPsContent = @"
# OWASP Zombies on Fire - Start Script
Write-Host "Starting OWASP Zombies on Fire - Tabletop Exercise Portal..." -ForegroundColor Green
Set-Location `$PSScriptRoot
& .\venv\Scripts\Activate.ps1
python run.py
"@

    Set-Content $startPsScript $startPsContent
    Write-Success "Created start.ps1"
}

# Main installation flow
function Main {
    Write-Info "Starting installation..."
    Write-Host ""

    Confirm-Python
    New-VirtualEnvironment
    Install-Dependencies
    Initialize-Environment
    New-RequiredDirectories
    New-StartupScript

    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║              Installation Complete!                       ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Info "To start the application:"
    Write-Host ""
    Write-Host "  Option 1: Double-click start.bat"
    Write-Host ""
    Write-Host "  Option 2: Run in PowerShell:"
    Write-Host "     .\venv\Scripts\Activate.ps1"
    Write-Host "     python run.py"
    Write-Host ""
    Write-Host "  Then open http://localhost:8000 in your browser"
    Write-Host ""
    Write-Warning "Don't forget to configure your LLM API keys in .env!"
    Write-Host ""
}

# Run main function
Main
