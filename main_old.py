from urllib.parse import urlparse
from pathlib import Path
from functions import get_name_from_url, get_price_from_url, check_item_in_csv, get_next_item_number, save_dict_to_csv, print_product_info, add_to_csv, print_all_in_csv, import_into_set, get_url_from_item_num, print_item_name
from product import Product
MEMBERS = {"1","2","3","4"}
url_dict = {
      "Item 1" : "https://www.amazon.com/nuphy-Air75-V3-Swappable-Mechanical/dp/B0FFFR1CDQ/?_encoding=UTF8&pd_rd_w=DwgPd&content-id=amzn1.sym.4efc43db-939e-4a80-abaf-50c6a6b8c631%3Aamzn1.symc.5a16118f-86f0-44cd-8e3e-6c5f82df43d0&pf_rd_p=4efc43db-939e-4a80-abaf-50c6a6b8c631&pf_rd_r=ATQYTGV8A769EBTPJ9EJ&pd_rd_wg=JqjEN&pd_rd_r=377a3547-3d58-4f6e-895a-7fe8409b70d2&th=1",
      "Item 2" : "Monkey",
}
product_by_id = {}
c = get_next_item_number()

choice = input(
     "What would you like to do: "
     "\n1) View All Products"
     "\n2) View Specific Product"
     "\n3) Add a Product"
     "\n4) Remove a Product\n"
)

while choice.strip() not in MEMBERS:
    choice = input("Enter 1, 2, 3 or 4: ")

#Choice 1: View List
if choice.strip() == "1":
    for item_num, url in url_dict.items():
        product_by_id[item_num] = Product(item_num, url)

#Choice 2: View a Specific item
elif choice.strip() == "2":
    print_item_name()
    members2 = set()
    import_into_set(members2,"item")
    choice2 = input("Enter the # for the item you would like to see: ")
    while choice2.strip() not in members2:
        print_all_in_csv()
        choice2 = input(("Enter a valid item #: "))
    choice2 = choice2.strip()
    choice2_url = get_url_from_item_num(choice2)
    print_product_info(choice2_url)

#Choice 3: Add a Product
elif choice.strip() == "3":
    url = input("Enter URL (press Enter on blank line to finish): ")
    while url != "":
        url_dict[f"{c}"] = url
        c+=1
        url = input("Enter URL (press Enter on blank line to finish): ")
#Choice 4: Delete a Product
elif choice.strip() == "4":
    print('4')
# try:
#      choice = choice.strip()
#      if choice.strip() == "1" or "2" or "3":
#         #Choice 1: View List
#         if choice == 1: 
#             print('1') #placeholder for now 
#         #Choice 2: Add Product
#         elif choice == 2:
#             url = input("Enter URL (press Enter on blank line to finish): ")
#             while url != "":
#                 url_dict[f"Item {c}"] = url
#                 c+=1
#                 url = input("Enter URL (press Enter on blank line to finish): ")
#         #Choice 3: Delete Item from list 
#         elif choice == 3:
#              print("3") #placeholder for now 
                
# except:
#     ValueError

    # Checks to see if all the items inside the dictionary are inside the CSV, if so print product information, if not notify the user (should add to csv and then output all csv items after)
    # for item in url_dict:
    #     found = check_item_in_csv(url_dict, item)
    # if found:
    #      print_product_info(url_dict[item])
    # else:
    #      print(f"{item} Not Inside Me")



