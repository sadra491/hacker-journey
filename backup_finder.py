import requests
from concurrent.futures import ThreadPoolExecutor

# لیست پسوندها و نام‌های رایج برای فایل‌های بکاپ
BACKUP_EXTENSIONS = [
    ".bak", ".old", ".backup", "~", ".save", ".swp", ".zip", ".tar.gz"
]

COMMON_FILES = [
    "index.php", "config.php", "db.php", ".env", "database.sql"
]

def check_backup_file(base_url, filename):
    url = f"{base_url}/{filename}"
    try:
        r = requests.get(url, timeout=2)
        
        # اگه فایل پیدا شد و 404 نبود
        if r.status_code == 200 and "Not Found" not in r.text:
            print(f"[+] Found Backup File: {url}")
            
            # اگه فایل پسوند متنی داشت (مثل .bak)، یه تیکه از محتواش رو چاپ کن
            if any(ext in filename for ext in [".bak", ".old", ".env", ".sql", "~"]):
                snippet = r.text[:100].replace('\n', ' ')
                print(f"    [!] Data Snippet: {snippet}...")
                
    except Exception:
        pass

def scan_backups(base_url):
    print(f"[*] Scanning for exposed backup files on: {base_url}")
    
    # ساخت لیست هدف‌ها (ترکیب نام فایل و پسوند)
    targets = []
    for file in COMMON_FILES:
        for ext in BACKUP_EXTENSIONS:
            targets.append(f"{file}{ext}")
    
    # اضافه کردن فایل‌های مستقیم
    targets.extend(["backup.zip", "site.tar.gz", "www.zip", ".env"])
    
    # اسکن همزمان با ۱۰ ترد
    with ThreadPoolExecutor(max_workers=10) as executor:
        for target in targets:
            executor.submit(check_backup_file, base_url, target)
            
    print("[*] Scan complete.")

if __name__ == "__main__":
    target = "http://127.0.0.1:8000"
    scan_backups(target)
