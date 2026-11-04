from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

request_count = {}

class RateLimitHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        request_count[client_ip] = request_count.get(client_ip, 0) + 1
        count = request_count[client_ip]
        
        if count > 5:
            self.send_response(429)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Too Many Requests")
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(("Request " + str(count) + " OK").encode())

print("Mock Rate Limit Server running on port 8000...")
print("Will block after 5 requests per IP.")
ThreadingHTTPServer(('127.0.0.1', 8000), RateLimitHandler).serve_forever()
