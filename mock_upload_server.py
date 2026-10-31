from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

class UploadHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        # شبیه‌سازی سطحی چک کردن پسوند
        # (در واقعیت باید محتوا هم چک بشه، اینجا عمداً باگ داره)
        if "filename=" in self.headers.get('Content-Disposition', ''):
            pass
        
        # ساده‌سازی: فرض کن هر فایلی رو قبول می‌کنیم
        self.wfile.write(b"File uploaded successfully!")

print("Mock Upload Server running on port 8000...")
HTTPServer(('127.0.0.1', 8000), UploadHandler).serve_forever()
