import socket
import requests
import sys
from concurrent.futures import ThreadPoolExecutor

# پورت‌هایی که معمولاً مهمن
COMMON_PORTS = [21, 22, 80, 443, 8080]

def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((ip, port))
        s.close()
        return port if result == 0 else None
    except:
        return None

def get_headers(url):
    try:
        # verify=False برای اینکه اگه گواهی SSL مشکل داشت، برنامه کرش نکنه
        r = requests.get(url, timeout=3, verify=False)
        return r.headers
    except:
        return None

def main(domain):
    print(f"[*] Starting Automated Recon on: {domain}")
    
    # ۱. پیدا کردن آی‌پی
    try:
        ip = socket.gethostbyname(domain)
        print(f"[+] IP Address: {ip}")
    except:
        print("[-] Could not resolve domain.")
        return

    # ۲. اسکن پورت‌ها به صورت همزمان
    print("[*] Scanning common ports...")
    open_ports = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(lambda port: scan_port(ip, port), COMMON_PORTS)
        for port in results:
            if port:
                print(f"    [+] Port {port} is OPEN")
                open_ports.append(port)

    # ۳. اگه پورت وب باز بود، هدرها رو دربیار
    if 80 in open_ports or 443 in open_ports:
        print("[*] Extracting Web Server Information...")
        protocol = "https" if 443 in open_ports else "http"
        url = f"{protocol}://{domain}"
        headers = get_headers(url)
        
        if headers:
            print(f"    [+] Server: {headers.get('Server', 'Unknown')}")
            print(f"    [+] Tech Stack: {headers.get('X-Powered-By', 'Unknown')}")
            print(f"    [+] Content-Type: {headers.get('Content-Type', 'Unknown')}")
        else:
            print("    [-] Could not fetch headers.")
    else:
        print("[-] No common web ports (80/443) are open.")

if __name__ == "__main__":
    # اگه اسم دامنه رو موقع اجرا بدی، همون رو تست می‌کنه، وگرنه گوگل رو
    target = "google.com"
    if len(sys.argv) > 1:
        target = sys.argv[1]
        
    main(target)

