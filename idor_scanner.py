import requests
import json

def scan_idor(url, engine):
    """
    ساده ترین نوع تست IDOR:
    عددهای داخل URL رو پیدا میکنه، تغییرشون میده و ببینید جواب 200 میده یا نه.
    """
    import re
    
    # پیدا کردن اعداد توی URL
    numbers = re.findall(r'\d+', url)
    if not numbers:
        print("[-] No numeric ID found in URL to test IDOR.")
        return
    
    target_id = numbers[0]
    print(f"[*] Testing IDOR on ID: {target_id}")
    
    # ساخت چند ID تستی
    test_ids = [str(int(target_id) + 1), str(int(target_id) - 1), "1", "999999"]
    
    # گرفتن درخواست اصلی برای مقایسه
    try:
        original_res = engine.request("GET", url)
        original_length = len(original_res.text)
    except Exception as e:
        print(f"[!] Failed to get original response: {e}")
        return

    for new_id in test_ids:
        if new_id == target_id:
            continue
            
        # جایگزینی ID توی URL
        new_url = url.replace(f"/{target_id}", f"/{new_id}").replace(f"={target_id}", f"={new_id}")
        
        try:
            print(f"[*] Trying ID: {new_id} -> {new_url}")
            res = engine.request("GET", new_url)
            
            if res.status_code == 200:
                # اگر طول پاسخ خیلی متفاوت بود، یعنی احتمالا دیتای یه کاربر دیگه رو داده
                new_length = len(res.text)
                
                # بررسی اینکه آیا JSON برگردونده یا نه
                is_json = 'application/json' in res.headers.get('Content-Type', '')
                
                if new_length > 100 and new_length != original_length:
                     print(f"[+] POTENTIAL IDOR FOUND! Status: 200, ID: {new_id}, Length change: {original_length} -> {new_length}")
                     if is_json:
                         print(f"    Snippet: {res.text[:100]}...")
                     # برای اینکه لاگ شلوغ نشه فقط اولین مورد رو گزارش میدیم
                     return
            else:
                 print(f"[-] ID {new_id} returned {res.status_code}")
                 
        except Exception as e:
            print(f"[!] Error testing ID {new_id}: {e}")
            
    print("[-] IDOR scan complete. No obvious vulnerabilities found.")
