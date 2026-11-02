from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class ParamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # پارامتر مخفی: debug=true
        # اگه کاربر این پارامتر رو بفرسته، محتوای بیشتری نشون می‌ده (طول پاسخ عوض میشه)
        if query.get('debug', [''])[0] == 'true':
            html = "<html><body>Welcome! [DEBUG MODE ENABLED] Here is sensitive info: DB_PASS=1234.</body></html>"
        else:
            html = "<html><body>Welcome!</body></html>"
            
        self.wfile.write(html.encode())

print("Mock Param Server running on port 8000...")
HTTPServer(('127.0.0.1', 8000), ParamHandler).serve_forever()
