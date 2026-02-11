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

#saves dictionary to CSV
def save_dict_to_csv(dict, filename="urls.csv"): 
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Item", "Name", "Price", "URL"])
        for item, product in dict.items():
            writer.writerow([product.id, product.name, product.price, product.url])

#check to see if product already inside of CSV, if not gets added USING URL
def check_item_in_csv(product, filename="urls.csv"): 
        with open(filename, mode='r', newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            key_to_check = product.id

            found = False
            for row in reader:
                if row.get('Item') == key_to_check:
                    found = True
                    break
            if found:
                 print(f"{product.name} is Already Being Tracked.") #Testing Purposes
                 return True
            else:
                 return False

#Add Product to CSV 
def add_to_csv(url, item='', filename="urls.csv"):
    item = get_next_item_number()
    with open(filename, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([item, url, get_name_from_url(url), get_price_from_url(url)])
        
#Get the next item number based on how many items already in CSV 
def get_next_item_number(filename="urls.csv"): 
    max_num = 1
    num_set = set()
    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                item = (row.get("Item") or "").strip()
                num_set.add(item)
            while max_num in num_set:
                max_num += 1
    except FileNotFoundError:
        pass
    return max_num

#Using the URL prints all the information about the product that is stored inside the csv 
def print_product_info(url, filename="urls.csv"):
     with open(filename, mode='r', newline='', encoding="utf-8") as f:
         reader = csv.DictReader(f)
         for row in reader:
             if row.get("url") == url:
                item_num = row.get("item")
                parts = item_num.split()
                print(f"Item: {row.get("item")}; Name: {row.get("name")}; Price: {row.get("price")}")

#Print the item #, name, and price of all the products inside the csv
def print_all_in_csv(filename="urls.csv"):
    with open(filename, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"Item {row["item"]}; Name: {row["name"]}; Price: {row["price"]}")

#Adds values from a column in the csv into a set
def import_into_set(set,row_to_check,filename="urls.csv"):
    with open(filename, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            item = row.get(row_to_check)
            set.add(item)

#Gets the url of product using item number that it is associated with in the csv 
def get_url_from_item_num(item_num, filename="urls.csv"):
    with open(filename, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("item") == item_num:
                url = row.get("url")
                return url

#Print the item number + item name  
def print_item_name(filename="urls.csv"):
    with open(filename, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"Item {row["item"]}; Name: {row["name"]}")

#Delete a row based on the item #
def delete_row(item,filename="urls.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

