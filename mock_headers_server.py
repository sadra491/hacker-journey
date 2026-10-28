from http.server import BaseHTTPRequestHandler, HTTPServer

class HeaderHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        # فقط چند هدر امنیتی رو تنظیم می‌کنیم (بقیه عمداً حذف شدن)
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('X-XSS-Protection', '1; mode=block')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<html><body>Mock site for header testing</body></html>")

print("Mock Header Server running on port 8000...")
HTTPServer(('127.0.0.1', 8000), HeaderHandler).serve_forever()
