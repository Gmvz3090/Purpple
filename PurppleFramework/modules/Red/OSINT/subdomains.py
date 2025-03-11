import requests

def normalize_subdomain(subdomain):
    """
    Clean up subdomain string: strip whitespace, trailing periods,
    and convert to lowercase.
    """
    return subdomain.strip().rstrip('.').lower()


def query_crtsh(domain):
    """
    Query crt.sh for subdomains of the given domain.
    Returns a set of subdomains.
    """
    subdomains = set()
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                subdomain = normalize_subdomain(entry['name_value'])
                # Only add if it looks like a valid subdomain
                if subdomain and domain in subdomain:
                    subdomains.add(subdomain)
    except Exception:
        pass
    return subdomains


def query_virustotal(domain, vt_api_key):
    """
    Query VirusTotal for subdomains of the given domain.
    Returns a set of subdomains.
    """
    subdomains = set()
    url = f"https://www.virustotal.com/api/v3/domains/{domain}/subdomains"
    headers = {"x-apikey": vt_api_key}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for entry in data.get('data', []):
                subdomain = normalize_subdomain(entry['id'])
                if subdomain and domain in subdomain:
                    subdomains.add(subdomain)
    except Exception:
        pass
    return subdomains


def query_securitytrails(domain, st_api_key):
    """
    Query SecurityTrails for subdomains of the given domain.
    Returns a set of subdomains.
    """
    subdomains = set()
    url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains"
    headers = {"APIKEY": st_api_key}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for entry in data.get('subdomains', []):
                subdomain = normalize_subdomain(f"{entry}.{domain}")
                if subdomain and domain in subdomain:
                    subdomains.add(subdomain)
    except Exception:
        pass
    return subdomains


def gather_subdomains(domain, vt_api_key=None, st_api_key=None):
    """
    High-level function to gather subdomains from:
      - crt.sh
      - VirusTotal
      - SecurityTrails

    :param domain: The target domain (e.g., 'example.com')
    :param vt_api_key: VirusTotal API key (if available)
    :param st_api_key: SecurityTrails API key (if available)
    :return: A set of unique subdomains discovered
    """
    print(f"\n[*] Gathering subdomains for '{domain}' via OSINT sources...")

    all_subdomains = set()

    # 1. crt.sh - no API key required
    all_subdomains.update(query_crtsh(domain))

    # 2. VirusTotal (only if API key is provided)
    if vt_api_key:
        all_subdomains.update(query_virustotal(domain, vt_api_key))

    # 3. SecurityTrails (only if API key is provided)
    if st_api_key:
        all_subdomains.update(query_securitytrails(domain, st_api_key))

    # Normalize & remove potential duplicates
    final_subdomains = set()
    for item in all_subdomains:
        # If there are newline artifacts, split them
        if "\n" in item:
            for sub in item.split('\n'):
                final_subdomains.add(normalize_subdomain(sub))
        else:
            final_subdomains.add(normalize_subdomain(item))

    # Remove empty or top-level domain from set
    final_subdomains.discard(domain)
    final_subdomains.discard('')

    return final_subdomains


# Optional: Allow standalone execution for quick testing
if __name__ == "__main__":
    domain = input("[?] Enter target domain: ")
    vt_api_key = input("[?] VirusTotal API key (optional): ").strip() or None
    st_api_key = input("[?] SecurityTrails API key (optional): ").strip() or None

    results = gather_subdomains(domain, vt_api_key, st_api_key)
    print(f"\n[+] Found {len(results)} unique subdomains:")
    for sub in sorted(results):
        print(sub)
