@echo off
REM VoxaLab AI - Quick Start Setup Script for Windows
REM Sets up VoxaLab AI for local development

echo.
echo VoxaLab AI - Setup
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.10 or later from https://python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo OK - Python %PYTHON_VERSION% installed

REM Check Node.js installation
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Please install Node.js 16 or later from https://nodejs.org
    pause
    exit /b 1
)

for /f %%i in ('node --version') do set NODE_VERSION=%%i
echo OK - Node.js %NODE_VERSION% installed

REM Check Git installation
git --version >nul 2>&1
if errorlevel 1 (
    echo NOTE: Git not found (optional). Some features may not work without Git.
) else (
    echo OK - Git is installed
)

echo.
echo Setting up Backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -q -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env configuration file...
    if exist ".env.example" (
        copy .env.example .env >nul
    ) else (
        echo MISTRAL_API_KEY=your-api-key-here > .env
    )
    echo NOTE: Please edit backend\.env and add your Mistral API key
)

echo OK - Backend setup complete
cd ..

REM Setup Frontend
echo.
echo Setting up Frontend...
cd frontend

REM Install dependencies
echo Installing npm dependencies...
npm install -q --legacy-peer-deps >nul 2>&1
if errorlevel 1 (
    npm install -q
)

echo OK - Frontend setup complete
cd ..

echo.
echo Setup Complete
echo.
echo Next Steps:
echo.
echo 1. Edit backend\.env with your Mistral API key:
echo    MISTRAL_API_KEY=sk-your-key-here
echo.
echo 2. Start the backend in Terminal 1:
echo    cd backend
echo    venv\Scripts\activate.bat
echo    python main.py
echo.
echo 3. Start the frontend in Terminal 2:
echo    cd frontend
echo    npm start
echo.
echo 4. Open http://localhost:3000 in your browser
echo.
echo Documentation:
echo    README.md - Project overview
echo    DEPLOY.md - Deployment guide
echo.
echo Get your Mistral API key from:
echo    https://console.mistral.ai
echo.
pause
