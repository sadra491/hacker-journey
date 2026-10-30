from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class SQLiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        query = parse_qs(urlparse(self.path).query)
        user_id = query.get('id', [''])[0]
        
        # شبیه‌سازی کوئری آسیب‌پذیر
        # اگه هکر ' OR 1=1 -- وارد کنه، برنامه بهش اطلاعات همه کاربران رو میده
        if "' OR 1=1 --" in user_id or "' OR '1'='1" in user_id:
            html = "<html><body>Welcome Admin! Data: [User1, User2, User3]</body></html>"
        elif user_id == "1":
            html = "<html><body>Welcome User 1</body></html>"
        else:
            html = "<html><body>User not found</body></html>"
            
        self.wfile.write(html.encode())

print("Mock SQLi Server running on port 8000...")
HTTPServer(('127.0.0.1', 8000), SQLiHandler).serve_forever()
