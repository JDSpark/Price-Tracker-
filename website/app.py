from flask import Flask, render_template, request, redirect, url_for, flash
from functions import (load_csv_to_dict, save_dict_to_csv, set_product_info,
                       get_next_item_number, check_item_in_dict, run_updates)
from scraper import get_website
import os
from dotenv import load_dotenv 
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

SUPPORTED_SITES = {"Amazon"}  # Add "Best Buy", "Macy's" here when ready

def get_products():
    return load_csv_to_dict()

@app.route("/")
def home_page():
    products = get_products()
    run_updates(products)
    products = dict(sorted(products.items(), key=lambda x: int(x[0])))
    return render_template("home.html", products=products)

@app.route("/add", methods=["POST"])
def add_product():
    url = request.form.get("url", "").strip()
    if not url:
        flash("Please enter a URL.", "error")
        return redirect(url_for("home_page"))

    site = get_website(url)
    if site not in SUPPORTED_SITES:
        flash(f"{site} is not yet supported. Only Amazon is supported right now.", "error")
        return redirect(url_for("home_page"))

    products = get_products()
    if check_item_in_dict(url, products):
        flash("That product is already being tracked.", "info")
        return redirect(url_for("home_page"))

    new_id = get_next_item_number(products)
    products[new_id] = set_product_info(url, products)
    save_dict_to_csv(products)
    flash("Product added successfully!", "success")
    return redirect(url_for("home_page"))

@app.route("/delete/<int:item_id>", methods=["POST"])
def delete_product(item_id):
    products = get_products()
    if item_id in products:
        del products[item_id]
        save_dict_to_csv(products)
        flash("Product removed.", "info")
    return redirect(url_for("home_page"))

if __name__ == "__main__":
    app.run(debug=True)