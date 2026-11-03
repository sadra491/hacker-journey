from pypdf import PdfReader
import sys

def analyze_pdf(file_path):
    print(f"[*] Analyzing PDF: {file_path}")
    
    findings = 0
    
    # ۱. خواندن متادیتا و تعداد صفحات
    try:
        reader = PdfReader(file_path)
        print(f"    [+] Pages: {len(reader.pages)}")
        meta = reader.metadata
        if meta:
            print(f"    [+] Author: {meta.author}")
            print(f"    [+] Creator: {meta.creator}")
    except Exception as e:
        print(f"[-] Error: {e}")
        return

    # ۲. خواندن محتوای خام فایل برای پیدا کردن اشیاء مخفی
    with open(file_path, "rb") as f:
        raw_content = f.read()

    # ۳. جستجوی نشانه‌های خطرناک در فایل خام
    if b"/JS" in raw_content or b"/JavaScript" in raw_content:
        print("    [!] JavaScript detected inside PDF!")
        findings += 1
        
    if b"/URI" in raw_content:
        print("    [!] External Link (URI) detected inside PDF!")
        findings += 1
        
    if b"/OpenAction" in raw_content:
        print("    [!] Auto-Open Action detected (suspicious)!")
        findings += 1
        
    if b"/Launch" in raw_content:
        print("    [!] Launch Action detected (tries to run a program)!")
        findings += 1
        
    if b"/EmbeddedFile" in raw_content:
        print("    [!] Embedded File detected inside PDF!")
        findings += 1

    print("-" * 40)
    if findings > 0:
        print(f"[!] WARNING: {findings} suspicious items found in this PDF!")
    else:
        print("[+] PDF seems clean.")

if __name__ == "__main__":
    target_file = "mock_document.pdf"
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    analyze_pdf(target_file)
