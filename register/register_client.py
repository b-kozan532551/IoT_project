# Gdy użytkownik zakończy skanowanie, wciska enter i kwota jest wysyłana do terminal_server

from product_scanner import scan_bar_codes
from product_database import Product
import requests

TERMINAL_SERVER_URL = "http://0.0.0.0:8001/cart/pay"

def run_register() -> int:

    products: list[Product] = scan_bar_codes()
    total_value = sum(product.value for product in products)

    requests.post(TERMINAL_SERVER_URL, data=total_value)

    return total_value

if __name__ == "__main__":
    run_register()