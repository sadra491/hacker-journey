import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import os

def load_payloads(filepath="payloads/xss.txt"):
    """
    پیلودها رو از فایل متنی می‌خونه. 
    اگر فایل پیدا نشد، از یه پیلود پیش‌فرض استفاده می‌کنه.
    """
    if not os.path.exists(filepath):
        print(f"[!] Payload file '{filepath}' not found. Using default payload.")
        return ["<script>alert(1)</script>"]
    
    with open(filepath, "r", encoding="utf-8") as f:
        # خواندن خطوط، حذف فاصله‌های اضافی و نادیده گرفتن خطوط خالی
        payloads = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return payloads

def scan_xss(url):
    # ۱. بارگذاری پیلودها از فایل
    payloads = load_payloads()
    if not payloads:
        print("[-] No payloads loaded.")
        return

    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    if not query_params:
        print("[-] هیچ پارامتری در این آدرس پیدا نشد.")
        return

    # ۲. حلقه روی پارامترهای URL
    for param in query_params:
        print(f"[*] Testing parameter: {param}")
        vulnerable = False
        
        # ۳. حلقه روی تمام پیلودهای داخل فایل
        for payload in payloads:
            # ساخت آدرس جدید با پیلود
            new_params = {k: v[0] for k, v in query_params.items()}
            new_params[param] = payload
            new_query = urlencode(new_params)
            
            new_parsed = parsed_url._replace(query=new_query)
            test_url = urlunparse(new_parsed)
            
            try:
                r = requests.get(test_url, timeout=5)
                
                # بررسی اینکه آیا پیلود توی جواب سرور برگشته یا نه
                if payload in r.text:
                    print(f"[+] XSS Found! (Vulnerable)")
                    print(f"    Payload: {payload}")
                    print(f"    URL: {test_url}")
                    vulnerable = True
                    break  # اگر باگ پیدا شد، دیگه بقیه پیلودها رو برای این پارامتر تست نکن
                    
            except Exception as e:
                print(f"[!] Error with payload {payload}: {e}")
        
        # اگر هیچ پیلودی کار نکرد
        if not vulnerable:
            print(f"[-] Not vulnerable.")

if __name__ == "__main__":
    print("[*] Starting XSS scan...")
    # این آدرس تستی هست، در ابزار اصلی آدرس واقعی جایگزین میشه
    target_url = "http://127.0.0.1:8000/search.php?test=query"
    scan_xss(target_url)
    print("[*] Scan complete.")
