import os
import requests
import re
from urllib.parse import urlparse

# -------------------------------
# CONFIGURATION
# -------------------------------
# Find the correct path for urls.txt and api.txt inside PurppleFramework/txts/
script_dir = os.path.dirname(os.path.abspath(__file__))  # Current script directory
purppleframework_dir = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))  # Navigate up to PurppleFramework
txts_dir = os.path.join(purppleframework_dir, "txts")  # Path to txts directory
os.makedirs(txts_dir, exist_ok=True)  # Ensure the 'txts' folder exists

URLS_FILE = os.path.join(txts_dir, "urls.txt")  # Input file
API_FILE = os.path.join(txts_dir, "api.txt")  # Output file

REQUEST_TIMEOUT = 5  # Seconds before requests time out

# -------------------------------
# 1. DISCOVER LINKS IN HTML
# -------------------------------
def find_all_links_in_html(base_url):
    """
    Fetches the HTML content of 'base_url' and finds every link
    that starts with http:// or https://.
    Returns a set of unique, cleaned links discovered.
    """
    found_links = set()
    try:
        response = requests.get(base_url, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            matches = re.findall(r'(https?://[^\s"\'<>]+)', response.text)
            # Remove trailing punctuation, whitespace, or invalid chars
            cleaned_links = {match.strip(" ,`'\"") for match in matches}
            found_links.update(cleaned_links)
    except requests.RequestException:
        pass

    return found_links

# -------------------------------
# MAIN FUNCTION: SCAN URL LIST
# -------------------------------
def scan_urls():
    """
    Reads each URL from 'PurppleFramework/txts/urls.txt', finds all http(s) links on the page,
    filters them so that each link must contain the same domain AND 'api',
    prints the unique resulting API links, and saves them to 'PurppleFramework/txts/api.txt'.
    Also appends found URLs to urls.txt without overwriting existing ones.
    """

    if not os.path.exists(URLS_FILE):
        print(f"[!] Error: '{URLS_FILE}' not found!")
        return

    unique_api_links = set()
    found_urls = set()

    with open(URLS_FILE, "r") as f:
        urls = [u.strip() for u in f if u.strip()]

    for base_url in urls:
        parsed_base = urlparse(base_url)
        base_domain = parsed_base.netloc.lower()

        links = find_all_links_in_html(base_url)

        # Filter links that contain the base domain and 'api'
        for link in links:
            if base_domain in link.lower() and "api" in link.lower():
                unique_api_links.add(link)
            found_urls.add(link)

    # Save new API links to api.txt
    with open(API_FILE, "w") as f:
        for link in sorted(unique_api_links):
            f.write(link + "\n")

    # Append new URLs to urls.txt without duplicates
    existing_urls = set(urls)
    new_urls = existing_urls - found_urls
    if new_urls:
        with open(URLS_FILE, "a") as f:
            for link in sorted(new_urls):
                f.write(link + "\n")

    # Print results
    print(f"\n✅ Found {len(unique_api_links)} API links. Saved to: {API_FILE}")
    for link in sorted(unique_api_links):
        print(link)

if __name__ == "__main__":
    scan_urls()
