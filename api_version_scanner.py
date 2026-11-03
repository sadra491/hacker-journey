import requests

# لیست نسخه‌های رایج API که هکرها تست می‌کنن
API_VERSIONS = [
    "/api/v1/users",
    "/api/v2/users",
    "/api/v3/users",
    "/api/beta/users",
    "/api/internal/users",
    "/api/private/users",
    "/api/test/users",
    "/api/legacy/users"
]

def scan_api_versions(base_url):
    print("[*] Scanning API versions on: " + base_url)
    print("-" * 50)
    
    for endpoint in API_VERSIONS:
        url = base_url + endpoint
        try:
            r = requests.get(url, timeout=3)
            
            # شرط اصلاح شده: کد 200 باشه ولی جواب not_found نباشه
            if r.status_code == 200 and "Unauthorized" not in r.text and "not_found" not in r.text:
                print("[+] OPEN API FOUND (No Auth): " + endpoint)
                snippet = r.text[:80].replace('\n', ' ')
                print("    Data: " + snippet)
                print("    [!!!] This is vulnerable to Broken Access Control!")
            elif r.status_code == 200:
                print("[*] Protected API: " + endpoint + " (Status: 200, but needs token)")
        except Exception:
            pass
            
    print("-" * 50)
    print("[*] Scan complete.")

if __name__ == "__main__":
    target = "http://127.0.0.1:8000"
    scan_api_versions(target)
