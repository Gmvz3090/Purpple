import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def web_crawl(start_url: str, max_pages=50) -> list:
    """
    A simplified BFS-based web crawler using requests & Beautiful Soup.
    - start_url: The base URL to crawl (e.g., 'http://example.com')
    - max_pages: The maximum number of pages to visit
    :return: A list of discovered URLs (internal links)
    """
    to_visit = [start_url]
    visited = set()
    results = []

    # Determine the domain from the start_url
    start_domain = urlparse(start_url).netloc

    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop(0)

        # Skip if already visited
        if current_url in visited:
            continue

        visited.add(current_url)

        try:
            resp = requests.get(current_url, timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                # Extract all <a href="..."> links
                for link in soup.find_all("a", href=True):
                    absolute_url = urljoin(current_url, link['href'])

                    # Check if it's internal
                    if urlparse(absolute_url).netloc == start_domain:
                        if absolute_url not in visited and absolute_url not in to_visit:
                            to_visit.append(absolute_url)
                results.append(current_url)
        except Exception as e:
            # Just skip on error (e.g., timeouts, connection errors)
            pass

    return results
