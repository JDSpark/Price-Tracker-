import csv
import time
from product import Product
from scraper import get_product_info_amazon
from alerts import send_price_alert

# -------------------------------------------------------
# URL Cleaner
# -------------------------------------------------------

def fix_url(url):
    if "/dp/" not in url:
        return None
    start = url.find("/dp/") + len("/dp/")
    slash = url.find("/", start)
    question_mark = url.find("?", start)
    #if -1 is outputed, it means there was no character found in the string
    if question_mark == -1 and slash == -1:
        end = len(url)
    elif question_mark == -1:
        end = slash
    elif slash == -1:
        end = question_mark
    elif question_mark != -1 and slash != -1:
        end = min(question_mark, slash)
    dp = url[start:end]
    if len(dp) != 10:
        return None
    clean_url = "https://www.amazon.com/dp/" + dp
    return clean_url

# -------------------------------------------------------
# CSV — Save
# -------------------------------------------------------

def save_dict_to_csv(dict, filename="urls.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Item", "Name", "Current Price", "Last Price", "URL"])
        for item_num, product in dict.items():
            if product.last_price == "" or product.last_price is None:
                product.last_price = product.current_price
            writer.writerow([product.id, product.name, product.current_price, product.last_price, product.url])

# -------------------------------------------------------
# CSV — Load
# -------------------------------------------------------

def load_csv_to_dict(filename="urls.csv"):
    products_by_id = {}
    with open(filename, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_num = int(row.get("Item"))
            url = row.get("URL")
            name = row.get("Name")
            current_price = row.get("Current Price")
            last_price = row.get("Last Price")
            products_by_id[item_num] = Product(item_num, url, name, current_price, last_price)
    return products_by_id

# -------------------------------------------------------
# ID Management
# -------------------------------------------------------

def get_next_item_number(dict):
    num_set = set()
    import_into_set(dict, num_set)
    max_num = 1
    while max_num in num_set:
        max_num += 1
    return max_num

def import_into_set(dict, set):
    for item_num, product in dict.items():
        set.add(product.id)

# -------------------------------------------------------
# Product Info
# -------------------------------------------------------

def set_product_info(url, dict):
    name, current_price = get_product_info_amazon(url)
    id = get_next_item_number(dict)
    product = Product(id, url, name, current_price)
    return product

def check_item_in_dict(item_to_check, dict):
    for item_num, product in dict.items():
        if item_to_check == product.url:
            return True
    return False

# -------------------------------------------------------
# Price Updates
# -------------------------------------------------------

def check_for_price_updates(dict):
    changes = []
    for item_num, product in dict.items():
        old_price = product.current_price
        _, new_price = get_product_info_amazon(product.url)
        time.sleep(2)
        changed = product.apply_new_price(new_price)
        if changed:
            changes.append({
                "name": product.name,
                "old_price": old_price,
                "new_price": product.current_price,
                "url" : product.url
            })
            print(f"{product.name}: {product.last_price} → {product.current_price}")
    return changes

def run_updates():
    dict = load_csv_to_dict()
    changes = check_for_price_updates(dict)
    save_dict_to_csv(dict)
    for change in changes:
        send_price_alert(change["name"], change["old_price"], change["new_price"], change["url"])
    return changes

# -------------------------------------------------------
# CLI helpers (used by main.py only)
# -------------------------------------------------------

def print_all_in_csv(dict):
    for item_num, product in dict.items():
        print(f"Item {product.id}; Name: {product.name}; Current Price: {product.current_price}; Previous Price: {product.last_price}")

def print_item_name(dict):
    for item_num, product in dict.items():
        print(f"Item: {product.id}; Name: {product.name}")

def print_product_info(dict, item_num):
    product = dict[item_num]
    print(f"Name: {product.name}; Price: {product.current_price}")