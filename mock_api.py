from http.server import BaseHTTPRequestHandler, HTTPServer

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # شبیه‌سازی APIها
        if self.path == "/api/v1/admin/users":
            self.wfile.write(b'{"status": "success", "data": "SECRET_ADMIN_DATA"}')
        elif self.path == "/api/v1/config":
            self.send_response(403) # دسترسی ممنوع
            self.end_headers()
            self.wfile.write(b'{"error": "Forbidden"}')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "Not Found"}')

print("Mock API Server running on port 8000...")
HTTPServer(('127.0.0.1', 8000), APIHandler).serve_forever()
