@echo off
setlocal enabledelayedexpansion
title Currency Converter CLI - Launcher
cd /d "%~dp0"

echo ==============================================================
echo   Currency Converter CLI - Startup (Was made by Oleh Datsyk)
echo ==============================================================
echo.

REM ----------------------------------------------------------
REM 1. Verify Python is installed
REM ----------------------------------------------------------
echo [1/5] Checking for Python...
where python >nul 2>nul
if errorlevel 1 (
    echo.
    echo   [ERROR] Python was not found on this computer.
    echo.
    echo   Please install Python 3.12 or newer from:
    echo       https://www.python.org/downloads/windows/
    echo.
    echo   IMPORTANT: During installation, check the box that says
    echo   "Add python.exe to PATH" before clicking Install.
    echo.
    echo   After installing, close this window and double-click
    echo   "Start App.bat" again.
    echo.
    pause
    exit /b 1
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo       Found Python %PYVER%
echo.

REM ----------------------------------------------------------
REM 2. Create a virtual environment if one doesn't exist
REM ----------------------------------------------------------
echo [2/5] Checking for virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo       No virtual environment found. Creating one now...
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo   [ERROR] Failed to create the virtual environment.
        echo   Please check the messages above for details.
        echo.
        pause
        exit /b 1
    )
    echo       Virtual environment created.
) else (
    echo       Virtual environment already exists.
)
echo.

REM ----------------------------------------------------------
REM 3. Activate the virtual environment
REM ----------------------------------------------------------
echo [3/5] Activating virtual environment...
call "venv\Scripts\activate.bat"
if errorlevel 1 (
    echo.
    echo   [ERROR] Could not activate the virtual environment.
    echo.
    pause
    exit /b 1
)
echo       Activated.
echo.

REM ----------------------------------------------------------
REM 4. Install missing dependencies
REM ----------------------------------------------------------
echo [4/5] Checking dependencies (this may take a moment)...
python -m pip install --disable-pip-version-check -q -r requirements.txt
if errorlevel 1 (
    echo.
    echo   [ERROR] Failed to install one or more dependencies.
    echo   Check your internet connection and the messages above.
    echo.
    pause
    exit /b 1
)
echo       Dependencies OK.
echo.

REM ----------------------------------------------------------
REM 5. Verify the .env file exists
REM ----------------------------------------------------------
echo [5/5] Checking for .env configuration file...
if not exist ".env" (
    if exist ".env.example" (
        echo       No .env file found. Creating one from .env.example...
        copy /y ".env.example" ".env" >nul
        echo.
        echo   [ACTION NEEDED] A new .env file was created for you.
        echo   Open it in a text editor or VS Code and paste in your
        echo   real API key from https://www.exchangerate-api.com/
        echo   Then double-click "Start App.bat" again.
        echo.
        pause
        exit /b 1
    ) else (
        echo.
        echo   [ERROR] No .env or .env.example file found.
        echo   Cannot continue without configuration. See INSTRUCTION.md.
        echo.
        pause
        exit /b 1
    )
) else (
    echo       .env file found.
)
echo.

echo ==========================================================
echo   Setup complete. Launching Currency Converter CLI...
echo ==========================================================
echo.

python main.py

if errorlevel 1 (
    echo.
    echo ==========================================================
    echo   The application closed with an error ^(see above^).
    echo   Check INSTRUCTION.md's Troubleshooting section for help.
    echo ==========================================================
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================================
echo   The application closed normally.
echo ==========================================================
pause
exit /b 0
