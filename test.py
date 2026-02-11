import csv
import os
from functions import * 
from product import Product


c = get_next_item_number
url_dict = {
    "1" : "https://www.amazon.com/nuphy-Air75-V3-Swappable-Mechanical/dp/B0FFFR1CDQ/?_encoding=UTF8&pd_rd_w=DwgPd&content-id=amzn1.sym.4efc43db-939e-4a80-abaf-50c6a6b8c631%3Aamzn1.symc.5a16118f-86f0-44cd-8e3e-6c5f82df43d0&pf_rd_p=4efc43db-939e-4a80-abaf-50c6a6b8c631&pf_rd_r=ATQYTGV8A769EBTPJ9EJ&pd_rd_wg=JqjEN&pd_rd_r=377a3547-3d58-4f6e-895a-7fe8409b70d2&th=1",
    "2" : "https://www.amazon.com/nuphy-Air75-V2-Mechanical-Grey-Gateron/dp/B0CMYYM2SQ/?_encoding=UTF8&pd_rd_w=DwgPd&content-id=amzn1.sym.4efc43db-939e-4a80-abaf-50c6a6b8c631%3Aamzn1.symc.5a16118f-86f0-44cd-8e3e-6c5f82df43d0&pf_rd_p=4efc43db-939e-4a80-abaf-50c6a6b8c631&pf_rd_r=ATQYTGV8A769EBTPJ9EJ&pd_rd_wg=JqjEN&pd_rd_r=377a3547-3d58-4f6e-895a-7fe8409b70d2&th=1",
    "3" : "https://www.amazon.com/nuphy-Mechanical-Compatible-Bluetooth-White-Gateron/dp/B0CQRLHPSP/?_encoding=UTF8&pd_rd_w=DwgPd&content-id=amzn1.sym.4efc43db-939e-4a80-abaf-50c6a6b8c631%3Aamzn1.symc.5a16118f-86f0-44cd-8e3e-6c5f82df43d0&pf_rd_p=4efc43db-939e-4a80-abaf-50c6a6b8c631&pf_rd_r=ATQYTGV8A769EBTPJ9EJ&pd_rd_wg=JqjEN&pd_rd_r=377a3547-3d58-4f6e-895a-7fe8409b70d2&th=1",
    "4" : "https://www.amazon.com/nuphy-Wireless-Mechanical-Bluetooth-Connection/dp/B0CRKR24FC/?_encoding=UTF8&pd_rd_w=DwgPd&content-id=amzn1.sym.4efc43db-939e-4a80-abaf-50c6a6b8c631%3Aamzn1.symc.5a16118f-86f0-44cd-8e3e-6c5f82df43d0&pf_rd_p=4efc43db-939e-4a80-abaf-50c6a6b8c631&pf_rd_r=ATQYTGV8A769EBTPJ9EJ&pd_rd_wg=JqjEN&pd_rd_r=377a3547-3d58-4f6e-895a-7fe8409b70d2&th=1",
    }
products_by_id_num = {}

for item_num, url in url_dict.items():
    products_by_id_num[item_num] = Product(item_num,url)
    #item = item in dict
    #url = url in dict

    # item number = first item in dict
    # url = second item in dict 

#prints id number for all products inside the products_by_id_num dict
for item_num, product in products_by_id_num.items():
    print(products_by_id_num[item_num].id)

item2 = products_by_id_num['2']