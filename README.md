#  INE Malware Builder v7.4 — README

**Expanded Browsers + Luna Features**  
*by NODE — INE Project*

---

## Overview

INE Malware Builder v7.4 is a feature-packed infostealer and payload generator with a modern dark-themed GUI. It compiles modular Python payloads into standalone Windows executables capable of harvesting credentials, sessions, files, and system intelligence from compromised machines, then exfiltrating everything through Discord webhooks.

Version 7.4 expands browser coverage to **15 Chromium-based targets**, adds Luna-inspired niche forks, and introduces WiFi extraction, clipboard capture, game session theft, anti-VM detection, anti-spam mutexing, and self-destruct cleanup.

---

## Features at a Glance

###  Credential Harvesting
| Module | Target |
|--------|--------|
| Passwords | Saved browser logins (Chromium AES-GCM decryption) |
| Cookies | All browser cookies via `browser_cookie3` |
| Credit Cards | Auto-fill payment data from browser Web Data |
| Passkeys / WebAuthn | FIDO2 credentials + Windows Credential Vault |
| Discord Tokens | Scraped from Discord client local storage |
| WiFi Passwords | All saved wireless profiles via `netsh` |
| Authenticator | Google Auth registry, WinAuth XML, Authy, browser extension TOTP seeds, Microsoft Authenticator |

###  Financial & Gaming
| Module | Target |
|--------|--------|
| Wallets | Exodus, Atomic, Electrum, Coinomi, Guarda |
| Roblox Cookies | `.roblox.com` cookies from all browsers |
| Games | Minecraft launcher accounts/tokens, Epic Games configs, MultiMC/PrismLauncher sessions |

### 🖥️ System Recon
| Module | Target |
|--------|--------|
| System Info | Hostname, OS, username, public IP, admin status |
| Screenshot | Full desktop capture (mss or PIL fallback) |
| Webcam | Single snapshot from default camera |
| Keylogger | Background keystroke capture (60s window) |
| Clipboard | Current clipboard content via PowerShell |
| Common Files | Documents/Desktop/Downloads sweep for sensitive filenames + extensions |

### 🌐 Browser Data
| Module | Target |
|--------|--------|
| Browser History | Last 300 visited URLs per profile |
| Downloads | Last 300 downloaded files + source URLs |
| Search History | Last 300 search terms |
| Extensions | Full extension directory copy from all profiles |
| Telegram Sessions | `tdata` folder copy for session hijacking |

###  Persistence & Evasion
| Module | Function |
|--------|----------|
| Disable Defender | Registry + PowerShell: RTP, behavior monitoring, cloud protection, script scanning, sample submission |
| Add Exclusion | Adds executable + temp paths to Defender exclusion list |
| Startup | Copies to Startup folder + HKCU/HKLM Run registry keys as `WindowsUpdate.exe` |
| Anti-VM/Debug | Detects VMware, VirtualBox, debugger presence, small screens — exits silently if flagged |
| Anti-Spam | Named Windows mutex prevents duplicate execution |
| Self-Destruct | Batch file loop deletes the payload executable after exfiltration |
| Fake Error | Displays a customizable `tkinter` error popup to the victim |

###  Expanded Browser Support (15 Browsers)
```
Chrome  •  Edge  •  Brave  •  Opera  •  Vivaldi
Kometa  •  Orbitum  •  CentBrowser  •  7Star  •  Sputnik
Epic Privacy  •  Uran  •  Yandex  •  Iridium
```

---

## GUI Preview

The builder window (940×900 px, non-resizable) contains:

- **Header bar** — version badge, project credit
- **Webhook row** — URL entry, Test button (validates with a ping message), Paste-from-clipboard button
- **Ping toggle** — enable/disable `@everyone` or `@here` on Discord embeds
- **Checkbox grid** — 28 toggleable modules in a 4-column layout with Select All / None / Stealers quick-filters
- **Fake Error config** — custom title + message fields
- **Build row** — format selector (`.exe` / `.py`), filename input, icon picker, BUILD button
- **Console panel** — scrolling build log with color-coded status tags

Keyboard shortcut: `Ctrl+B` triggers build.

---

## Installation

### Prerequisites
- **Python 3.9+** (with PATH enabled during install)
- **Windows 10/11** (builder and payload target)
- **Discord webhook URL** (for exfiltration)

### One-Click Dependency Install

Save the following as `install_deps.bat` and run as Administrator:

