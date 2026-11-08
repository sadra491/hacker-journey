import json

def fuzz_post_json(url, json_data, engine):
    print(f"[*] Fuzzing JSON POST to: {url}")
    
    payloads = [
        "<script>alert(1)</script>",
        "' OR 1=1 --",
        "../../../../etc/passwd",
        "{{7*7}}"
    ]
    
    try:
        original_res = engine.request("POST", url, json_data=json_data)
        original_len = len(original_res.text)
        print(f"[*] Baseline response length: {original_len}, Status: {original_res.status_code}")
    except Exception as e:
        print(f"[!] Failed to get baseline: {e}")
        return

    for key, value in json_data.items():
        if isinstance(value, str):
            for payload in payloads:
                test_data = json_data.copy()
                test_data[key] = payload
                
                print(f"[*] Testing key '{key}' with payload: {payload[:20]}...")
                try:
                    res = engine.request("POST", url, json_data=test_data)
                    
                    if res.status_code == 200 and len(res.text) != original_len:
                        print(f"[+] Potential issue found on key '{key}' with payload: {payload}")
                        print(f"    Status: {res.status_code}, Length: {len(res.text)}")
                        snippet = res.text[:100].replace('\n', ' ')
                        print(f"    Snippet: {snippet}")
                        return
                        
                except Exception:
                    pass
                    
    print("[-] POST JSON Fuzzing complete. No direct reflection found.")
