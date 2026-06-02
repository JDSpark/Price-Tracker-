import threading
import time
from product import Product
from scraper import get_name_from_path, get_product_info_amazon
from alerts import send_price_alert
from db import get_connection

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
    name = get_name_from_path(url)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO products (name, current_price, last_price, url) VALUES (?,?,?,?) ", (name, "Fetching...", "Fetching...", url))
    conn.commit()
    new_id = cur.lastrowid
    threading.Thread(target=scrape_and_update, args=(new_id, url)).start()
    product = Product(new_id, url, name, "Fetching...", "Fetching...")
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
# Helper Functions
# -------------------------------------------------------

def import_into_set(dict, set):
    for item_num, product in dict.items():
        set.add(product.id)

def scrape_and_update(product_id, url):
    for attempt in range(10):
        name, price = get_product_info_amazon(url)
        if price == "N/A":
            time.sleep(15)
        else:
            break
    if price == "N/A":
        price = "FAILED"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE products SET name = ?, current_price = ?, last_price = ? WHERE id = ?", (name, price, price, product_id,))
    conn.commit()
    conn.close()

# -------------------------------------------------------
# Price Updates
# -------------------------------------------------------

def run_updates():
    product_dict = load_db_to_dict()
    for item_num, item in product_dict.items():
        _, new_price = get_product_info_amazon(item.url)
        if new_price != item.current_price:
            item.apply_new_price(new_price) 
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE products SET current_price = ?, last_price = ? WHERE id = ?", (item.current_price, item.last_price, item.id))
            conn.commit()
            conn.close()
            send_price_alert(item.name, item.last_price, item.current_price, item.url)


# -------------------------------------------------------
# CLI helpers (used by main.py only)
# -------------------------------------------------------

def print_item_name(dict):
    for item_num, product in dict.items():
        print(f"Item: {product.id}; Name: {product.name}")

def print_product_info(dict, item_num):
    product = dict[item_num]
    print(f"Name: {product.name}; Price: {product.current_price}")