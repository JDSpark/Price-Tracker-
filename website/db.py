import psycopg2
import os 
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products 
    (id SERIAL PRIMARY KEY, 
    name TEXT NOT NULL, 
    current_price TEXT NOT NULL, 
    last_price TEXT NOT NULL, 
    url TEXT NOT NULL )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS history
    (id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    price REAL NOT NULL,
    date TEXT NOT NULL)
    """)

    conn.commit()
    conn.close()

