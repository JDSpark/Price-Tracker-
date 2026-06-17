import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from functions import (get_price_history, load_db_to_dict, fix_url, add_product, delete_product, url_already_tracked)
from scraper import get_website
from scheduler import start_scheduler
from dotenv import load_dotenv
from db import init_db 
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
init_db()

SUPPORTED_SITES = {"Amazon"}  # Add "Best Buy", "Macy's" here when ready

def get_products():
    return load_db_to_dict()

@app.route("/")
def home_page():
    products = get_products()
    products = dict(sorted(products.items(), key=lambda x: int(x[0])))
    return render_template("home.html", products=products)

@app.route("/add", methods=["POST"])
def add_product_flask():
    url = request.form.get("url", "").strip()
    url = fix_url(url)
    if not url:
        flash("The URL You Entered is invalid.", "error")
        return redirect(url_for("home_page"))

    site = get_website(url)
    if site not in SUPPORTED_SITES:
        flash(f"{site} is not yet supported. Only Amazon is supported right now.", "error")
        return redirect(url_for("home_page"))

    if url_already_tracked(url):
        flash("That product is already being tracked.", "info")
        return redirect(url_for("home_page"))

    add_product(url)
    flash("Product added successfully!", "success")
    return redirect(url_for("home_page"))

@app.route("/delete/<int:item_id>", methods=["POST"])
def delete_product_flask(item_id):
    delete_product(item_id)
    flash("Product removed.", "info")
    return redirect(url_for("home_page"))

@app.route("/history/<int:product_id>")
def get_history_flask(product_id):
    product_history_list = get_price_history(product_id)
    return jsonify(product_history_list)

@app.route("/product/<int:product_id>")
def product_page(product_id):
    db_list = get_products()
    product = db_list[product_id]
    return render_template("product.html", product = product)

start_scheduler()
if __name__ == "__main__":
    app.run(debug=True)