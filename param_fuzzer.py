import requests

# لیست پارامترهای رایج که معمولاً پنهان هستن
COMMON_PARAMS = [
    "debug", "test", "admin", "is_admin", "hidden", 
    "secret", "dev", "internal", "source", "show"
]

def fuzz_params(url):
    print(f"[*] Fuzzing hidden parameters on: {url}")
    
    # ۱. گرفتن پاسخ پایه (بدون پارامتر اضافه)
    try:
        base_response = requests.get(url, timeout=3)
        base_length = len(base_response.text)
        print(f"    [Baseline] Response length: {base_length} bytes\n")
    except Exception as e:
        print(f"[-] Error reaching target: {e}")
        return

    # ۲. شلیک تک‌تک پارامترها و مقایسه طول پاسخ
    for param in COMMON_PARAMS:
        # پارامتر رو با مقدار true تست می‌کنیم
        test_url = f"{url}?{param}=true"
        try:
            r = requests.get(test_url, timeout=3)
            new_length = len(r.text)
            
            # اگه طول پاسخ تغییر کرد، یعنی پارامتر تاثیر داره
            if new_length != base_length:
                print(f"[+] Hidden Parameter Found: ?{param}=true")
                print(f"    Length changed: {base_length} -> {new_length}")
                
        except Exception:
            pass
            
    print("\n[*] Parameter fuzzing complete.")

if __name__ == "__main__":
    target = "http://127.0.0.1:8000/"
    fuzz_params(target)
