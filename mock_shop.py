import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class ShopHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/checkout':
            length = int(self.headers.get('Content-Length'))
            post_data = json.loads(self.rfile.read(length).decode('utf-8'))
            
            item = post_data.get('item', 'unknown')
            quantity = post_data.get('quantity', 0)
            price = post_data.get('price', 0)
            
            # باگ منطقی: تعداد منفی چک نمی‌شه!
            total = quantity * price
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "success",
                "message": f"Purchased {quantity} of {item}.",
                "total_cost": total
            }
            if total < 0:
                response["message"] = "Whoa! You gained money?!"
                
            self.wfile.write(json.dumps(response).encode())

print("Shop Server running on port 8000...")
HTTPServer(('127.0.0.1', 8000), ShopHandler).serve_forever()
