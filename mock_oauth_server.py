from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/oauth/authorize':
            query = parse_qs(parsed_path.query)
            redirect_uri = query.get('redirect_uri', [''])[0]
            
            # باگ: چک کردن سطحی با استفاده از کلمه کلیدی
            # در واقعیت باید چک بشه که دامنه دقیقا همون باشه
            if "localhost:8000" in redirect_uri:
                self.send_response(302) # ریدایرکت
                self.send_header('Location', f"{redirect_uri}?code=SECRET_AUTH_CODE_123")
                self.end_headers()
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid redirect_uri")
        else:
            self.send_response(404)
            self.end_headers()

print("Mock OAuth Server running on port 8000...")
HTTPServer(('127.0.0.1', 8000), OAuthHandler).serve_forever()
