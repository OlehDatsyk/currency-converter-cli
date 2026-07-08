# 💱 Currency Converter CLI

A production-ready, command-line currency converter written in Python. It
fetches **live exchange rates** from a real API and displays a clean,
color-coded result table right in your terminal using the
[Rich](https://github.com/Textualize/rich) library.

This README assumes **zero prior experience**. If you have only ever
installed Visual Studio Code, you will still be able to follow every step
and get this project running.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Features](#2-features)
3. [Folder Structure](#3-folder-structure)
4. [Prerequisites](#4-prerequisites)
5. [Step-by-Step Installation Guide](#5-step-by-step-installation-guide)
6. [Getting Your Free API Key](#6-getting-your-free-api-key)
7. [Configuring the `.env` File](#7-configuring-the-env-file)
8. [Running the Project in VS Code](#8-running-the-project-in-vs-code)
9. [Example Terminal Output](#9-example-terminal-output)
10. [Troubleshooting](#10-troubleshooting)
11. [Future Improvements](#11-future-improvements)
12. [License](#12-license)

---

## 1. Project Overview

This application is a **CLI (Command Line Interface)** tool. That means
there is no window with buttons to click — you interact with it entirely by
typing in a terminal. You will be asked to:

1. Enter a **source currency** (the currency you're converting *from*, e.g. `USD`)
2. Enter a **target currency** (the currency you're converting *to*, e.g. `EUR`)
3. Enter an **amount** to convert

The app then calls a live currency exchange API over the internet and
prints a neatly formatted table with the result.

The codebase follows **Clean Architecture** principles — each file has a
single, clear responsibility, making the project easy to read, test, and
extend.

---

## 2. Features

- ✅ Convert between any two supported ISO 4217 currency codes (USD, EUR, GBP, JPY, etc.)
- ✅ Live, real-time exchange rates fetched from an external API
- ✅ Beautiful, color-coded terminal output using **Rich**
- ✅ Displays: Source Currency, Target Currency, Amount, Exchange Rate,
  Converted Amount, and Last Updated timestamp
- ✅ Full input validation (rejects empty, malformed, or negative amounts and
  malformed currency codes before ever calling the API)
- ✅ Graceful handling of invalid currencies (e.g. typing `XYZ`)
- ✅ Graceful handling of API errors (bad key, quota exceeded, inactive account)
- ✅ Graceful handling of network errors (no internet connection, timeout)
- ✅ Configuration via environment variables (`.env` file) — no secrets hardcoded
- ✅ Fully typed with Python type hints
- ✅ PEP 8 compliant, modular, object-oriented where appropriate

---

## 3. Folder Structure

```
currency-converter-cli/
│
├── main.py               # Entry point — CLI UI, input prompts, output rendering
├── currency_service.py   # Handles all communication with the exchange rate API
├── config.py              # Loads and validates environment variables
├── utils.py                # Validation & formatting helper functions
├── requirements.txt        # Python dependencies
├── .env.example            # Template for your environment variables
├── .gitignore               # Files/folders Git should ignore
└── README.md                 # You are here
```

**Why is it structured this way?**

| File                 | Responsibility                                                            |
|----------------------|-----------------------------------------------------------------------------|
| `main.py`             | Only handles the terminal UI: prompts, printing, and wiring everything together |
| `currency_service.py` | Only handles talking to the API and turning responses into Python objects |
| `config.py`            | Only handles reading and validating environment variables               |
| `utils.py`             | Only handles small, reusable, testable helper logic (validation, formatting) |

This separation means you could, for example, swap the terminal UI for a
web UI later without touching `currency_service.py` at all.

---

## 4. Prerequisites

Before you begin, make sure you have the following installed. If you
already have them, you can skip to the next section.

### 4.1 Visual Studio Code

You said you already have this installed. If not, download it from
<https://code.visualstudio.com/> and install it like any other application.

**Recommended VS Code extension:** Once VS Code is open, install the
official **Python** extension (by Microsoft):

1. Click the Extensions icon in the left sidebar (or press `Ctrl+Shift+X` / `Cmd+Shift+X`)
2. Search for `Python`
3. Click **Install** on the extension published by Microsoft

### 4.2 Python 3.12 or newer

This project requires **Python 3.12+**.

**Check if Python is already installed:**

Open a terminal (in VS Code: `Terminal` → `New Terminal`) and run:

```bash
python --version
```

or, on macOS/Linux, you may need:

```bash
python3 --version
```

If you see something like `Python 3.12.x` or higher, you're good to go.

**If Python is not installed (or the version is too old):**

- **Windows:** Download the installer from
  <https://www.python.org/downloads/windows/>.
  ⚠️ During installation, **check the box that says "Add python.exe to PATH"**
  before clicking Install — this is the #1 cause of "python is not
  recognized" errors later.
- **macOS:** Download the installer from
  <https://www.python.org/downloads/macos/>, or if you use
  [Homebrew](https://brew.sh/), run:
  ```bash
  brew install python@3.12
  ```
- **Linux (Debian/Ubuntu):**
  ```bash
  sudo apt update
  sudo apt install python3.12 python3.12-venv
  ```

After installing, **close and reopen your terminal** and re-run the
`python --version` command to confirm it worked.

### 4.3 Git (optional)

Git is only needed if you plan to clone this project from a repository or
put it under version control. It is **not required** to simply run the app.
If you want it anyway, download it from <https://git-scm.com/downloads>.

---

## 5. Step-by-Step Installation Guide

### Step 1 — Open the project folder in VS Code

1. Open Visual Studio Code
2. Go to `File` → `Open Folder...`
3. Select the `currency-converter-cli` folder
4. Click **Select Folder**

### Step 2 — Open a terminal inside VS Code

Go to the top menu: `Terminal` → `New Terminal`.
A terminal panel will appear at the bottom of VS Code, already pointed at
your project folder.

### Step 3 — Create a virtual environment

A **virtual environment** is an isolated Python installation just for this
project, so its dependencies don't clash with other projects on your
computer. In the terminal, run:

```bash
python -m venv venv
```

(On macOS/Linux, use `python3` instead of `python` if needed:)

```bash
python3 -m venv venv
```

This creates a new folder called `venv/` inside your project.

### Step 4 — Activate the virtual environment

You must **activate** the virtual environment every time you open a new
terminal to work on this project.

**Windows (Command Prompt):**
```bat
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```
> If PowerShell blocks the script with an execution-policy error, run this
> once (in an Administrator PowerShell window) and try again:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

**macOS / Linux (bash/zsh):**
```bash
source venv/bin/activate
```

You'll know it worked when you see `(venv)` appear at the start of your
terminal prompt line.

> 💡 **Tip:** VS Code often detects the `venv` folder automatically and
> asks "Select Interpreter" — if a popup appears in the bottom-right
> corner, click it and choose the interpreter located inside `venv`.

### Step 5 — Install the dependencies

With the virtual environment activated, run:

```bash
pip install -r requirements.txt
```

This installs:
- `requests` — for making HTTP calls to the exchange rate API
- `python-dotenv` — for loading your `.env` configuration file
- `rich` — for the colorful terminal output

You should see pip download and install each package with no errors.

---

## 6. Getting Your Free API Key

This project uses **[ExchangeRate-API.com](https://www.exchangerate-api.com/)**,
which offers a free tier that's more than enough for personal projects.

1. Go to <https://www.exchangerate-api.com/>
2. Click **"Get Free Key"**
3. Enter your email address and create a free account
4. Verify your email address (check your inbox for a confirmation link —
   also check your Spam folder)
5. Once logged in, you'll see your **API Key** on your account dashboard.
   It looks something like: `a1b2c3d4e5f6g7h8i9j0`
6. Copy that key — you'll paste it into the `.env` file in the next step

> The free tier includes 1,500 requests per month, which is plenty for
> learning and personal use.

---

## 7. Configuring the `.env` File

Your API key is a secret and should **never** be typed directly into the
source code or committed to Git. Instead, it lives in a local `.env` file.

### Step 1 — Create your `.env` file

In the VS Code terminal (from the project's root folder), run:

**Windows (Command Prompt):**
```bat
copy .env.example .env
```

**macOS / Linux:**
```bash
cp .env.example .env
```

This creates a new file called `.env` — a copy of `.env.example`.

### Step 2 — Edit the `.env` file

1. In the VS Code file explorer (left sidebar), click on the new `.env` file
2. Replace `your_api_key_here` with the real API key you copied in Step 6

It should look like this:

```dotenv
EXCHANGE_RATE_API_KEY=a1b2c3d4e5f6g7h8i9j0
EXCHANGE_RATE_API_BASE_URL=https://v6.exchangerate-api.com/v6
REQUEST_TIMEOUT_SECONDS=10
```

3. Save the file (`Ctrl+S` / `Cmd+S`)

> ⚠️ The `.env` file is listed in `.gitignore`, so it will never
> accidentally be uploaded to GitHub or shared with anyone.

---

## 8. Running the Project in VS Code

Make sure:
- Your virtual environment is activated (you see `(venv)` in the terminal)
- You've run `pip install -r requirements.txt`
- Your `.env` file is created and filled in with a real API key

Then, in the VS Code terminal, run:

```bash
python main.py
```

(On macOS/Linux, use `python3 main.py` if `python` isn't recognized.)

You'll be prompted to enter a source currency, a target currency, and an
amount. Follow the on-screen prompts.

> 💡 You can also run the file by opening `main.py` in the editor and
> clicking the ▶ **Run** button in the top-right corner of VS Code.

---

## 9. Example Terminal Output

```
╭──────────────────────────────────────────╮
│ 💱  Currency Converter CLI                │
│ Live exchange rates, right in your        │
│ terminal                                  │
╰──────────────────────────────────────────╯
Enter the source currency code (e.g. USD): usd
Enter the target currency code (e.g. USD): eur
Enter the amount to convert: 100

                 Conversion Result
╭──────────────────┬─────────────────────────╮
│ Source Currency    │ USD                     │
│ Target Currency     │ EUR                    │
│ Amount                │ 100.00               │
│ Exchange Rate           │ 0.921500           │
│ Converted Amount         │ 92.15 EUR         │
│ Last Updated               │ 2026-07-08 09:15:42 UTC │
╰──────────────────┴─────────────────────────╯
```

### Example: Invalid currency code

```
Enter the source currency code (e.g. USD): usd
Enter the target currency code (e.g. USD): xyz
Enter the amount to convert: 50
Invalid currency: Currency code not supported by the API: 'USD' or 'XYZ'.
Please double-check the ISO 4217 currency codes (e.g. USD, EUR, GBP).
```

### Example: No internet connection

```
Network error: Could not connect to the exchange rate service.
Please check your internet connection and try again.
```

---

## 10. Troubleshooting

| Problem | Likely Cause | Solution |
|---|---|---|
| `'python' is not recognized as an internal or external command` | Python isn't installed or not added to PATH | Reinstall Python and check "Add python.exe to PATH" during setup |
| `ModuleNotFoundError: No module named 'rich'` (or `requests`, `dotenv`) | Dependencies not installed, or venv not activated | Activate the venv, then run `pip install -r requirements.txt` again |
| `Configuration error: Missing required environment variable: 'EXCHANGE_RATE_API_KEY'` | `.env` file missing or empty | Copy `.env.example` to `.env` and add your real API key |
| `API error: The configured API key is invalid` | Wrong or mistyped API key | Double-check the key on your ExchangeRate-API dashboard and re-paste it into `.env` |
| `Rate limit exceeded` | You've used up your free monthly quota | Wait until next month's reset, or upgrade your plan |
| `Network error: The request... timed out` | Slow/no internet connection, or firewall blocking the request | Check your internet connection; try again; check firewall/VPN settings |
| PowerShell says script execution is disabled when activating venv | Windows execution policy blocks scripts | Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` in an admin PowerShell, then retry |
| `(venv)` doesn't appear in the terminal after activation | You may have opened a *new* terminal after activating in a different one | Re-run the activation command in the current terminal (see Step 4 in Section 5) |
| Currency code rejected before even calling the API | You typed something that isn't exactly 3 letters | Use standard 3-letter ISO codes: USD, EUR, GBP, JPY, INR, etc. |
| App can't find `main.py` | Terminal isn't opened in the project folder | Run `cd path/to/currency-converter-cli` first, or reopen VS Code via `File → Open Folder` |

If you're still stuck, try running with a fresh virtual environment:

```bash
# delete the old one (Windows: use "rmdir /s venv")
rm -rf venv
python -m venv venv
# activate it again (see Step 4 above), then:
pip install -r requirements.txt
```

---

## 11. Future Improvements

Ideas for extending this project further:

- 🌐 Add a REST API wrapper (FastAPI) so the converter can be used as a web service
- 📊 Add historical exchange rate charts
- 💾 Cache exchange rates locally to reduce API calls and support offline retries
- 🧪 Add a full `pytest` test suite with mocked HTTP responses
- 🌍 Support batch conversion (convert one amount into multiple currencies at once)
- 🖥️ Build a GUI version using `Textual` (terminal UI) or a desktop framework
- 🔁 Add a "watch mode" that refreshes exchange rates on an interval
- 📦 Package the app with `pyinstaller` for a standalone executable
- 🗃️ Support additional exchange rate providers with a pluggable interface

---

## 12. License

This project is provided as-is for educational and personal use. Feel free
to modify and extend it for your own purposes.
