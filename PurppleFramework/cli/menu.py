import questionary
from urllib.parse import urlparse, parse_qs
from PurppleFramework.config import Config
from PurppleFramework.modules.Red.OSINT.osint_manager import run_all_osint
from PurppleFramework.modules.Red.Scanning.scanning_manager import run_all_scanning
from PurppleFramework.modules.Red.Sniffer.sniffer import run_sniffer
from PurppleFramework.modules.Red.ExploitSearch.exploit_manager import run_selected_exploits
from PurppleFramework.modules.Red.WebVuln.webvuln_manager import run_selected_scans

def run_cli():
    

    # 2) Choose mode (Red / Blue)
    mode_choice = questionary.select(
        "Select your mode:",
        choices=[
            "🔴 Red Team (Offensive)",
            "🔵 Blue Team (Defensive)"
        ]
    ).ask()

    # 3) Multi-select modules
    selected_modules = questionary.checkbox(
        "Select modules to enable:",
        choices=[
            "OSINT & Reconnaissance",
            "Scanning & Enumeration",
            "Web Vulnerability Scan",
            "Exploit Search",
            "Network Sniffer/Summarizer",
            "Cloud Security",
            "Reporting & Automation"
        ]
    ).ask()

    print("\n===== User Selections =====")
    print(f"Mode chosen: {mode_choice}")

    if not selected_modules:
        print("No modules were selected.")
        return
    else:
        print("Modules selected:")
        for module in selected_modules:
            print(f" - {module}")

    # Enforce prerequisites for Exploit Search and Web Vulnerability Scan
    if "Exploit Search" in selected_modules or "Web Vulnerability Scan" in selected_modules:
        if "OSINT & Reconnaissance" not in selected_modules:
            print("\n[!] You must also select 'OSINT & Reconnaissance' to use 'Exploit Search' or 'Web Vulnerability Scan'.")
            selected_modules = [m for m in selected_modules if m not in {"Exploit Search", "Web Vulnerability Scan"}]
            print("\n[!] Removing Exploit Search / Web Vulnerability Scan from your final selection.\n")
            print("Updated Modules selected:")
            for module in selected_modules:
                print(f" - {module}")

    # Run selected modules
    if mode_choice.startswith("🔴 Red Team"):
        if "OSINT & Reconnaissance" in selected_modules:
            domain = questionary.text("Enter target domain for OSINT:").ask()
            run_all_osint(
                domain=domain,
                vt_api_key=Config.vt_api_key,
                st_api_key=Config.st_api_key,
                shodan_api_key=Config.shodan_api_key,
                censys_id=Config.censys_id,
                censys_secret=Config.censys_secret
            )
        
        if "Scanning & Enumeration" in selected_modules:
            scan_target = questionary.text("Enter IP or domain for scanning:").ask()
            run_all_scanning(scan_target)

        if "Network Sniffer/Summarizer" in selected_modules:
            iface = questionary.text("Enter network interface (e.g., Wi-Fi, eth0, wlan0):").ask()
            run_sniffer(iface)
        
        if "Exploit Search" in selected_modules:
            target = questionary.text("Enter the target URL or IP for exploit search:").ask()
            run_selected_exploits(target)
        
        if "Web Vulnerability Scan" in selected_modules:
            run_selected_scans()

if __name__ == "__main__":
    run_cli()
