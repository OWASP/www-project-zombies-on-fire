@echo off
REM OWASP Zombies on Fire - Windows Installation Script (Batch)
REM This script sets up the Tabletop Exercise Portal on Windows
REM For best results, use install-windows.ps1 instead

setlocal enabledelayedexpansion

echo.
echo ===============================================================
echo     OWASP Zombies on Fire - Windows Installation Script
echo          Tabletop Exercise Portal Setup
echo ===============================================================
echo.

REM Get script directory and project root
set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%.."
cd /d "%PROJECT_DIR%"
echo [INFO] Working directory: %PROJECT_DIR%

REM Check for Python
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo [INFO] Please install Python 3.11+ from https://www.python.org/downloads/
    echo [INFO] Make sure to check "Add Python to PATH" during installation
    echo.
    echo Opening Python download page...
    start https://www.python.org/downloads/
    echo.
    echo After installing Python, run this script again.
    pause
    exit /b 1
)

REM Display Python version
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [SUCCESS] Found %PYTHON_VERSION%

REM Check Python version (basic check for 3.x)
python -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Python 3.11+ is recommended. You have %PYTHON_VERSION%
    echo [WARNING] Some features may not work correctly.
    echo.
    set /p CONTINUE="Continue anyway? (y/N): "
    if /i not "!CONTINUE!"=="y" (
        echo [INFO] Please upgrade Python and run this script again.
        pause
        exit /b 1
    )
)

REM Create virtual environment
echo.
echo [INFO] Creating virtual environment...
if exist venv (
    echo [WARNING] Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [SUCCESS] Virtual environment activated

REM Upgrade pip
echo.
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo [SUCCESS] pip upgraded

REM Install dependencies
echo [INFO] Installing dependencies (this may take a few minutes)...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [SUCCESS] Dependencies installed

REM Setup environment file
echo.
echo [INFO] Setting up environment configuration...
if exist .env (
    echo [WARNING] .env file already exists. Skipping.
) else (
    if exist .env.example (
        copy .env.example .env >nul
        echo [SUCCESS] Environment file created
        echo [WARNING] Please edit .env to configure your settings and API keys
    ) else (
        echo [ERROR] .env.example not found
    )
)

REM Create required directories
echo.
echo [INFO] Creating required directories...
if not exist uploads mkdir uploads
if not exist generated_pdfs mkdir generated_pdfs
echo [SUCCESS] Directories created

REM Create startup script
echo.
echo [INFO] Creating startup script...
(
echo @echo off
echo echo Starting OWASP Zombies on Fire - Tabletop Exercise Portal...
echo cd /d "%%~dp0"
echo call venv\Scripts\activate.bat
echo python run.py
echo pause
) > start.bat
echo [SUCCESS] Created start.bat

REM Complete
echo.
echo ===============================================================
echo              Installation Complete!
echo ===============================================================
echo.
echo To start the application:
echo.
echo   1. Double-click start.bat
echo.
echo   Or manually:
echo   - Open Command Prompt in this directory
echo   - Run: venv\Scripts\activate.bat
echo   - Run: python run.py
echo.
echo   Then open http://localhost:8000 in your browser
echo.
echo [WARNING] Don't forget to configure your LLM API keys in .env!
echo.

pause
