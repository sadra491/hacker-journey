import requests

# لیست مسیرهای رایج API که هکرها تست می‌کنن
COMMON_ENDPOINTS = [
    "/api/v1/users",
    "/api/v1/admin/users",
    "/api/v1/config",
    "/api/v1/login",
    "/api/v1/backup"
]

def fuzz_api(target_url):
    print(f"[*] Starting API Fuzzing on {target_url}")
    
    for endpoint in COMMON_ENDPOINTS:
        url = f"{target_url}{endpoint}"
        try:
            r = requests.get(url, timeout=2)
            
            # اگه 200 گرفتیم یعنی مسیر بازه
            if r.status_code == 200:
                print(f"[+] Found (200 OK): {endpoint}")
                # اگه دیتای حساسی برگشت، نشونش بده
                if "SECRET" in r.text:
                    print(f"    [!] LEAKED DATA: {r.text}")
            
            # اگه 403 گرفتیم یعنی مسیر وجود داره ولی محافظت شده
            elif r.status_code == 403:
                print(f"[!] Exists but Forbidden (403): {endpoint}")
                
        except Exception as e:
            pass

if __name__ == "__main__":
    target = "http://127.0.0.1:8000"
    fuzz_api(target)
