import requests
import os

# -------------------------------
# CONFIGURATION
# -------------------------------
# Find the correct path for urls.txt inside PurppleFramework/txts/
script_dir = os.path.dirname(os.path.abspath(__file__))  # Current script directory
purppleframework_dir = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))  # Navigate up to PurppleFramework
txts_dir = os.path.join(purppleframework_dir, "txts")  # Path to txts directory
os.makedirs(txts_dir, exist_ok=True)  # Ensure the 'txts' folder exists

URLS_FILE = os.path.join(txts_dir, "urls.txt")  # Input file

REQUEST_TIMEOUT = 5  # Seconds before requests time out

# -------------------------------
# CORS MISCONFIGURATION CHECKER
# -------------------------------
def check_cors(target):
    """
    Checks for CORS misconfigurations by sending an Origin header.
    """
    headers = {"Origin": "https://evil.com", "Referer": target}
    try:
        response = requests.get(target, headers=headers, timeout=REQUEST_TIMEOUT)
        cors_headers = response.headers
        
        if "Access-Control-Allow-Origin" in cors_headers:
            origin = cors_headers["Access-Control-Allow-Origin"]
            credentials = cors_headers.get("Access-Control-Allow-Credentials", "False").lower()
            
            if origin == "*" and credentials == "true":
                print(f"[!] Critical CORS Misconfiguration Found on {target}")
                return True
            elif origin == "*" or credentials == "true":
                print(f"[+] Potential CORS Issue: {target} allows {origin} with credentials={credentials}")
                return True
    except requests.exceptions.RequestException:
        print(f"[-] Could not connect to {target}")
    return False

# -------------------------------
# MAIN FUNCTION: SCAN URL LIST
# -------------------------------
def scan_cors():
    """
    Reads each URL from 'PurppleFramework/txts/urls.txt' and checks for CORS vulnerabilities.
    """
    if not os.path.exists(URLS_FILE):
        print(f"[!] Error: '{URLS_FILE}' not found!")
        return

    with open(URLS_FILE, "r") as f:
        urls = [u.strip() for u in f if u.strip()]
    
    print("[+] Scanning URLs for CORS misconfigurations...")
    found_misconfig = False
    
    for url in urls:
        if check_cors(url):
            found_misconfig = True
    
    if not found_misconfig:
        print("[-] No CORS misconfigurations found on any URLs.")

if __name__ == "__main__":
    scan_cors()
