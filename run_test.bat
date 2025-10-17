@echo off
REM GENESIS-SOVEREIGN Quick Test Runner
REM Runs the test suite with proper environment setup

echo ========================================
echo   GENESIS-SOVEREIGN Test Runner
echo   Hex Protocol: 0x47454E45534953
echo ========================================
echo.

REM Check if Ollama is running
echo [1/3] Checking Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo   X Ollama not responding on localhost:11434
    echo.
    echo   Please start Ollama in another terminal:
    echo   ^> ollama serve
    echo.
    pause
    exit /b 1
) else (
    echo   √ Ollama is running
)
echo.

REM Check virtual environment
echo [2/3] Checking Python environment...
if not exist .venv (
    echo   X Virtual environment not found
    echo   Run setup.bat first
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
echo   √ Virtual environment activated
echo.

REM Check if dependencies are installed
python -c "import asyncio" 2>nul
if errorlevel 1 (
    echo   X Dependencies not installed
    echo   Installing now...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo   X Failed to install dependencies
        pause
        exit /b 1
    )
)
echo   √ Dependencies ready
echo.

REM Run the test
echo [3/3] Running GENESIS test...
echo.
python test_genesis.py

echo.
echo ========================================
echo   Test Complete
echo ========================================
echo.

if errorlevel 1 (
    echo Result: FAILED
    echo Check error messages above
) else (
    echo Result: SUCCESS
    echo The Genesis Engine is operational!
)

echo.
pause
