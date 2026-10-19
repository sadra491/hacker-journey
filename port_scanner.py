import socket
from concurrent.futures import ThreadPoolExecutor
import sys

def scan_port(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((target, port))
        if result == 0:
            print(f"[+] Port {port} is OPEN")
        s.close()
    except:
        pass

if __name__ == "__main__":
    target_ip = "127.0.0.1" # هدف فعلی
    if len(sys.argv) > 1:
        target_ip = sys.argv[1] # می‌تونی آی‌پی رو موقع اجرا هم بدی
    
    print(f"[*] Starting fast scan on {target_ip}...")
    print("-" * 40)
    
    # اسکن پورت‌های ۱ تا ۱۰۰۰ به صورت همزمان (با ۱۰۰ رشته موازی)
    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(1, 1001):
            executor.submit(scan_port, target_ip, port)
            
    print("-" * 40)
    print("[*] Scan complete.")
