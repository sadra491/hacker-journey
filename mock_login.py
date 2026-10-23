from http.server import BaseHTTPRequestHandler, HTTPServer

class LoginHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length'))
        post_data = self.rfile.read(length).decode('utf-8')
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # رمز درست برای تست: secret123
        if "username=admin&password=secret123" in post_data:
            self.wfile.write(b"<html><body>Welcome Admin! Login Successful.</body></html>")
        else:
            self.wfile.write(b"<html><body>Login failed! Invalid credentials.</body></html>")

print("Server running on port 8000...")
HTTPServer(('127.0.0.1', 8000), LoginHandler).serve_forever()
