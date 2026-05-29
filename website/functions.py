import sqlite3
import time
from product import Product
from scraper import get_name_from_url, get_price_from_url, get_product_info_amazon
from alerts import send_price_alert
from website.db import get_connection

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
# Database Management
# -------------------------------------------------------

def load_db_to_dict():
    product_dict = {}
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(""" SELECT * FROM products """)
    rows = cur.fetchall()
    for row in rows:
        product = Product(id=row[0],url=row[4],name=row[1], current_price=row[2],last_price=row[3])
        product_dict[product.id] = product
    conn.close()
    return product_dict

def add_product(url):
    name, price = get_product_info_amazon(url)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO products (name, current_price, last_price, url) VALUES (?,?,?,?) ", (name, price, price, url))
    conn.commit()
    new_id = cur.lastrowid
    product = Product(new_id, url, name, price, price)
    conn.close()
    return product

def delete_product(product_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def url_already_tracked(url):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM products WHERE url = ?", (url,))
    check = cur.fetchone()
    conn.close()
    return check is not None
    
# -------------------------------------------------------
# ID Management
# -------------------------------------------------------

def import_into_set(dict, set):
    for item_num, product in dict.items():
        set.add(product.id)

# -------------------------------------------------------
# Product Info
# -------------------------------------------------------

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

def print_item_name(dict):
    for item_num, product in dict.items():
        print(f"Item: {product.id}; Name: {product.name}")

def print_product_info(dict, item_num):
    product = dict[item_num]
    print(f"Name: {product.name}; Price: {product.current_price}")