import requests

def check_cors(url):
    print(f"[*] Testing CORS configuration on: {url}")
    
    # دامنه‌ای که نقش هکر رو بازی می‌کنه
    malicious_origin = "https://evil.com"
    headers = {"Origin": malicious_origin}
    
    try:
        r = requests.get(url, headers=headers, timeout=3)
        
        # بررسی هدرهای پاسخ
        allow_origin = r.headers.get('Access-Control-Allow-Origin', '')
        allow_credentials = r.headers.get('Access-Control-Allow-Credentials', '')
        
        print(f"    [>] Sent Origin: {malicious_origin}")
        print(f"    [<] Allow-Origin: {allow_origin}")
        print(f"    [<] Allow-Credentials: {allow_credentials}")
        
        # تحلیل آسیب‌پذیری
        if allow_origin == malicious_origin and allow_credentials.lower() == 'true':
            print("\n[!] CRITICAL: CORS Misconfiguration Found!")
            print("    The server reflects any Origin and allows credentials.")
            print("    An attacker can steal user data from any website.")
        elif allow_origin == '*':
            print("\n[!] WARNING: Wildcard CORS detected.")
            print("    (Usually not exploitable if credentials are false).")
        else:
            print("\n[-] CORS seems properly configured.")
            
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    target_url = "http://127.0.0.1:8000/api/secret"
    check_cors(target_url)
