import requests
import csv
import os
from urllib.parse import urlparse
from pathlib import Path
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

# -------------------------------------------------------
# Site Detection
# -------------------------------------------------------

def get_website(url):
    parsed_url = urlparse(url)
    website_name = parsed_url.netloc
    if "amazon.com" in website_name:
        return "Amazon"
    elif "bestbuy.com" in website_name:
        return "Best Buy"
    elif "macys.com" in website_name:
        return "Macy's"
    # Add new sites here in the future
    else:
        return "Unknown"

# -------------------------------------------------------
# Price Router — add new sites here in the future
# -------------------------------------------------------

def get_price_from_url(url):
    site = get_website(url)
    if site == "Amazon":
        return get_price_amazon(url)
    elif site == "Best Buy":
        return get_price_bestbuy(url)
    elif site == "Macy's":
        return get_price_macys(url)
    else:
        print(f"Unsupported site: {site}")
        return None

# -------------------------------------------------------
# Name Router — add new sites here in the future
# -------------------------------------------------------

def get_name_from_url(url):
    site = get_website(url)
    if site == "Amazon":
        return get_name_amazon(url)
    elif site == "Best Buy":
        return get_name_bestbuy(url)
    elif site == "Macy's":
        return get_name_macys(url)
    else:
        return get_name_from_path(url)

# -------------------------------------------------------
# Shared fetch helper
# -------------------------------------------------------

def fetch_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Request error for {url}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error for {url}: {e}")
        return None

# -------------------------------------------------------
# Amazon
# -------------------------------------------------------

def get_price_amazon(url):
    soup = fetch_page(url)
    if not soup:
        return None
    price = soup.select_one('#corePrice_feature_div span.a-offscreen')
    if price:
        return price.get_text().strip()
    print("Amazon: price element not found")
    return None

def get_name_amazon(url):
    soup = fetch_page(url)
    if not soup:
        return get_name_from_path(url)
    title = soup.find("span", {"id": "productTitle"})
    if title:
        return title.get_text(strip=True)
    return get_name_from_path(url)

# -------------------------------------------------------
# Best Buy (placeholder — add selector when ready)
# -------------------------------------------------------

def get_price_bestbuy(url):
    # TODO: implement when Best Buy API key or selector is ready
    print("Best Buy scraping not yet implemented")
    return None

def get_name_bestbuy(url):
    # TODO: implement when Best Buy API key or selector is ready
    return get_name_from_path(url)

# -------------------------------------------------------
# Macy's (placeholder — add selector when ready)
# -------------------------------------------------------

def get_price_macys(url):
    # TODO: implement when Macy's selector is confirmed
    print("Macy's scraping not yet implemented")
    return None

def get_name_macys(url):
    # TODO: implement when Macy's selector is confirmed
    return get_name_from_path(url)

# -------------------------------------------------------
# Fallback name parser from URL path
# -------------------------------------------------------

def get_name_from_path(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = path.strip("/").split("/", 1)[0]
    filename = filename.replace('-', ' ')
    return filename

# -------------------------------------------------------
# CSV helper (used by product.py)
# -------------------------------------------------------

def get_price_from_csv(url, product_by_id):
    for key, product in product_by_id.items():
        if product.url == url:
            return product.current_price
    return None