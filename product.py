from functions import get_next_item_number, get_name_from_url, get_price_from_url
class Product:
    def __init__(self, id:str, url:str):
        self.id = id
        self.url = url 
        self.name = get_name_from_url(url)
        self.price = "test"   
    # name = get_name_from_url(url)
    # current_price = get_price_from_url(url)
    # last_price = "last_price"
    # alert_rules = "alert-rules"
