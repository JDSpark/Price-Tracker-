for item in url_dict:
    found = check_item_in_csv(url_dict, item)
    if found:
         print_product_info(url_dict[item])
    else:
         print("Not Inside Me")