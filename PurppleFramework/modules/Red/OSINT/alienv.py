# osint_manager.py

from PurppleFramework.modules.Red.OSINT.alienvaults import alienvault_domain_info

def run_alienvault_checks(domain: str, otx_api_key: str) -> None:
    """
    Runs the AlienVault OTX check for the given domain, printing results.
    """
    if not otx_api_key:
        print("[-] No AlienVault OTX API key provided. Skipping AlienVault checks.")
        return

    print(f"\n[+] Checking AlienVault OTX for {domain} ...")
    data = alienvault_domain_info(domain, otx_api_key)
    
    if "error" in data:
        print(f"[!] Error from AlienVault OTX: {data['error']}")
        if "details" in data:
            print(f"    Details: {data['details']}")
    else:
        # Print out some key items from the OTX data
        pulses = data.get("pulse_info", {}).get("pulses", [])
        print(f"[*] Found {len(pulses)} pulses for {domain}")
        for pulse in pulses:
            print(f"   - Pulse Name: {pulse.get('name')}")
            print(f"     Created: {pulse.get('created')}")
            print(f"     Tags: {pulse.get('tags')}")
            print("-----")
