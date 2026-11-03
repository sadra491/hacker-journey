import requests

def check_takeover(url):
    print("[*] Checking " + url + " for Subdomain Takeover...")
    
    # امضاهای (Fingerprints) مربوط به سرویس‌های مختلف
    # اگه این پیام‌ها دیده بشن، یعنی دامنه معلق شده
    fingerprints = {
        "GitHub Pages": "There isn't a GitHub Pages site here",
        "AWS S3": "NoSuchBucket",
        "Heroku": "No such app",
        "Shopify": "Sorry, this shop is currently unavailable",
        "Fastly": "Fastly error: unknown domain"
    }
    
    try:
        r = requests.get(url, timeout=3)
        
        for service, fingerprint in fingerprints.items():
            if fingerprint in r.text:
                print("\n[+] VULNERABLE TO SUBDOMAIN TAKEOVER!")
                print("    Service: " + service)
                print("    URL: " + url)
                print("    Fingerprint Found: " + fingerprint)
                return True
                
        print("[-] Not vulnerable.")
        return False
    except Exception as e:
        print("[-] Error connecting: " + str(e))
        return False

if __name__ == "__main__":
    # شبیه‌سازی تست روی یک زیردامنه
    target_url = "http://127.0.0.1:8000/blog"
    check_takeover(target_url)
