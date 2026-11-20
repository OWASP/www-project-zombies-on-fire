@echo off
rem Start Zombies on Fire: finds a free port, opens your browser, and handles AI calls (no CORS setup).
rem Usage: start.bat [--port 9000] [--no-open]
setlocal
cd /d "%~dp0"
set NODEMAJOR=0
where node >nul 2>nul
if %errorlevel%==0 (
  for /f %%v in ('node -p "parseInt(process.versions.node)"') do set NODEMAJOR=%%v
)
if %NODEMAJOR% GEQ 18 (
  node server.js %*
  if errorlevel 1 pause
  exit /b
)
echo Node.js 18 or newer gives the best experience (AI calls without CORS setup): https://nodejs.org
where py >nul 2>nul && (echo Starting the basic Python server instead. & py serve.py & exit /b)
where python >nul 2>nul && (echo Starting the basic Python server instead. & python serve.py & exit /b)
echo Please install Node.js 18+ from https://nodejs.org and run this again.
pause
exit /b 1