```batch
@echo off
title INE Malware Builder v7.4 — Dependency Installer
echo ========================================
echo   INE Malware Builder v7.4
echo   Dependency Installer
echo ========================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found in PATH.
    echo Install Python 3.9+ from https://python.org
    echo Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)
echo [OK] Python detected:
python --version
echo.

echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo.

echo [ 1/10] customtkinter
python -m pip install customtkinter --quiet

echo [ 2/10] requests (+ urllib3, chardet, certifi, idna)
python -m pip install requests --quiet

echo [ 3/10] Pillow (PIL, icon conversion)
python -m pip install Pillow --quiet

echo [ 4/10] pyinstaller (EXE compilation)
python -m pip install pyinstaller --quiet

echo [ 5/10] browser-cookie3
python -m pip install browser-cookie3 --quiet

echo [ 6/10] cryptography (AES-GCM decryption)
python -m pip install cryptography --quiet

echo [ 7/10] opencv-python (webcam capture)
python -m pip install opencv-python --quiet

echo [ 8/10] mss (screenshot)
python -m pip install mss --quiet

echo [ 9/10] pynput (keylogger)
python -m pip install pynput --quiet

echo [10/10] pywin32 (win32crypt, win32cred, Windows APIs)
python -m pip install pywin32 --quiet

echo.
echo ========================================
echo   All dependencies installed!
echo   You can now launch the builder.
echo ========================================
echo.
pause
```

### Manual Installation

```bash
pip install customtkinter requests Pillow pyinstaller browser-cookie3 cryptography opencv-python mss pynput pywin32
```

---

## Quick Start

1. **Launch the builder:**
   ```bash
   python builder.py
   ```

2. **Paste your Discord webhook URL** into the Webhook field and click **Test** to verify connectivity.

3. **Select features** by checking desired modules. Use the quick-filter buttons:
   - **All** — enables everything
   - **None** — clears selection
   - **Stealers** — enables all harvesting modules, leaves persistence/defense unchecked

4. **Configure options:**
   - Toggle **Ping on Send** to mention `@everyone` or `@here` in Discord embeds
   - Customize the **Fake Error** title and message if that module is enabled

5. **Choose output format:**
   - `.exe` — compiled standalone executable (requires PyInstaller, supports custom icon)
   - `.py` — raw Python script (no compilation needed)

6. **Pick an icon** (optional, `.exe` only) — `.ico`, `.png`, or `.jpg`

7. **Set filename** and click ** BUILD**

8. **Retrieve your payload** from the `output/` directory.

---

## Detailed Module Breakdown

### Passwords
Extracts saved browser passwords from all 15 Chromium browsers. Uses `win32crypt` to decrypt the master key from `Local State`, then AES-GCM decrypts each password blob from the `Login Data` SQLite database. Outputs one line per credential: `URL | Username | Password`.

### Cookies
Leverages `browser_cookie3` to dump every cookie from every installed browser into a tab-separated file (`domain \t name \t value`). No browser database locking issues — `browser_cookie3` handles that internally.

### Credit Cards
Reads the `credit_cards` table from each browser's `Web Data` SQLite file. Card numbers come encrypted; the output includes the encrypted blob prefix for reference. Expiration dates and cardholder names are captured in plaintext.

### Discord Tokens
Walks through all Discord client variants (stable, Canary, PTB) in both `LocalAppData` and `AppData\Roaming`. Scans `.ldb` and `.log` files with a regex pattern matching Discord's token format (`[A-Za-z0-9-_]{24}\.[A-Za-z0-9-_]{6}\.[A-Za-z0-9-_]{27}`). First 10 tokens are sent as an immediate text message; the full deduplicated list goes out as a file.

### WiFi Passwords
Runs `netsh wlan show profiles` to enumerate saved wireless networks, then `netsh wlan show profile <name> key=clear` for each to extract the pre-shared key. Outputs `SSID: Password` pairs. Open networks show `(open)`. First 15 entries are sent as a text preview.

### Authenticator
Multi-vector 2FA/TOTP harvesting:
- **Google Authenticator** — reads registry keys under `SOFTWARE\Google\Google Authenticator`
- **WinAuth** — parses XML files for `<secret>` tags and `Secret=` attributes, plus standalone Base32 strings
- **Authy Desktop** — copies the full Authy data directory
- **Browser Extensions** — scans `Local Extension Settings` for TOTP-like Base32 strings (16+ chars, A-Z2-7)
- **Microsoft Authenticator** — copies the app package data from `LocalAppData\Packages`
- **Windows Credential Vault** — enumerates credentials with `2fa`, `totp`, `authenticator`, `authy`, `otp`, or `token` in the target name

### Wallets
Copies wallet data directories for Exodus, Atomic, Electrum, Coinomi, and Guarda from their default install paths. Exodus `exodus.wallet` file, Atomic and Guarda `leveldb` directories, Electrum `wallets` folder. Bundles everything into `wallets.zip`.

