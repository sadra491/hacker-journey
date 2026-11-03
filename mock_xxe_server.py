from http.server import BaseHTTPRequestHandler, HTTPServer

class XXEHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8', errors='ignore')
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        # شبیه‌سازی باگ XXE
        # اگه پیلود مخرب توش باشه، محتوای فایل رو برمی‌گردونه
        if 'SYSTEM "file:///etc/passwd"' in body:
            self.wfile.write(b"Processed XML. Result: root:x:0:0:root:/root:/bin/bash")
        else:
            self.wfile.write(b"Processed XML. Result: Normal Data")

print("Mock XXE Server running on port 8000...")
HTTPServer(('127.0.0.1', 8000), XXEHandler).serve_forever()
