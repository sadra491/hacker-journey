import requests

# لیست هدرهای امنیتی مهم که باید در پاسخ سرور وجود داشته باشن
SECURITY_HEADERS = [
    "X-Frame-Options",
    "X-XSS-Protection",
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Content-Type-Options"
]

def check_headers(url):
    print(f"[*] Analyzing security headers for: {url}")
    try:
        # ارسال درخواست GET به سایت
        r = requests.get(url, timeout=5, verify=False)
        headers = r.headers
        
        missing_headers = []
        for header in SECURITY_HEADERS:
            if header in headers:
                print(f"    [+] {header}: {headers[header]}")
            else:
                print(f"    [-] Missing: {header}")
                missing_headers.append(header)
        
        print("\n[*] Scan complete.")
        if missing_headers:
            print(f"[!] WARNING: {len(missing_headers)} security headers are missing!")
            print("    This site may be vulnerable to Clickjacking or XSS.")
        else:
            print("[+] All recommended security headers are present.")
            
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    target = "http://127.0.0.1:8000"
    check_headers(target)
