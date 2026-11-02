from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class SSRFHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == '/fetch':
            query = parse_qs(parsed.query)
            target_url = query.get('url', [''])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            
            # شبیه‌سازی پاسخ موفقیت‌آمیز برای تست (تا ابزار ما تشخیص بده)
            if "127.0.0.1" in target_url or "localhost" in target_url or "169.254" in target_url:
                self.wfile.write(b"Fetched: Internal Server Response (Fake Data)")
            else:
                self.wfile.write(b"Fetched: External Data")
        else:
            self.send_response(404)
            self.end_headers()

print("Mock SSRF Server running on port 8000...")
HTTPServer(('127.0.0.1', 8000), SSRFHandler).serve_forever()
