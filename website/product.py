from scraper import get_name_from_url, get_price_from_url, get_price_from_csv
from typing import Optional

class Product:
    def __init__(self, id:int, url:str, name:str , current_price:str, last_price:Optional[str] = None):
        self.id = id
        self.url = url 
        self.name = name
        self.current_price = current_price
        if last_price is None:
            self.last_price =  current_price
        else:
            self.last_price = last_price

    # alert_rules = "alert-rules"

    def apply_new_price(self, new_price: str) -> bool:
        if not new_price:
            return False
        
        if new_price != self.current_price:
            self.last_price = self.current_price
            self.current_price = new_price
            return True
        
        return False