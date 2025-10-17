@echo off
echo ========================================
echo 🌟 GENESIS-SOVEREIGN Setup Script
echo ========================================
echo.

echo [1/5] Checking Python installation...
python --version
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.11 or later
    pause
    exit /b 1
)
echo ✓ Python found
echo.

echo [2/5] Creating .venv virtual environment...
if exist .venv (
    echo   .venv already exists
) else (
    python -m venv .venv
    echo ✓ .venv created
)
echo.

echo [3/5] Activating .venv and upgrading pip...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
echo ✓ pip upgraded
echo.

echo [4/5] Installing dependencies...
pip install -r requirements.txt
echo ✓ Dependencies installed
echo.

echo [5/5] Creating .env file...
if exist .env (
    echo   .env already exists
) else (
    copy .env.example .env >nul
    echo ✓ .env created - EDIT THIS FILE WITH YOUR CREDENTIALS!
)
echo.

echo ========================================
echo ✓ Setup Complete!
echo ========================================
echo.
echo To activate .venv: .venv\Scripts\activate
echo Signal: LIVE
echo Hex: 0x47454E45534953
echo ========================================
pause
