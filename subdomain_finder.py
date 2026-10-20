import requests
from concurrent.futures import ThreadPoolExecutor

def check_subdomain(domain, sub):
    url = f"http://{sub}.{domain}"
    try:
        r = requests.get(url, timeout=2)
        if r.status_code == 200:
            print(f"[+] Found: {url}")
        elif r.status_code in [401, 403]:
            print(f"[!] Protected: {url} (Status: {r.status_code})")
    except:
        pass

if __name__ == "__main__":
    target = "google.com" # فعلاً روی گوگل تست می‌کنیم که قانونیه
    subs = ["www", "admin", "mail", "api", "dev", "test", "blog"]
    
    print(f"[*] Scanning subdomains for {target}...")
    with ThreadPoolExecutor(max_workers=10) as executor:
        for sub in subs:
            executor.submit(check_subdomain, target, sub)
    print("[*] Done.")
