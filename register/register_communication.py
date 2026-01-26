from product_scanner import scan_bar_codes
from product_database import Product
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import json


BROKER_HOST = "test.mosquitto.org"

TOPIC_GET = "iot_5214/cart/result"
TOPIC_SEND = "iot_5214/cart/payment"


prev_products: list[Product] = []


def listen(client, userdata, message):
    global prev_products

    data = json.loads(message.payload)
    if data['result']:
        print("Payment successful. Finalizing purchase...")
        prev_products = []
        prev_products = run_register()
    else:
        print("Payment failed. Please try again.")
        prev_products = run_register()   


def run_register():
    global prev_products

    products: list[Product] = scan_bar_codes()
    products += prev_products

    total_value = sum(product.value for product in products)

    publish.single(TOPIC_SEND, payload=json.dumps({'value': total_value}), hostname=BROKER_HOST)
    return products


if __name__ == "__main__":
    prev_products = run_register()
    print(f"Register is listening on topic {TOPIC_GET}...")
    subscribe.callback(listen, TOPIC_GET, hostname=BROKER_HOST)