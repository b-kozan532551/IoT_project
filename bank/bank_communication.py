import json
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
from bank.payment_processing import verify_payment
from bank.bank_database import create_bank_db


BROKER_HOST = "test.mosquitto.org"
TOPIC_GET = "iot_5214/payment/verification"
TOPIC_SEND = "iot_5214/payment/result"


def verify_pin(client, userdata, message):
    data = json.loads(message.payload)
    is_authorized = verify_payment(data['id'], data['data_hash'], data['value'])

    response = json.dumps({'authorized': is_authorized})
    publish.single(TOPIC_SEND, payload=response, hostname=BROKER_HOST)


if __name__ == "__main__":
    create_bank_db()
    print(f"Bank is listening on topic {TOPIC_GET}...")
    subscribe.callback(verify_pin, TOPIC_GET, hostname=BROKER_HOST)