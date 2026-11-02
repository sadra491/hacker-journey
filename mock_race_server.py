from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import time

balance = 100 # موجودی اولیه

class RaceHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global balance
        if self.path == '/withdraw':
            length = int(self.headers.get('Content-Length'))
            data = json.loads(self.rfile.read(length).decode('utf-8'))
            amount = data.get('amount', 0)
            
            # باگ منطقی: اول چک می‌کنه، بعد تاخیر میندازه، بعد کم می‌کنه
            if balance >= amount:
                time.sleep(1) # این تاخیر باعث ایجاد باگ Race Condition میشه
                balance -= amount
                self.send_response(200)
                self.end_headers()
                self.wfile.write(f"Withdrew {amount}. Remaining: {balance}".encode())
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Insufficient funds")

# حتما از Threading استفاده می‌کنیم تا سرور بتونه چند درخواست رو همزمان پردازش کنه
print("Mock Race Condition Server running on port 8000...")
ThreadingHTTPServer(('127.0.0.1', 8000), RaceHandler).serve_forever()
