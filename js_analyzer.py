import re
import sys

def analyze_js(file_path):
    print(f"[*] Analyzing JavaScript file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            js_code = f.read()
    except Exception as e:
        print(f"[-] Error reading file: {e}")
        return

    # ۱. پیدا کردن Endpointهای API
    print("\n[+] Extracted API Endpoints:")
    # این Regex دنبال رشته‌هایی می‌گرده که با /api/ شروع می‌شن
    endpoints = set(re.findall(r'["\'](/api/[^"\']+)["\']', js_code))
    for ep in endpoints:
        print(f"    -> {ep}")

    # ۲. پیدا کردن ایمیل‌ها
    print("\n[+] Extracted Emails:")
    emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', js_code))
    for email in emails:
        print(f"    -> {email}")

if __name__ == "__main__":
    # ابزار رو روی فایل جعلی اجرا می‌کنیم
    analyze_js("mock_app.js")
