@echo off
REM Setup script for Amazon Order Automation with Stagehand AI (Windows)
REM Author: qm-somesh
REM Date: 2025-10-23

echo ==================================================
echo Amazon Order Automation - Setup Script
echo Powered by Stagehand AI
echo ==================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3 is not installed. Please install Python 3.9 or higher.
    exit /b 1
)

echo ✓ Found Python
python --version

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed. Please install Node.js 16+ for Stagehand AI.
    exit /b 1
)

echo ✓ Found Node.js
node --version

REM Create virtual environment
echo.
echo Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo ✓ Virtual environment activated

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install Python dependencies
echo.
echo Installing Python dependencies...
pip install -r requirements.txt

echo ✓ Python dependencies installed

REM Install Stagehand via npm
echo.
echo Installing Stagehand AI...
call npm install @browserbasehq/stagehand

echo ✓ Stagehand AI installed

REM Check for wkhtmltopdf
echo.
echo Checking for wkhtmltopdf (required for PDF generation)...
where wkhtmltopdf >nul 2>&1
if errorlevel 1 (
    echo WARNING: wkhtmltopdf not found. Please install it manually:
    echo   Download from https://wkhtmltopdf.org/downloads.html
) else (
    echo ✓ wkhtmltopdf is installed
)

REM Create output directories
echo.
echo Creating output directories...
if not exist "output" mkdir output
if not exist "screenshots" mkdir screenshots

echo ✓ Output directories created

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo.
    echo Creating .env file from template...
    copy .env.example .env
    echo ✓ .env file created
    echo.
    echo IMPORTANT: Please edit .env file and add your Amazon credentials:
    echo   - AMAZON_EMAIL
    echo   - AMAZON_PASSWORD
) else (
    echo.
    echo ✓ .env file already exists
)

REM Summary
echo.
echo ==================================================
echo Setup Complete! 🎉
echo ==================================================
echo.
echo Next steps:
echo 1. Edit .env file with your Amazon credentials
echo 2. Run the automation:
echo    python src\amazon_automation.py
echo.
echo For more information, see README.md
echo.

pause
