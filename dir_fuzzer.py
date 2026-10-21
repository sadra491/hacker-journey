import requests
from concurrent.futures import ThreadPoolExecutor

def check_path(target, path):
    url = f"{target}/{path}"
    try:
        r = requests.get(url, timeout=2)
        if r.status_code == 200:
            print(f"[+] Found: {url}")
        elif r.status_code in [301, 302, 403]:
            print(f"[!] Interesting: {url} (Status: {r.status_code})")
    except:
        pass

if __name__ == "__main__":
    target = "http://127.0.0.1:8000"
    # کلماتی که قراره حدس زده بشن
    paths = ["admin", "login", "backup", "config", "robots.txt", "secret"]
    
    print(f"[*] Fuzzing directories on {target}...")
    with ThreadPoolExecutor(max_workers=10) as executor:
        for path in paths:
            executor.submit(check_path, target, path)
    print("[*] Done.")
