# shodan_search.py

try:
    import shodan  # pip install shodan
except ImportError:
    shodan = None

def shodan_search(api_key: str, query: str) -> list:
    """
    Search Shodan for a given query (e.g., 'apache port:80').

    :param api_key: Shodan API key
    :param query: The Shodan query
    :return: A list of IP addresses or info related to the query
    """
    if not shodan:
        raise ImportError("Shodan library is not installed. Please install via 'pip install shodan'.")

    results = []
    try:
        api = shodan.Shodan(api_key)
        scan_result = api.search(query)

        for match in scan_result['matches']:
            ip_str = match.get('ip_str')
            port = match.get('port')
            data = match.get('data')
            results.append({
                "ip": ip_str,
                "port": port,
                "data": data
            })
    except Exception as e:
        results.append({"error": str(e)})

    return results
