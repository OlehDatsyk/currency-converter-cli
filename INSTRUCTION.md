# 📘 Beginner's Complete Guide - Currency Converter CLI

Welcome! This guide assumes you have **never used** Python, Visual Studio Code, Git, a terminal, or an API before. Every step is spelled out. Just follow along from top to bottom - you don't need to skip ahead or already know anything.

By the end, you'll have a working program on your computer that looks up real currency exchange rates and converts money between currencies, right from a terminal window.

---

## Table of Contents

1. [What This App Actually Is](#1-what-this-app-actually-is)
2. [Installing Python](#2-installing-python)
3. [Installing Git (optional but recommended)](#3-installing-git-optional-but-recommended)
4. [Installing Visual Studio Code](#4-installing-visual-studio-code)
5. [Required VS Code Extensions](#5-required-vs-code-extensions)
6. [Opening the Project](#6-opening-the-project)
7. [What Is a Terminal?](#7-what-is-a-terminal)
8. [Creating a Virtual Environment](#8-creating-a-virtual-environment)
9. [Activating the Virtual Environment](#9-activating-the-virtual-environment)
10. [Installing Dependencies](#10-installing-dependencies)
11. [Getting a Free API Key](#11-getting-a-free-api-key)
12. [Creating and Configuring the .env File](#12-creating-and-configuring-the-env-file)
13. [Running the Application](#13-running-the-application)
14. [Using Every Feature](#14-using-every-feature)
15. [Testing the Application](#15-testing-the-application)
16. [Troubleshooting](#16-troubleshooting)
17. [FAQ](#17-faq)
18. [Common Mistakes](#18-common-mistakes)
19. [Security Recommendations](#19-security-recommendations)
20. [Next Learning Steps](#20-next-learning-steps)

---

## 1. What This App Actually Is

This is a **CLI application** - CLI stands for "Command Line Interface." That means there are no buttons or windows to click; instead, you type text into a black-and-white (well, colorful, thanks to this app) window called a **terminal**, and the program responds with text.

What it does, step by step:
1. You type in a currency you're converting **from** (like `USD` for US Dollars).
2. You type in a currency you're converting **to** (like `EUR` for Euros).
3. You type an amount (like `100`).
4. The app contacts a real currency-exchange website over the internet, gets the current exchange rate, and shows you the converted amount in a neat table.

---

## 2. Installing Python

Python is the programming language this app is written in. Your computer needs it installed to run the app.

**Check if you already have it:**

1. Open a terminal. (Don't worry - [Section 7](#7-what-is-a-terminal) explains exactly what this is and how to open one; you can also just open VS Code first per Section 4 and use its built-in terminal.)
2. Type this and press Enter:
   ```bash
   python --version
   ```
3. If you see something like `Python 3.12.4`, you already have it - skip to [Section 3](#3-installing-git-optional-but-recommended).
4. If you see an error like "command not found" or "not recognized," you need to install it - keep reading.

**Installing Python on Windows:**

1. Go to <https://www.python.org/downloads/windows/>
2. Click the yellow "Download Python 3.x.x" button.
3. Open the downloaded file.
4. **Very important:** On the first installer screen, check the box at the bottom that says **"Add python.exe to PATH"** before clicking Install. This is the single most common mistake beginners make - skipping this causes "python is not recognized" errors later.
5. Click **Install Now** and wait for it to finish.
6. Close and reopen any terminal windows, then run `python --version` again to confirm.

**Installing Python on macOS:**

- Option A: Go to <https://www.python.org/downloads/macos/>, download the installer, and run it like any other Mac application.
- Option B (if you have Homebrew): open Terminal and run:
  ```bash
  brew install python@3.12
  ```

**Installing Python on Linux (Debian/Ubuntu):**

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv
```

---

## 3. Installing Git (Optional but Recommended)

Git is a tool for tracking changes to code and uploading projects to GitHub. **You don't strictly need it to run this app**, but it's good to have.

1. Go to <https://git-scm.com/downloads>
2. Download the version for your operating system.
3. Run the installer, accepting the default options (the defaults are fine for beginners).
4. Confirm it worked by opening a terminal and running:
   ```bash
   git --version
   ```

---

## 4. Installing Visual Studio Code

Visual Studio Code (VS Code) is the program you'll use to open, view, and run this project's code.

1. Go to <https://code.visualstudio.com/>
2. Click the big download button for your operating system.
3. Run the installer and accept the default options.
4. Open VS Code once installed to confirm it launches.

---

## 5. Required VS Code Extensions

An "extension" adds extra functionality to VS Code. You need one for this project:

1. Open VS Code.
2. Click the **Extensions** icon in the left-hand sidebar (it looks like four small squares, one detached - or press `Ctrl+Shift+X` on Windows/Linux, `Cmd+Shift+X` on Mac).
3. Type `Python` into the search box.
4. Find the extension called **Python**, published by **Microsoft**, and click **Install**.

That's the only extension you strictly need. It gives VS Code the ability to understand Python code, run it, and let you pick which Python environment to use.

---

## 6. Opening the Project

1. Open VS Code.
2. Go to the top menu: `File` -> `Open Folder...`
3. Browse to and select the `currency-converter-cli` folder.
4. Click **Select Folder** (Windows/Linux) or **Open** (Mac).

You should now see the project's files listed in the sidebar on the left: `main.py`, `currency_service.py`, `config.py`, `utils.py`, `requirements.txt`, `.gitignore`, `.env.example`, and `README.md`.

---

## 7. What Is a Terminal?

A terminal is a text-based window where you type commands instead of clicking buttons. VS Code has one built in, so you don't need to open a separate program.

**To open the terminal inside VS Code:**

1. Go to the top menu: `Terminal` -> `New Terminal`.
2. A panel appears at the bottom of the VS Code window with a blinking cursor - that's your terminal, already pointed at your project folder.

You'll type all the commands in the rest of this guide into that panel, pressing **Enter** after each one.

---

## 8. Creating a Virtual Environment

A **virtual environment** is an isolated, self-contained copy of Python just for this one project. It keeps this project's dependencies (the external code libraries it needs) separate from anything else on your computer, so nothing conflicts.

In the terminal, run:

```bash
python -m venv venv
```

(On macOS/Linux, if `python` doesn't work, try `python3` instead.)

Nothing dramatic will appear to happen - but a new folder called `venv` will now exist inside your project. That's your isolated Python environment.

> **Note:** If a `venv` (or `.venv`) folder already exists from a previous setup, you can either reuse it (skip to [Section 9](#9-activating-the-virtual-environment)) or delete it and recreate it fresh with the command above.

---

## 9. Activating the Virtual Environment

"Activating" tells your terminal to use the isolated Python environment you just created, instead of your computer's system-wide Python. **You must do this every time you open a new terminal to work on this project.**

**Windows (Command Prompt):**
```bat
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```
> If you get an error about "execution policies," open PowerShell **as Administrator** and run this once:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```
> Then try activating again in a normal (non-admin) terminal.

**macOS / Linux:**
```bash
source venv/bin/activate
```

**How do you know it worked?** Your terminal prompt will now start with `(venv)`, like this:
```
(venv) C:\Users\you\currency-converter-cli>
```

---

## 10. Installing Dependencies

"Dependencies" are external code libraries the app needs to work - things other people already wrote so you don't have to. With your virtual environment **activated** (you see `(venv)` in the prompt), run:

```bash
pip install -r requirements.txt
```

This installs three things:
- **`requests`** - lets the app make internet calls to fetch exchange rates
- **`python-dotenv`** - lets the app read your secret API key from a `.env` file
- **`rich`** - makes the terminal output colorful and nicely formatted

You'll see pip download and install each one. When it finishes without red error text, you're done.

---

## 11. Getting a Free API Key

This app needs a **free API key** from ExchangeRate-API.com to fetch live exchange rates. An API key is like a personal password that identifies you to that service.

1. Go to <https://www.exchangerate-api.com/>
2. Click **"Get Free Key"**.
3. Enter your email address and create a free account.
4. Check your email inbox (and Spam folder) for a confirmation link, and click it.
5. Once logged in, your dashboard will show your **API Key** - a string of letters and numbers.
6. Copy that key. You'll paste it in the next step.

The free tier gives you 1,500 requests per month - plenty for learning and personal use.

---

## 12. Creating and Configuring the `.env` File

Your API key is a secret. It should never be typed directly into the code or shared publicly - it lives in a separate file called `.env` that stays on your computer only.

**Step 1 - Create the file.** In the VS Code terminal, run:

**Windows:**
```bat
copy .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
```

This creates a new file called `.env`, copied from the `.env.example` template.

**Step 2 - Edit the file.**
1. In the VS Code file explorer (left sidebar), click on `.env`.
2. Find the line `EXCHANGE_RATE_API_KEY=your_api_key_here`.
3. Replace `your_api_key_here` with the real key you copied in Section 11, so it looks like:
   ```dotenv
   EXCHANGE_RATE_API_KEY=a1b2c3d4e5f6g7h8i9j0
   ```
4. Leave the other two lines (`EXCHANGE_RATE_API_BASE_URL` and `REQUEST_TIMEOUT_SECONDS`) as they are - the defaults work fine.
5. Save the file: `Ctrl+S` (Windows/Linux) or `Cmd+S` (Mac).

`.env` is listed in `.gitignore`, so it will never be accidentally uploaded to GitHub - but see [Section 19](#19-security-recommendations) for more on keeping it safe.

---

## 13. Running the Application

Make sure all three of these are true first:
- ✅ Your terminal shows `(venv)` at the start of the line (see Section 9)
- ✅ You ran `pip install -r requirements.txt` successfully (Section 10)
- ✅ Your `.env` file has your real API key in it (Section 12)

Then run:

```bash
python main.py
```

(On macOS/Linux, use `python3 main.py` if `python` isn't recognized.)

---

## 14. Using Every Feature

When you run the app, here's exactly what happens and what to type:

1. **Banner:** A colorful title box appears - no input needed here, just confirms the app started.
2. **"Enter the source currency code (e.g. USD)":** Type the 3-letter code of the currency you're converting *from*, e.g. `USD`, `GBP`, `JPY`. Lowercase is fine - the app automatically converts it to uppercase.
3. **"Enter the target currency code (e.g. USD)":** Type the 3-letter code of the currency you're converting *to*, e.g. `EUR`.
4. **"Enter the amount to convert":** Type a positive number, e.g. `100` or `99.95`. Commas (like `1,000`) are accepted too.
5. **Result table:** The app fetches the live rate and prints a table showing:
   - Source Currency
   - Target Currency
   - Amount
   - Exchange Rate
   - Converted Amount (highlighted in green)
   - Last Updated (when that rate was last refreshed by the provider)

**What if I type something wrong?**
- If you type an invalid currency format (not exactly 3 letters), the app tells you immediately and asks again - no internet call is even made.
- If you type a currency code that's correctly formatted but doesn't actually exist (like `XYZ`), the app will contact the API, discover it's unsupported, and show a clear error message.
- If you type a non-numeric or negative amount, the app rejects it and asks again.

**To run another conversion:** Just run `python main.py` again. Each run performs exactly one conversion.

**To exit at any prompt:** Press `Ctrl+C`. The app will show "Cancelled by user" and close cleanly.

---

## 15. Testing the Application

This project doesn't currently include an automated test suite (this is noted in `PROJECT_REVIEW.md`), so "testing" here means manually trying out different scenarios to confirm everything works:

| Try this | Expected result |
|---|---|
| Source: `USD`, Target: `EUR`, Amount: `100` | A normal result table with a real exchange rate |
| Source: `usd` (lowercase) | Still works - automatically capitalized |
| Source: `US` (2 letters) | Immediate "Invalid currency code" message, no internet call |
| Source: `XYZ` (not a real currency) | "Invalid currency" error after contacting the API |
| Amount: `-5` | "Amount must be a positive number" error |
| Amount: `abc` | "Invalid amount" error |
| Turn off your Wi-Fi, then run the app | "Network error: Could not connect..." message |

If you'd like proper automated tests added later (using `pytest`), that's listed as a recommended next step in `PROJECT_REVIEW.md`.

---

## 16. Troubleshooting

| Problem | Likely Cause | Solution |
|---|---|---|
| `'python' is not recognized...` | Python not installed or not added to PATH | Reinstall Python, making sure to check "Add python.exe to PATH" |
| `ModuleNotFoundError: No module named 'rich'` | Dependencies not installed, or venv not activated | Activate venv (Section 9), then re-run `pip install -r requirements.txt` |
| `Configuration error: Missing required environment variable` | `.env` file missing or empty | Repeat Section 12 |
| `API error: The configured API key is invalid` | Wrong/mistyped key | Re-check your key on the ExchangeRate-API dashboard and re-paste it |
| `Rate limit exceeded` | You've used your free monthly quota (1,500 requests) | Wait for next month's reset, or upgrade your plan |
| `Network error: ...timed out` | No/slow internet, or a firewall blocking the request | Check your connection; check firewall/VPN |
| PowerShell blocks venv activation | Windows execution policy | Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` in an admin PowerShell |
| `(venv)` missing from prompt | You opened a *new* terminal without activating in it | Re-run the activation command from Section 9 in the current terminal |
| App can't find `main.py` | Terminal isn't in the right folder | Run `cd path/to/currency-converter-cli`, or reopen the folder via `File -> Open Folder` |

**Still stuck?** Try a completely fresh virtual environment:
```bash
# delete the old one first (Windows: rmdir /s venv)
rm -rf venv
python -m venv venv
# then activate it again (Section 9) and reinstall:
pip install -r requirements.txt
```

---

## 17. FAQ

**Do I need to know how to code to use this?**
No - you just need to follow the setup steps once. Using the app afterward is just answering three prompts.

**Do I need to activate the virtual environment every single time?**
Yes, every time you open a *new* terminal window for this project. If you close VS Code and reopen it later, you'll need to activate again.

**Is my API key safe?**
It stays in your local `.env` file only, and `.gitignore` prevents it from being uploaded if you use Git. See [Section 19](#19-security-recommendations) for more.

**Can I use this without an internet connection?**
No - it needs to reach the exchange rate API live for every conversion.

**Does this cost money?**
No. The free ExchangeRate-API tier (1,500 requests/month) is more than enough for personal use.

**Can I convert more than one amount without restarting?**
Not currently - each run of `python main.py` does exactly one conversion. Running it again is quick, though.

---

## 18. Common Mistakes

- **Forgetting to activate the virtual environment** before installing dependencies or running the app - this causes `ModuleNotFoundError`.
- **Forgetting to check "Add python.exe to PATH"** during the Windows Python installer - this causes `'python' is not recognized`.
- **Leaving `your_api_key_here` in `.env`** instead of replacing it with a real key.
- **Editing `.env.example` instead of `.env`** - always edit the copy named exactly `.env`, not the template.
- **Typing currency names instead of codes**, e.g. typing `Dollars` instead of `USD`.
- **Sharing or uploading the project folder (or a ZIP of it) without removing `.env` first** - see the next section.

---

## 19. Security Recommendations

- **Never share your `.env` file** - not in chat, not in a ZIP, not in a screenshot, not in a support ticket. It contains your live API key.
- **Never paste your API key directly into `main.py`, `config.py`, or any other source file.** The whole point of `.env` is to keep secrets out of your code.
- **Before zipping this project to share with anyone**, delete or exclude: `.env`, `venv/` (or `.venv/`), and `__pycache__/`. None of these should ever leave your computer.
- **If you ever suspect your API key has been exposed** (e.g., accidentally committed to a public GitHub repo, or shared in a ZIP), go to your ExchangeRate-API dashboard and regenerate a new key immediately - treat the old one as compromised.
- **If you use Git**, double-check with `git status` before your first commit that `.env` is *not* listed as a file to be committed - it should be silently ignored thanks to `.gitignore`.

---

## 20. Next Learning Steps

Once you're comfortable running and using this app, here are natural next steps to keep learning:

1. **Read the code** - start with `utils.py` (the simplest file), then `config.py`, then `currency_service.py`, then `main.py`. Try to predict what each function does before reading its docstring.
2. **Make a small change** - e.g., change the app's title in `main.py`, or add a new field to the result table (like a "fee" calculation).
3. **Learn `pytest`** and try writing one test for `utils.normalize_currency_code` - it's a small, pure function and a great first test to write.
4. **Learn Git basics** - `git init`, `git add`, `git commit` - so you can track your own changes over time.
5. **Publish it to GitHub** - once you've read `PROJECT_REVIEW.md`'s GitHub Readiness section and rotated your API key, this project is genuinely ready to share.
6. **Explore the "Future Improvements" list in README.md** - batch conversion, a FastAPI web wrapper, and historical rate charts are all realistic next projects once you're comfortable with the basics.

You now have everything you need to install, run, use, and safely maintain this project. Good luck, and enjoy learning!
