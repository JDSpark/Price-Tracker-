from math import prod
from typing import Any
from urllib.parse import urlparse
from pathlib import Path
from scraper import get_website
from functions import get_next_item_number, print_all_in_csv, load_csv_to_dict, print_item_name, import_into_set, print_product_info, run_updates, save_dict_to_csv, set_product_info, check_item_in_dict
from product import Product
MEMBERS = {"1","2","3","4"}
url_dict = {}
product_by_id = load_csv_to_dict()
run_updates(product_by_id)
c = get_next_item_number(product_by_id)
#all items inside CSV has been loaded into product_by_id dict

choice = input(
     "What would you like to do: "
     "\n1) View All Products"
     "\n2) View Specific Product"
     "\n3) Add a Product"
     "\n4) Remove a Product\n"
)

while choice.strip() not in MEMBERS:
    choice = input("Enter Valid Choice: ")

#View All Items inside CSV - COMPLETED
if choice.strip() == "1":
        run_updates(product_by_id)
        print_all_in_csv(product_by_id)

#View a Specific Item - COMPLETED
elif choice.strip() == "2":
    members2 = set[int]()
    import_into_set(product_by_id, members2)
    print_item_name(product_by_id)
    choice2 = int(input("Enter the Item Number for the Product You Would Like to View: "))
    while choice2 not in members2:
        choice2 = int(input("Enter Valid Choice: "))
    item_num = choice2
    print_product_info(product_by_id, item_num)
     
#Add product information into CSV
elif choice.strip() == "3":
    members2 = set[int]()
    import_into_set(product_by_id, members2)
    url = input("Enter URL (press Enter on blank line to finish): ")
    while url != "":
        while c in members2:
            c = get_next_item_number(product_by_id)
        found = check_item_in_dict(url, product_by_id)
        if not found:
            product_by_id[f"{c}"] = set_product_info(url, product_by_id)
            members2.add(c)
        url = input("Enter URL (press Enter on blank line to finish): ")

#Delete a Product inside the CSV - Completed
elif choice.strip() == "4":
    members2 = set[int]()
    import_into_set(product_by_id, members2)
    print_item_name(product_by_id)
    choice2 = int(input("Enter the Item Number for the Product You Would Like to Delete: "))
    while choice2 not in members2:
        choice2 = int(input("Enter Valid Choice: "))
    item_num = choice2
    del product_by_id[item_num]
    print_item_name(product_by_id)

save_dict_to_csv(product_by_id)