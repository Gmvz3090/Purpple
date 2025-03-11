import requests

def alienvault_domain_info(domain: str, otx_api_key: str) -> dict:
    """
    Query AlienVault OTX to retrieve reputation info for a specific domain.

    :param domain: The domain to query (e.g., 'example.com')
    :param otx_api_key: Your free OTX API key from your AlienVault dashboard
    :return: JSON data containing info about pulses, reputation, and malware indicators
    """
    headers = {
        "X-OTX-API-KEY": otx_api_key,
    }
    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/general"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}", "details": response.text}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    otx_key = input("Enter your AlienVault OTX API Key: ")
    domain = input("Domain to lookup: ")
    data = alienvault_domain_info(domain, otx_key)
    print(data)
