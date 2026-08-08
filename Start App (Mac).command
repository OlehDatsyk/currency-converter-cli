#!/bin/bash

# ==========================================================
#  Currency Converter CLI - Startup (macOS)
#  Double-click this file to run. If macOS blocks it the
#  first time, see INSTRUCTION.md / the note at the bottom
#  of this file for how to allow it.
# ==========================================================

# Always run from the folder this script lives in
cd "$(dirname "$0")" || exit 1

echo "=============================================================="
echo "  Currency Converter CLI - Startup (Was made by Oleh Datsyk)"
echo "=============================================================="
echo

pause_and_exit() {
    echo
    read -n 1 -s -r -p "Press any key to close this window..."
    echo
    exit "${1:-1}"
}

# ----------------------------------------------------------
# 1. Verify Python is installed
# ----------------------------------------------------------
echo "[1/5] Checking for Python..."

PYTHON_CMD=""
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
fi

if [ -z "$PYTHON_CMD" ]; then
    echo
    echo "  [ERROR] Python was not found on this computer."
    echo
    echo "  Please install Python 3.12 or newer from:"
    echo "      https://www.python.org/downloads/macos/"
    echo "  or, if you use Homebrew:"
    echo "      brew install python@3.12"
    echo
    echo "  After installing, close this window and double-click"
    echo "  'Start App (Mac).command' again."
    pause_and_exit 1
fi

PYVER=$("$PYTHON_CMD" --version 2>&1)
echo "      Found $PYVER"
echo

# ----------------------------------------------------------
# 2. Create a virtual environment if one doesn't exist
# ----------------------------------------------------------
echo "[2/5] Checking for virtual environment..."
if [ ! -f "venv/bin/activate" ]; then
    echo "      No virtual environment found. Creating one now..."
    "$PYTHON_CMD" -m venv venv
    if [ $? -ne 0 ]; then
        echo
        echo "  [ERROR] Failed to create the virtual environment."
        echo "  Please check the messages above for details."
        pause_and_exit 1
    fi
    echo "      Virtual environment created."
else
    echo "      Virtual environment already exists."
fi
echo

# ----------------------------------------------------------
# 3. Activate the virtual environment
# ----------------------------------------------------------
echo "[3/5] Activating virtual environment..."
# shellcheck disable=SC1091
source "venv/bin/activate"
if [ $? -ne 0 ]; then
    echo
    echo "  [ERROR] Could not activate the virtual environment."
    pause_and_exit 1
fi
echo "      Activated."
echo

# ----------------------------------------------------------
# 4. Install missing dependencies
# ----------------------------------------------------------
echo "[4/5] Checking dependencies (this may take a moment)..."
python -m pip install --disable-pip-version-check -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo
    echo "  [ERROR] Failed to install one or more dependencies."
    echo "  Check your internet connection and the messages above."
    pause_and_exit 1
fi
echo "      Dependencies OK."
echo

# ----------------------------------------------------------
# 5. Verify the .env file exists
# ----------------------------------------------------------
echo "[5/5] Checking for .env configuration file..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "      No .env file found. Creating one from .env.example..."
        cp ".env.example" ".env"
        echo
        echo "  [ACTION NEEDED] A new .env file was created for you."
        echo "  Open it in a text editor or VS Code and paste in your"
        echo "  real API key from https://www.exchangerate-api.com/"
        echo "  Then double-click 'Start App (Mac).command' again."
        pause_and_exit 1
    else
        echo
        echo "  [ERROR] No .env or .env.example file found."
        echo "  Cannot continue without configuration. See INSTRUCTION.md."
        pause_and_exit 1
    fi
else
    echo "      .env file found."
fi
echo

echo "=========================================================="
echo "  Setup complete. Launching Currency Converter CLI..."
echo "=========================================================="
echo

python main.py
APP_EXIT_CODE=$?

if [ $APP_EXIT_CODE -ne 0 ]; then
    echo
    echo "=========================================================="
    echo "  The application closed with an error (see above)."
    echo "  Check INSTRUCTION.md's Troubleshooting section for help."
    echo "=========================================================="
    pause_and_exit 1
fi

echo
echo "=========================================================="
echo "  The application closed normally."
echo "=========================================================="
pause_and_exit 0

# ----------------------------------------------------------
# NOTE: If macOS shows "cannot be opened because it is from
# an unidentified developer" the first time you double-click
# this file:
#   1. Right-click (or Control-click) the file
#   2. Choose "Open"
#   3. Click "Open" again in the dialog that appears
# You only need to do this once.
# ----------------------------------------------------------
