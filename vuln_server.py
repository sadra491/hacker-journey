from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class V(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        q = parse_qs(urlparse(self.path).query)
        res = f"<html><body>Search result: {q.get('test',[''])[0]}</body></html>"
        self.wfile.write(res.encode())

HTTPServer(('127.0.0.1', 8000), V).serve_forever()

