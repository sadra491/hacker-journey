import requests
import time
import random

def test_with_jitter_and_block(url, num_requests=8, jitter_range=(1, 3)):
    print("[*] Testing jitter and block detection on: " + url)
    print("[*] Sending " + str(num_requests) + " requests with jitter " + str(jitter_range[0]) + "-" + str(jitter_range[1]) + "s")
    print("-" * 50)
    
    blocked = False
    success_count = 0
    
    for i in range(num_requests):
        delay = random.uniform(jitter_range[0], jitter_range[1])
        print("[*] Request " + str(i+1) + ": waiting " + str(round(delay, 2)) + "s...")
        time.sleep(delay)
        
        try:
            r = requests.get(url, timeout=5)
            
            if r.status_code == 429:
                print("    [!] BLOCKED (429 Too Many Requests) - stopping!")
                blocked = True
                break
            elif r.status_code == 403:
                print("    [!] BLOCKED (403 Forbidden) - stopping!")
                blocked = True
                break
            elif r.status_code == 200:
                print("    [+] OK: " + r.text[:50])
                success_count += 1
            else:
                print("    [?] Status: " + str(r.status_code))
        except Exception as e:
            print("    [-] Error: " + str(e))
    
    print("-" * 50)
    if blocked:
        print("[!] Result: Blocked after " + str(success_count) + " successful requests.")
        print("[*] Block Detection is working correctly.")
    else:
        print("[+] Result: " + str(success_count) + " successful requests, no block.")
    print("[*] Test complete.")

if __name__ == "__main__":
    target = "http://127.0.0.1:8000/test"
    test_with_jitter_and_block(target)
