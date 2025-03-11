import socket
import questionary
from .shodan_search import shodan_search
from .censys_search import censys_search
from .subdomains import gather_subdomains
from .alienv import run_alienvault_checks
from .whois_ import whois_lookup_windows

def run_all_osint(domain, vt_api_key=None, st_api_key=None, shodan_api_key=None, censys_id=None, censys_secret=None):
    """
    Allows the user to select which OSINT modules to run using questionary.
    """
    print(f"\n[+] Running OSINT on {domain}")
    
    selected_modules = questionary.checkbox(
        "Select OSINT modules to perform:",
        choices=[
            "IP Lookup",
            "WHOIS Lookup",
            "Subdomain Enumeration",
            "AlienVault Check",
            "Shodan Scan",
            "Censys Scan"
        ]
    ).ask()
    
    if not selected_modules:
        print("[!] No OSINT modules selected. Exiting.")
        return
    
    # 1) IP Lookup
    if "IP Lookup" in selected_modules:
        print("\n[*] --- IP ---")
        ip_address = socket.gethostbyname(domain)
        print(ip_address)
    
    # 2) WHOIS Lookup
    if "WHOIS Lookup" in selected_modules:
        print("\n[*] --- WHOIS ---")
        whois_data = whois_lookup_windows(domain)
        print(whois_data)
    
    # 3) Subdomains
    if "Subdomain Enumeration" in selected_modules:
        subdomain_results = gather_subdomains(domain, vt_api_key, st_api_key)
        print(f"\n[*] --- Subdomains ({len(subdomain_results)}) ---")
        for sub in sorted(subdomain_results):
            print(sub)
    
    # 4) AlienVault Check
    if "AlienVault Check" in selected_modules:
        print("\n[*] --- AlienVault ---")
        run_alienvault_checks(domain, "YOUR_ALIENVAULT_API_KEY")
    
    # 5) Shodan Scan
    if "Shodan Scan" in selected_modules and shodan_api_key:
        shodan_results = shodan_search(shodan_api_key, f"hostname:{domain}")
        print(f"\n[*] --- Shodan Results ({len(shodan_results)}) ---")
        for result in shodan_results:
            print(result)
    
    # 6) Censys Scan
    if "Censys Scan" in selected_modules and censys_id and censys_secret:
        censys_results = censys_search(censys_id, censys_secret, domain)
        print(f"\n[*] --- Censys Results ({len(censys_results)}) ---")
        for host in censys_results:
            print(host)
    
    print("\n[*] OSINT Scanning Completed!\n")

if __name__ == "__main__":
    domain = questionary.text("Enter the target domain:").ask()
    run_all_osint(domain)
