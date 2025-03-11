import os
import sys
import questionary

# Dynamically add PurppleFramework to sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
purppleframework_dir = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
sys.path.insert(0, purppleframework_dir)

from modules.Red.WebVuln.xss import scan_xss
from modules.Red.WebVuln.sqli import scan_sqli
from modules.Red.WebVuln.lfi import scan_lfi
from modules.Red.WebVuln.cors import scan_cors
from modules.Red.WebVuln.apichecker import scan_urls

def run_selected_scans():
    """
    Allows the user to select which web vulnerability scans to run using questionary.
    """
    print("\n[+] Select Web Vulnerability Scans to Run")
    
    selected_scans = questionary.checkbox(
        "Select the vulnerability scans to perform:",
        choices=[
            "XSS Scan",
            "SQL Injection Scan",
            "Local File Inclusion Scan",
            "CORS Misconfiguration Scan",
            "API Security Scan"
        ]
    ).ask()
    
    if not selected_scans:
        print("[!] No scans selected. Exiting.")
        return
    
    print("\n[+] Running Selected Web Vulnerability Scans...")

    if "API Security Scan" in selected_scans:
        print("\n[*] --- API Security Scan ---")
        scan_urls()
    
    if "XSS Scan" in selected_scans:
        print("\n[*] --- XSS Scan ---")
        scan_xss()
    
    if "SQL Injection Scan" in selected_scans:
        print("\n[*] --- SQL Injection Scan ---")
        scan_sqli()
    
    if "Local File Inclusion Scan" in selected_scans:
        print("\n[*] --- Local File Inclusion Scan ---")
        scan_lfi()
    
    if "CORS Misconfiguration Scan" in selected_scans:
        print("\n[*] --- CORS Misconfiguration Scan ---")
        scan_cors()
    
    
    
    print("\n[*] Web Vulnerability Scanning Completed!\n")

if __name__ == "__main__":
    run_selected_scans()
