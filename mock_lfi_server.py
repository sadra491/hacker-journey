from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class LFIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        query = parse_qs(urlparse(self.path).query)
        filename = query.get('file', [''])[0]
        
        # شبیه‌سازی باگ Path Traversal
        if "../" in filename or "/etc/passwd" in filename:
            # شبیه‌سازی محتوای فایل پسورد لینوکس
            html = "root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin"
        elif filename == "image.png":
            html = "[BINARY IMAGE DATA]"
        else:
            html = "File not found"
            
        self.wfile.write(html.encode())

print("Mock LFI Server running on port 8000...")
HTTPServer(('127.0.0.1', 8000), LFIHandler).serve_forever()
