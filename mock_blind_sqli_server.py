from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import time

class BlindSQLiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        user_id = query.get('id', [''])[0]
        
        # شبیه‌سازی کوئری دیتابیس
        # اگه پیلود SLEEP(3) توش بود، ۳ ثانیه تاخیر می‌ندازیم
        if "SLEEP(3)" in user_id or "sleep(3)" in user_id:
            time.sleep(3)
            
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # در Blind SQLi، پاسخ همیشه یکسان به نظر می‌رسه
        self.wfile.write(b"<html><body>Welcome User</body></html>")

print("Mock Blind SQLi Server running on port 8000...")
ThreadingHTTPServer(('127.0.0.1', 8000), BlindSQLiHandler).serve_forever()