### Roblox Cookies
Dual approach: `browser_cookie3` for `.roblox.com` domain cookies, plus direct SQLite reads from all Chromium profiles with AES-GCM decryption. Deduplicates and writes to `roblox_cookies.txt`.

### Games
- **Minecraft** — reads `launcher_accounts.json` and `launcher_profiles.json` from `.minecraft`, extracts `accessToken` values. Also covers MultiMC and PrismLauncher account files.
- **Epic Games** — copies `GameUserSettings.ini` and `Engine.ini` from the Epic Games Launcher config directory, plus the full `Saved\Config` tree.

### Common Files
Recursively scans Desktop, Documents, and Downloads for filenames containing sensitive keywords (`password`, `wallet`, `seed`, `backup`, `2fa`, `api key`, etc.) or sensitive extensions (`.kdbx`, `.rdp`, `.ovpn`, `.key`, `.pem`, `.env`, `.log`, and more). Files under 10 MB are collected. Skips `.lnk` shortcuts. Bundled as `common_files.zip`.

### Keylogger
Background thread using `pynput.keyboard.Listener`. Captures all keystrokes for 60 seconds while other scrapers run. Character keys are recorded directly; special keys are wrapped in brackets (`[Key.enter]`). Output is saved to `keylog.txt`. The listener runs concurrently and is stopped during the send phase.

### Screenshot
Attempts `mss` first (faster, multi-monitor aware), falls back to `PIL.ImageGrab` if unavailable. Saved as `screenshot.png`.

### Webcam
Opens the default camera (index 0) via `cv2.VideoCapture`, captures a single frame, and saves it as `webcam.jpg`. Camera is released immediately after. Silent failure if no camera is present.

### Disable Defender
Two-pronged attack:
1. **Registry** — sets `DisableAntiSpyware`, `DisableRealtimeMonitoring`, `DisableBehaviorMonitoring`, `DisableOnAccessProtection`, and `DisableScanOnRealtimeEnable` under `HKLM\SOFTWARE\Policies\Microsoft\Windows Defender`
2. **PowerShell** — runs 11 `Set-MpPreference` commands disabling RTP, behavior monitoring, block-at-first-seen, IOAV, privacy mode, signature updates, archive scanning, intrusion prevention, script scanning, sample submission, and MAPS reporting

### Add Exclusion
Adds the payload executable path, its parent directory, and the user's Temp folder to Windows Defender's exclusion list via PowerShell `Add-MpPreference -ExclusionPath` and registry (`HKLM\SOFTWARE\Microsoft\Windows Defender\Exclusions\Paths`).

### Startup
Copies the payload to `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\WindowsUpdate.exe` and creates `HKCU` + `HKLM` Run registry entries pointing to that path.

### Anti-VM / Anti-Debug
Runs **before** any scraping. Checks for:
- Debugger present (`IsDebuggerPresent()`)
- VMware/VirtualBox registry keys
- VM-related processes (`vmtoolsd.exe`, `VBoxService.exe`, etc.)
- Small screen resolution (≤1024×768, common on sandbox VMs)

If **any** indicator is found, the payload calls `sys.exit(0)` silently — no webhook message, no error, nothing.

### Anti-Spam
Creates a named Windows mutex using a random 16-character alphanumeric string (generated at build time). If a second instance launches with the same mutex name, `GetLastError()` returns `ERROR_ALREADY_EXISTS` (183) and the payload exits immediately.

### Self-Destruct
Generates a batch file (`cleanup.bat`) in the Temp directory that loops `del /f` on the payload executable until deletion succeeds, then deletes itself. Launched via `subprocess.Popen` with `DETACHED_PROCESS` + `CREATE_NO_WINDOW` flags so it runs independently after the Python process exits.

### Fake Error
Uses `tkinter.messagebox.showerror()` to display a configurable error dialog. Title and message are customizable in the builder GUI. Runs after data collection but before exfiltration — keeps the victim distracted.

---

## Webhook Configuration

### Ping Options
- **Off** — no mention prefix on embeds
- **@here** — pings online users in the webhook channel
- **@everyone** — pings all users in the webhook channel

The ping prefix is applied to text messages and embed titles. File-only sends are unaffected.

### Exfiltration Flow
1. `debug_full.log` — complete debug trace sent first
2. Harvest summary embed — lists all collected files with sizes
3. Individual files — each result file sent with category label
4. `harvest_full.zip` — everything bundled as a zip archive
5. `INE_CRASH.txt` — desktop crash log sent if it exists (fatal error recovery)

