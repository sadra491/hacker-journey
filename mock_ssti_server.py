from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class SSTIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        name = query.get('name', [''])[0]
        
        # شبیه‌سازی تمپلیت Jinja2 (باگ عمدی: اجرای ورودی کاربر)
        result = name
        if "{{" in name and "}}" in name:
            try:
                # این خط فقط برای شبیه‌سازی ضعف امنیتی است
                expr = name.replace("{{", "").replace("}}", "").strip()
                result = str(eval(expr))
            except:
                result = "Error"
                
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(("<html><body>Hello " + result + "</body></html>").encode())

print("Mock SSTI Server running on port 8000...")
HTTPServer(('127.0.0.1', 8000), SSTIHandler).serve_forever()
