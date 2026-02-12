import requests
import csv
import os
from urllib.parse import urlparse
from pathlib import Path
from bs4 import BeautifulSoup
from product import Product
from scraper import get_name_from_url, get_price_from_url

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
                item_url = row.get("URL")
                if item_url == product.url:
                    found = True
                    break
            if found:
                 print(f"{product.name} is Already Being Tracked.")
                 return True
            else:
                 return False

#Add Product to CSV 
def add_to_csv(url, item='', filename="urls.csv"):
    item = get_next_item_number()
    with open(filename, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([item, get_name_from_url(url), get_price_from_url(url), url])
        
#Get the next item number based on how many items already in CSV 
def get_next_item_number(filename="urls.csv"): 
    max_num = 1
    num_set = set()
    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                item = (row.get("Item") or "").strip()
                num_set.add(int(item))
            while max_num in num_set:
                max_num += 1
    except FileNotFoundError:
        pass
    return str(max_num)

#Print the item #, name, and price of all the products inside the csv
def print_all_in_csv(dict):
    for item_num, product in dict.items():
        product = dict[item_num]
        print(f"Item {product.id}; Name: {product.name}; Current Price: {product.current_price}; Previous Price: {product.old_price}")


#Adds values from a dict into a set
def import_into_set(dict, set):
    for item_num, product in dict.items():
        product = dict[item_num]
        set.add(product.id)

#Gets the url of product using item number that it is associated with in the csv 
def get_url_from_item_num(item_num, filename="urls.csv"):
    with open(filename, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("item") == item_num:
                url = row.get("url")
                return url

#Print the item number + item name  
def print_item_name(dict):
    for item_num, product in dict.items():
        product = dict[item_num]
        print(f"Item: {product.id}; Name: {product.name}")

#Stores all files currently inside the CSV into a dictionary 
def store_csv_in_dict(dict, filename = "urls.csv"):
    with open(filename, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_num = row.get("Item")
            url = row.get("URL")
            dict[item_num] = Product(item_num, url)

#using the item_num prints the products information
def print_product_info(dict, item_num):
    product = dict[item_num]
    print(f"Name: {product.name}; Price: {product.current_price}")