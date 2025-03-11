import os
import requests
import socket
import questionary
from .nmap_scanner import nmap_scan
from .crawler import web_crawl
from .ssltls import get_certificate_info

# -------------------------------
# Fetch Subdomains via OSINT (crt.sh)
# -------------------------------
def get_subdomains(target: str):
    """
    Fetches subdomains using OSINT from crt.sh (Certificate Transparency logs).
    Returns a list of unique subdomains.
    """
    url = f"https://crt.sh/?q={target}&output=json"
    subdomains = set()

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            json_data = response.json()
            for entry in json_data:
                name_value = entry.get("name_value", "")
                for subdomain in name_value.split("\n"):
                    subdomain = subdomain.strip().lower()
                    if subdomain.endswith(target):  # Ensure it belongs to the target
                        subdomains.add(subdomain)
    except requests.RequestException:
        print("[!] Failed to fetch subdomains from crt.sh")

    return sorted(subdomains)

# -------------------------------
# Main Scanning Function
# -------------------------------
def run_all_scanning(target: str, max_crawl_pages=50):
    """
    Allows the user to select which scanning modules to run using questionary.
    """
    print(f"\n[+] Running Scanning on {target}")
    
    selected_scans = questionary.checkbox(
        "Select the scanning modules to perform:",
        choices=[
            "Nmap Scan",
            "Web Crawling",
            "TLS/SSL Information"
        ]
    ).ask()
    
    if not selected_scans:
        print("[!] No scanning modules selected. Exiting.")
        return
    
    # 1️⃣ Nmap Scan
    if "Nmap Scan" in selected_scans:
        ip_address = socket.gethostbyname(target)
        print("\n[*] --- Nmap Scan ---")
        print(nmap_scan(ip_address))
    

        #print("\n[*] --- Subdomain Enumeration (OSINT) ---")
    discovered_subdomains = get_subdomains(target)
    base_urls = {f"http://{sub}" for sub in discovered_subdomains} | {f"http://{target}"}

        #for sub in discovered_subdomains:
       #     print(f" - Found: {sub}")
    
    # 3️⃣ Web Crawling
    all_discovered_pages = set()
    if "Web Crawling" in selected_scans:
        print("\n[*] --- Web Crawler ---")
        for url_to_crawl in base_urls:
            #print(f"\nCrawling: {url_to_crawl}")
            discovered_pages = web_crawl(url_to_crawl, max_pages=max_crawl_pages)
            #print(f"Discovered {len(discovered_pages)} pages from {url_to_crawl}:")
            for page in discovered_pages:
                print(page)
            all_discovered_pages.update(discovered_pages)
    
    # 4️⃣ Save Discovered URLs to 'urls.txt'
    script_dir = os.path.dirname(os.path.abspath(__file__))  
    purppleframework_dir = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
    txts_dir = os.path.join(purppleframework_dir, "txts")
    os.makedirs(txts_dir, exist_ok=True)  
    output_file = os.path.join(txts_dir, "urls.txt")

    all_unique_urls = base_urls | all_discovered_pages
    with open(output_file, "w") as f:
        for url in sorted(all_unique_urls):
            f.write(url + "\n")

    print(f"\n✅ Saved {len(all_unique_urls)} unique URLs to {output_file}")
    
    # 5️⃣ TLS/SSL Information
    if "TLS/SSL Information" in selected_scans:
        print("\n[*] --- TLS/SSL ---")
        cert_info = get_certificate_info(target, 443)
        print("🔹 Subject CN:", cert_info.get("subject_common_name"))
        print("🔹 Issuer CN:", cert_info.get("issuer_common_name"))
        print("🔹 Valid From:", cert_info.get("valid_from"))
        print("🔹 Valid To:  ", cert_info.get("valid_to"))
        print("🔹 Cipher:    ", cert_info.get("cipher"))
        print("🔹 Protocol:  ", cert_info.get("protocol"))
    
    print("\n[✅] Scanning finished!\n")

if __name__ == "__main__":
    target = questionary.text("Enter the target domain:").ask()
    run_selected_scans(target)
