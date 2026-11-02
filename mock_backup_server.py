from http.server import BaseHTTPRequestHandler, HTTPServer

class BackupHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Welcome to Mock Site</h1></body></html>")
            
        elif self.path == '/config.php.bak':
            # شبیه‌سازی یه فایل بکاپ لو رفته
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"<?php $db_user = 'root'; $db_pass = 'super_secret_password'; ?>")
            
        elif self.path == '/backup.zip':
            self.send_response(200)
            self.send_header('Content-type', 'application/zip')
            self.end_headers()
            self.wfile.write(b"PK\x03\x04... (Fake ZIP Data)")
            
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

print("Mock Backup Server running on port 8000...")
HTTPServer(('127.0.0.1', 8000), BackupHandler).serve_forever()
