from urllib.parse import urlparse
from pathlib import Path
from functions import check_item_in_csv, get_next_item_number, add_to_csv, print_all_in_csv, load_csv_to_dict, print_item_name, import_into_set, print_product_info, run_updates
from product import Product
MEMBERS = {"1","2","3","4"}
c = get_next_item_number()
url_dict = {}
product_by_id = {}
load_csv_to_dict(product_by_id)
#all items inside CSV has been loaded into product_by_id dict
run_updates(product_by_id)


choice = input(
     "What would you like to do: "
     "\n1) View All Products"
     "\n2) View Specific Product"
     "\n3) Add a Product"
     "\n4) Remove a Product\n"
)

while choice.strip() not in MEMBERS:
    choice = input("Enter Valid Choice: ")

#View All Items inside CSV
if choice.strip() == "1":
        print_all_in_csv(product_by_id)

#View a Specific Item
elif choice.strip() == "2":
    members2 = set()
    import_into_set(product_by_id, members2)
    print_item_name(product_by_id)
    choice2 = input("Enter the Item Number for the Product You Would Like to View: ")
    while choice2.strip() not in members2:
        choice2 = input("Enter Valid Choice: ")
    item_num = choice2.strip()
    print_product_info(product_by_id, item_num)
     

#Add product information into CSV
elif choice.strip() == "3":
    url = input("Enter URL (press Enter on blank line to finish): ")
    while url != "":
        url_dict[f"{str(c)}"] = url
        c = int(c)
        c+=1
        url = input("Enter URL (press Enter on blank line to finish): ")
    for item_num, url in url_dict.items():
        product_by_id[item_num] = Product(item_num, url)
    for item, product in product_by_id.items():
        found = check_item_in_csv(product)
        if found == False:
            add_to_csv(product.url)
    print("All Products Added Successfully!")

#Delete a Product inside the CSV 
elif choice.strip() == "4":
    print("NOT SETUP YET")