# censys_search.py

import requests

def censys_search(api_id: str, api_secret: str, query: str) -> list:
    """
    Search Censys for a given query.
    This uses a direct API call (basic example).
    For more complex usage, consider the official python-censys library.

    :param api_id: Censys API ID
    :param api_secret: Censys API Secret
    :param query: The Censys search query
    :return: A list of found hosts or error messages
    """
    url = "https://search.censys.io/api/v2/hosts/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "q": query,
        "per_page": 5  # Limit results for demonstration
    }

    results = []
    try:
        response = requests.post(url, json=payload, headers=headers, auth=(api_id, api_secret), timeout=10)
        data = response.json()
        if "code" in data and data["code"] != 200:
            return [{"error": data.get("message", "Unknown error from Censys")}]

        # Example of parsing host data
        for host in data["result"]["hits"]:
            results.append({
                "ip": host.get("ip"),
                "services": host.get("services", [])
            })
    except Exception as e:
        results.append({"error": str(e)})

    return results