If no data was collected, a failure embed is sent instead with the machine hostname, and the crash log is forwarded.

---

## Build Process

### `.exe` (PyInstaller)
1. Builder generates the payload `.py` file in `output/`
2. Syntax validation via `compile()` — catches errors before PyInstaller runs
3. PyInstaller invoked with: `--onefile --noconsole --uac-admin`
4. All `PAYLOAD_DEPS` are force-included via `--hidden-import`
5. `requests`, `urllib3`, `chardet`, `certifi`, `idna` are collected with `--collect-all`
6. Custom icon converted to `.ico` (256×256) if needed
7. Build temp directory cleaned after completion
8. `.py` source deleted from `output/`

Build time: 60–180 seconds depending on system specs.

### `.py` (Raw Script)
1. Builder generates the payload `.py` file in `output/`
2. Syntax validated, no compilation
3. Ready to run with `python payload.py`

The `.py` output is not self-contained — the target machine needs Python + dependencies installed.

---

## File Structure

```
ine-builder/
├── builder.py              # Main builder GUI
├── install_deps.bat        # One-click dependency installer
├── README.md               # This documentation
└── output/                 # Generated payloads
    ├── payload.exe         # Compiled executable
    ├── _build_temp/        # PyInstaller workdir (auto-cleaned)
    └── _icon_temp.ico      # Converted icon (auto-cleaned)
```

### On Target Machine (Payload Runtime)
```
%TEMP%\INE_YYYYMMDD_HHMMSS\   # Working directory
├── debug.log                 # Full debug trace
├── system_info.txt
├── passwords.txt
├── cookies.txt
├── ... (all scraped files)
└── harvest_full.zip          # Complete bundle

Desktop\INE_CRASH.txt         # Fatal error log (if payload crashes)

%TEMP%\cleanup.bat            # Self-destruct script (if enabled)
```

### Payload Artifacts (Persistence)
```
Startup\WindowsUpdate.exe     # Payload copy
HKCU\...\Run\WindowsUpdate    # Registry persistence
HKLM\...\Run\WindowsUpdate    # Registry persistence (admin)
```

---

## Troubleshooting

### "PyInstaller not found"
Install PyInstaller:
```bash
pip install pyinstaller
```

### "SyntaxError at line X"
The generated `.py` has a bug. The `.py` file is kept in `output/` for debugging. Check the error line and report it. Most common cause: special characters in the Fake Error message breaking string escaping.

### "WEBHOOK TEST FAILED" in payload
- Verify the webhook URL is still valid
- Check that the target machine has internet access
- Discord rate limits: 5 requests per 2 seconds per webhook. The payload sends files sequentially to avoid this.

### "No data collected"
- Target may not have any of the selected browsers installed
- Browser databases may be locked (browsers were running — the payload taskkills them first)
- Admin privileges may not have been obtained (UAC elevation failed)

### Anti-VM false positive
If the payload exits immediately on a real machine, it may be triggering on:
- A debugger or system monitoring tool
- A small screen resolution
- A process name matching the VM detection list

Disable Anti-VM/Debug in the builder and rebuild.

---

## Changelog

### v7.4 — Current
- **+7 niche browsers** — Kometa, Orbitum, CentBrowser, 7Star, Sputnik, Epic Privacy, Uran, Yandex, Iridium (15 total)
- **WiFi Passwords** — SSID + PSK extraction via netsh
- **Clipboard Capture** — current clipboard text via PowerShell
- **Common Files** — keyword + extension sweep of Desktop/Documents/Downloads
- **Games** — Minecraft (vanilla + MultiMC + PrismLauncher) + Epic Games
- **Anti-VM/Debug** — VM detection exits silently before any scraping
- **Self-Destruct** — batch file loop deletes payload after exfiltration
- **Anti-Spam** — mutex-based single-instance enforcement
- **Ping @everyone/@here** — configurable mention on Discord embeds
- **Desktop crash log** — `INE_CRASH.txt` for fatal error recovery
- **Enhanced Authenticator** — added WinAuth XML parsing, Base32 TOTP extraction, MS Authenticator app data
- **Expanded Fake Error** — customizable title + message from builder GUI

### v7.3
- 8 Chromium browsers, wallet scraping, Roblox cookies, Telegram sessions
- Passkeys/WebAuthn + Windows Vault
- Keylogger, webcam, screenshot
- Disable Defender, Add Exclusion, Startup persistence

---

## Credits

**INE Project — by NODE**  
Builder: v7.4  
Contact: [Discord](https://discord.gg/Kr4SjcPfTE)

---
