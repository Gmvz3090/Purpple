# PurppleFramework/modules/Red/Scanning/nmap_scanner.py

import subprocess

def nmap_scan(target: str) -> str:
    """
    Runs a basic Nmap scan on the specified target for the given port range.
    
    :param target: IP address or domain (e.g. '192.168.1.10' or 'example.com')
    :param ports: Port range (default: '1-1000')
    :return: Raw output from Nmap or error message
    """
    # Example flags: -sV (service version), -Pn (no ping), -p {ports}
    # Adjust or extend to suit your needs.
    command = ["nmap", "-sV", target]

    try:
        output = subprocess.check_output(command, text=True, timeout=180)
        return output
    except Exception as e:
        return f"[Error] Unable to run Nmap: {str(e)}"
