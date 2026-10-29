import requests

def fingerprint_technology(url):
    print(f"[*] Analyzing technology stack for: {url}")
    try:
        r = requests.get(url, timeout=5)
        
        # ۱. بررسی هدرهای HTTP
        server = r.headers.get('Server', 'Unknown')
        powered_by = r.headers.get('X-Powered-By', 'Unknown')
        print(f"\n[+] Server Header: {server}")
        print(f"[+] Backend Technology: {powered_by}")
        
        # ۲. بررسی کدهای HTML برای پیدا کردن فریم‌ورک
        html = r.text.lower()
        print("\n[+] Analyzing HTML source...")
        
        if "wp-content" in html or "wordpress" in html:
            print("    -> Detected CMS: WordPress")
        if "react" in html or "_next" in html:
            print("    -> Detected Frontend: React / Next.js")
        if "laravel" in r.cookies:
            print("    -> Detected Backend: Laravel")
            
        print("\n[*] Fingerprinting complete.")
        
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    # روی سرور جعلی خودمون تست می‌کنیم
    target = "http://127.0.0.1:8000"
    fingerprint_technology(target)
