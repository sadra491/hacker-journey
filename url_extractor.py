import requests
import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import sys

def extract_parameterized_urls(target_url, output_file="hunt_targets.txt"):
    print(f"[*] Fetching {target_url} ...")
    try:
        r = requests.get(target_url, timeout=10, verify=False)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        found_urls = set()
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(target_url, href)
            
            # فقط لینک‌هایی که پارامتر (?) دارن رو نگه دار
            if '?' in full_url and '=' in full_url:
                # حذف هشتگ‌ها (Fragments)
                clean_url = full_url.split('#')[0]
                found_urls.add(clean_url)
                
        if found_urls:
            with open(output_file, 'w') as f:
                for u in found_urls:
                    f.write(u + '\n')
            print(f"[+] Found {len(found_urls)} parameterized URLs.")
            print(f"[+] Saved to {output_file}")
        else:
            print("[-] No parameterized URLs found on this page.")
            
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    if len(sys.argv) < 2:
        print("Usage: python3 url_extractor.py <target_url>")
        print("Example: python3 url_extractor.py https://basalam.com")
        sys.exit(1)
        
    target = sys.argv[1]
    extract_parameterized_urls(target)
