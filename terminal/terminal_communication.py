import paho.mqtt.subscribe as subscribe
import json
from hash_data import hash_data
import paho.mqtt.publish as publish
from terminal.card_reader import read_card
from terminal.screen import payment_failed, payment_successful, clear_screen


BROKER_HOST = "test.mosquitto.org"

BANK_SEND = "iot_5214/payment/verification"
BANK_GET = "iot_5214/payment/result"
REGISTER_SEND = "iot_5214/cart/result"
REGISTER_GET = "iot_5214/cart/payment"


def listen(client, userdata, message):
    if message.topic == REGISTER_GET:
        received_data = json.loads(message.payload) 
        print(f"Terminal received {received_data['value']} amount of money")

        data = read_card(value=received_data['value'])

        if data is None:
            send_to_register(False)
        else:
            send_to_bank(card_id=data['card_id'], pin=data['pin'], value=received_data['value'])
    elif message.topic == BANK_GET:
        data = json.loads(message.payload)
        if data['authorized']:
            payment_successful()
        else:
            payment_failed()
        send_to_register(data['authorized'])


def send_to_bank(card_id, pin, value):
    payload = {
        'id': card_id,
        'data_hash': hash_data(card_id, pin),
        'value': value
    }

    publish.single(BANK_SEND, payload=json.dumps(payload), hostname=BROKER_HOST)
    print("Wysłano dane do weryfikacji.")


def send_to_register(result: bool):
    payload = {'result': result}

    publish.single(REGISTER_SEND, payload=json.dumps(payload), hostname=BROKER_HOST)
    print("Wysłano wynik płatności do kasy.")    


if __name__ == "__main__":
    TOPICS = [REGISTER_GET, BANK_GET]
    print(f"Terminal is listening on: {TOPICS}...")
    subscribe.callback(listen, TOPICS, hostname=BROKER_HOST)