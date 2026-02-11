from urllib.parse import urlparse
from pathlib import Path
from functions import get_name_from_url, get_price_from_url, check_item_in_csv, get_next_item_number, save_dict_to_csv, print_product_info, add_to_csv, print_all_in_csv, import_into_set, get_url_from_item_num, print_item_name
from product import Product
MEMBERS = {"1","2","3","4"}
c = get_next_item_number()
url_dict = {}
product_by_id = {}
choice = input("Enter a choice (1,2,3,4): ")

while choice.strip() not in MEMBERS:
    choice = input("Enter Valid Choice: ")

#View All Items inside CSV
if choice.strip() == "1":
    for item_num, url in url_dict.items():
        product_by_id[item_num] = Product(item_num, url)
    for item_num, product in product_by_id.items():
        item = product_by_id[item_num]
        print(f"Item {item.id}; Name: {item.name}; Price: {item.price}")

#Add product information into CSV
elif choice.strip() == "2":
    url = input("Enter URL (press Enter on blank line to finish): ")
    while url != "":
        url_dict[f"{str(c)}"] = url
        c+=1
        url = input("Enter URL (press Enter on blank line to finish): ")
    for item_num, url in url_dict.items():
        product_by_id[item_num] = Product(item_num, url)
    for item, product in product_by_id.items(): 
        check_item_in_csv(product)
        if check_item_in_csv == False:
            add_to_csv(product.url)