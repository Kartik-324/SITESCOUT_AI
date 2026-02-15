@echo off
REM AI Lead Generation System - Windows Setup Script

echo ============================================================
echo   AI Lead Generation System - Setup Script (Windows)
echo ============================================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9 or higher from python.org
    pause
    exit /b 1
)
echo Python found!
echo.

REM Navigate to backend
cd backend
if %errorlevel% neq 0 (
    echo ERROR: Could not find backend directory
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created!
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo Dependencies installed!
echo.

REM Create .env file
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo .env file created!
    echo.
    echo IMPORTANT: Please edit .env file with your API keys!
) else (
    echo .env file already exists
)
echo.

REM Check for credentials
if not exist "credentials.json" (
    echo WARNING: credentials.json not found
    echo Please download your Google service account JSON
    echo and rename it to credentials.json
) else (
    echo credentials.json found!
)
echo.

echo ============================================================
echo   Setup Complete!
echo ============================================================
echo.
echo Next Steps:
echo 1. Edit .env file with your API keys
echo 2. Add credentials.json file
echo 3. Run: python main.py
echo 4. Open frontend\index.html in your browser
echo.
echo Press any key to exit...
pause >nul
