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
        writer.writerow(["Item", "Name", "Current Price", "Last Price", "URL"])
        for item_num, product in dict.items():
            product = dict[item_num]
            if product.last_price == "":
                product.last_price = product.current_price
            writer.writerow([product.id, product.name, product.current_price, product.last_price, product.url])
                

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
    product = set_product_info(url)
    item = get_next_item_number()
    with open(filename, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([product.id, product.name, product.current_price, product.last_price, product.url])
        
#Get the next item number based on how many items already in CSV 
def get_next_item_number(dict, filename="urls.csv"): 
    max_num = 1
    num_set = set[int]()
    import_into_set(dict, num_set)
    while max_num in num_set:
        max_num+=1
    return max_num

#Print the item #, name, and price of all the products inside the csv
def print_all_in_csv(dict):
    for item_num, product in dict.items():
        product = dict[item_num]
        print(f"Item {product.id}; Name: {product.name}; Current Price: {product.current_price}; Previous Price: {product.last_price}")

#Adds id values from a dict into a set
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
def load_csv_to_dict(filename = "urls.csv"):
    products_by_id = {}
    with open(filename, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_num = row.get("Item")
            item_num = int(item_num)
            url = row.get("URL")
            name = row.get("Name")
            current_price = row.get("Current Price")
            last_price = row.get("Last Price")
            products_by_id[item_num] = Product(item_num, url, name, current_price, last_price)
    return products_by_id

#using the item_num prints the products information
def print_product_info(dict, item_num):
    product = dict[item_num]
    print(f"Name: {product.name}; Price: {product.current_price}")

#Checks to see if there are any price changes from the products inside CSV
def check_for_new_price(dict):
    for item_num, product in dict.items():
        product = dict[item_num]
        current_price = product.current_price
        last_price = product.last_price 
        if current_price != last_price:
            print(f"{product.name} Had a Price Change from {product.last_price} to {product.current_price}.")
            product.last_price = current_price
            product.current_price = get_price_from_url(product.url)

#runs checks and updates CSV 
def run_updates(dict):
    check_for_new_price(dict)
    save_dict_to_csv(dict)

#Sets the product information using the URL
def set_product_info(url, dict):
    name = get_name_from_url(url)
    id = get_next_item_number(dict)
    current_price = get_price_from_url(url)
    product = Product(id, url, name, current_price)
    return product
    
#check to see if product already inside of a dict, if not gets added 
def check_item_in_dict(item_to_check, dict, filename="urls.csv"): 
        for item_num, product in dict.items():
            url = product.url
            if item_to_check == url:
                print(f"Item {product.name} is Already being Tracked")
                return True
        return False
