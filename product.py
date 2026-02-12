from scraper import get_name_from_url, get_price_from_url, get_price_from_csv
class Product:
    def __init__(self, id:str, url:str):
        self.id = id
        self.url = url 
        self.name = get_name_from_url(url)
        self.current_price = get_price_from_url(url)
        self.old_price = get_price_from_csv(url)
    
    # last_price = "last_price"
    # alert_rules = "alert-rules"
