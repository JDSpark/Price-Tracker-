import sqlite3
import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "products.db")

def get_connection():
    return sqlite3.connect(DATABASE)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products 
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL, 
    current_price TEXT NOT NULL, 
    last_price TEXT NOT NULL, 
    url TEXT NOT NULL )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS history
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    price REAL NOT NULL,
    date TEXT NOT NULL)
    """)

    conn.commit()
    conn.close()

