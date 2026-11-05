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
    </ul>
    """

@app.route("/xss")
def xss():
    # اینجا عمداً ورودی کاربر رو بدون پاکسازی (Sanitize) برمی‌گردونیم تا XSS رخ بده
    q = request.args.get("q", "")
    return f"<html><body>Your search: {q}</body></html>"

@app.route("/sqli")
def sqli():
    # شبیه‌سازی خطای دیتابیس در صورت تزریق کوتیشن
    id_val = request.args.get("id", "")
    if "'" in id_val or "\"" in id_val:
        return "<html><body>Error: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version.</body></html>"
    return f"<html><body>User ID: {id_val}</body></html>"

@app.route("/lfi")
def lfi():
    # شبیه‌سازی خواندن فایل در صورت استفاده از Path Traversal
    file_val = request.args.get("file", "")
    if "../" in file_val or "/etc/passwd" in file_val:
        return "<html><body>root:x:0:0:root:/root:/bin/bash<br>daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin</body></html>"
    return f"<html><body>File content: {file_val}</body></html>"

if __name__ == "__main__":
    print("[*] Vulnerable Test Server running on http://127.0.0.1:8002")
    app.run(host="127.0.0.1", port=8002, debug=False)
