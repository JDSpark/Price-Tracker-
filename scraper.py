import requests
import csv
import os
from urllib.parse import urlparse
from pathlib import Path
from bs4 import BeautifulSoup

#takes inputed URL and outputs name of product
def get_name_from_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = path.strip("/").split("/", 1)[0]
    filename = filename.replace('-', ' ')
    return filename

#takes inputed url and outputs price (web scrapes the amazon page)
def get_price_from_url(url): 
    HEADERS = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept-Language' : 'en-US, en;q=0.5'
    }

    try:
        webpage = requests.get(url, headers=HEADERS, timeout=10)
        webpage.raise_for_status()

        soup = BeautifulSoup(webpage.content, "html.parser")

        price_element = soup.select_one('#corePrice_feature_div span.a-offscreen')

        if price_element:
            price = price_element.get_text().strip()
            return price
        else:
            print("Price element not found using current selectors")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def get_price_from_csv(url, filename="urls.csv"):
    with open(filename, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("URL") == url:
                return row.get("Price")