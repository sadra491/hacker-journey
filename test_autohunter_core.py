import time
import requests
from autohunter_core import normalize_target, load_proxies, RequestEngine, BlockDetected

BASE = "http://127.0.0.1:8001"

def test_normalize():
    assert normalize_target("example.com") == "https://example.com"
    assert normalize_target("https://example.com/") == "https://example.com"
    assert normalize_target("http://test.com/path") == "http://test.com/path"
    print("[+] normalize_target OK")

def test_load_proxies():
    text = "http://1.2.3.4:8080\n5.6.7.8:3128\nsocks5://9.10.11.12:1080"
    proxies = load_proxies(text)
    assert len(proxies) == 3
    assert proxies[0] == "http://1.2.3.4:8080"
    print("[+] load_proxies OK")

def test_jitter():
    engine = RequestEngine(jitter_min=0.5, jitter_max=1.0)
    start = time.time()
    engine.request("GET", f"{BASE}/")
    engine.request("GET", f"{BASE}/")
    elapsed = time.time() - start
    assert elapsed >= 1.0
    print(f"[+] Jitter OK (elapsed: {elapsed:.2f}s)")

def test_block_detection_429():
    requests.get(f"{BASE}/reset-counts")
    engine = RequestEngine(jitter_min=0.1, jitter_max=0.2)
    blocked = False
    try:
        for _ in range(10):
            engine.request("GET", f"{BASE}/rate-limited")
    except BlockDetected:
        blocked = True
        print(f"[+] Block detection (429) OK")
    assert blocked

def test_block_detection_403():
    engine = RequestEngine(jitter_min=0.1, jitter_max=0.2)
    try:
        engine.request("GET", f"{BASE}/forbidden")
    except BlockDetected:
        print("[+] Block detection (403) OK")

def test_block_wait():
    requests.get(f"{BASE}/reset-counts")
    engine = RequestEngine(jitter_min=0.1, jitter_max=0.2, block_wait_seconds=2)
    start = time.time()
    try:
        for _ in range(10):
            engine.request("GET", f"{BASE}/rate-limited")
    except BlockDetected:
        pass
    elapsed = time.time() - start
    assert elapsed >= 2.0
    print(f"[+] Block wait OK (elapsed: {elapsed:.2f}s)")

if __name__ == "__main__":
    print("=== AutoHunter Core Tests ===")
    test_normalize()
    test_load_proxies()
    test_jitter()
    test_block_detection_429()
    test_block_detection_403()
    test_block_wait()
    print("\n=== All core tests passed ===")
