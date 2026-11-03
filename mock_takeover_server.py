from http.server import BaseHTTPRequestHandler, HTTPServer

class TakeoverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/blog':
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # این دقیقا همون پیام خطای گیت‌هاب پیجز هست
            self.wfile.write(b"<html><body>404 There isn't a GitHub Pages site here.</body></html>")
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<html><body>Welcome to the main site!</body></html>")

print("Mock Takeover Server running on port 8000...")
HTTPServer(('127.0.0.1', 8000), TakeoverHandler).serve_forever()
