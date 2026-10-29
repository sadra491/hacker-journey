from http.server import BaseHTTPRequestHandler, HTTPServer

class TechHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        # شبیه‌سازی هدرهای PHP و nginx
        self.send_header('Server', 'nginx/1.18.0')
        self.send_header('X-Powered-By', 'PHP/8.1.2')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # شبیه‌سازی کدهای HTML وردپرس
        html = """
        <html>
        <head>
            <title>Mock Site</title>
            <meta name="generator" content="WordPress 6.2">
            <script src="/wp-content/themes/theme.js"></script>
        </head>
        <body>Hello World</body>
        </html>
        """
        self.wfile.write(html.encode())

print("Mock Tech Server running on port 8000...")
HTTPServer(('127.0.0.1', 8000), TechHandler).serve_forever()
