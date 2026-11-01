from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64

class JWTHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/protected':
            length = int(self.headers.get('Content-Length'))
            post_data = json.loads(self.rfile.read(length).decode('utf-8'))
            token = post_data.get('token', '')
            
            try:
                parts = token.split('.')
                if len(parts) < 2:
                    raise ValueError("Invalid token")
                
                # دیکد کردن هدر و پیلود
                header_b64 = parts[0] + '=' * (-len(parts[0]) % 4)
                header = json.loads(base64.urlsafe_b64decode(header_b64).decode('utf-8'))
                
                payload_b64 = parts[1] + '=' * (-len(parts[1]) % 4)
                payload = json.loads(base64.urlsafe_b64decode(payload_b64).decode('utf-8'))
                
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                
                # باگ: اگه الگوریتم none باشه، بدون چک کردن امضا قبولش می‌کنیم!
                if header.get('alg') == 'none':
                    if payload.get('role') == 'admin':
                        self.wfile.write(b"Welcome Admin! (Bypassed)")
                    else:
                        self.wfile.write(b"Welcome User!")
                else:
                    self.wfile.write(b"Signature verified.")
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(f"Error: {e}".encode())

print("Mock JWT Server running on port 8000...")
HTTPServer(('127.0.0.1', 8000), JWTHandler).serve_forever()
