from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <h1>Vulnerable Test Server</h1>
    <ul>
        <li><a href="/xss?q=hello">Test XSS</a></li>
        <li><a href="/sqli?id=1">Test SQLi</a></li>
        <li><a href="/lfi?file=test.txt">Test LFI</a></li>
        <li><a href="/auth_xss?q=hello">Test Auth XSS (Requires Header)</a></li>
    </ul>
    """

@app.route("/xss")
def xss():
    q = request.args.get("q", "")
    return f"<html><body>Your search: {q}</body></html>"

@app.route("/sqli")
def sqli():
    id_val = request.args.get("id", "")
    if "'" in id_val or "\"" in id_val:
        return "<html><body>Error: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version.</body></html>"
    return f"<html><body>User ID: {id_val}</body></html>"

@app.route("/lfi")
def lfi():
    file_val = request.args.get("file", "")
    if "../" in file_val or "/etc/passwd" in file_val:
        return "<html><body>root:x:0:0:root:/root:/bin/bash<br>daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin</body></html>"
    return f"<html><body>File content: {file_val}</body></html>"

@app.route("/auth_xss")
def auth_xss():
    # چک کردن هدر امنیتی
    auth_header = request.headers.get("X-Auth-Token")
    if auth_header != "secret123":
        return "<html><body><h1>403 Forbidden</h1><p>Missing or invalid X-Auth-Token</p></body></html>", 403
    
    # اگر هدر درست بود، اجازه میده و باگ XSS رو نشون میده
    q = request.args.get("q", "")
    return f"<html><body>Authenticated search: {q}</body></html>"

if __name__ == "__main__":
    print("[*] Vulnerable Test Server running on http://127.0.0.1:8002")
    app.run(host="127.0.0.1", port=8002, debug=False)
