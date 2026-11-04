from pypdf import PdfWriter

writer = PdfWriter()
writer.add_blank_page(width=200, height=200)

# اضافه کردن جاوااسکریپت مخفی به PDF
writer.add_js("app.alert('XSS via PDF!')")
# اضافه کردن یه لینک مخفی
writer.add_uri(0, "http://evil.com/phishing", (0, 0, 100, 100))

with open("mock_document.pdf", "wb") as f:
    writer.write(f)

print("[+] mock_document.pdf created with hidden JS and URI.")
