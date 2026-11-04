from http.server import BaseHTTPRequestHandler, HTTPServer

class VersionHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # API v2 (امن): نیاز به توکن داره
        if self.path == '/api/v2/users':
            if 'Authorization' in self.headers:
                self.wfile.write(b'{"status": "ok", "data": "SECURE_USER_DATA"}')
            else:
                self.send_response(401)
                self.wfile.write(b'{"error": "Unauthorized"}')
                
        # API v1 (قدیمی و آسیب‌پذیر): بدون احراز هویت!
        elif self.path == '/api/v1/users':
            self.wfile.write(b'{"status": "ok", "data": "LEAKED_USER_DATA_FROM_OLD_API"}')
            
        # API beta (داخلی)
        elif self.path == '/api/beta/users':
            self.wfile.write(b'{"status": "ok", "data": "BETA_INTERNAL_DATA"}')
            
        else:
            self.wfile.write(b'{"status": "not_found"}')

print("Mock API Versioning Server running on port 8000...")
HTTPServer(('127.0.0.1', 8000), VersionHandler).serve_forever()
