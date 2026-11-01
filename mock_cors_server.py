from http.server import BaseHTTPRequestHandler, HTTPServer

class CorsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # گرفتن هدر Origin از درخواست
        origin = self.headers.get('Origin', '')
        
        self.send_response(200)
        # باگ: هر Originی رو قبول می‌کنه و Credentials رو هم اجازه می‌ده
        if origin:
            self.send_header('Access-Control-Allow-Origin', origin)
            self.send_header('Access-Control-Allow-Credentials', 'true')
            
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        if self.path == '/api/secret':
            self.wfile.write(b'{"data": "SECRET_USER_DATA"}')
        else:
            self.wfile.write(b'{"status": "ok"}')

print("Mock CORS Server running on port 8000...")
HTTPServer(('127.0.0.1', 8000), CorsHandler).serve_forever()
