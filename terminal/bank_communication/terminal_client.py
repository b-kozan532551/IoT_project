import requests
from hash_data import hash_data


def verify_payment(card_id, pin, value):
    url = "http://LAPTOP-2652TMLP.local:8000/verify_payment"

    payload = {
        "id": card_id,
        "data_hash": hash_data(card_id, pin),
        "value": value
    }

    try:
        response = requests.post(url, json=payload, timeout=2)

        if response.status_code == 200:
            dane = response.json()
            return dane.get("authorized", False)
        else:
            print(f"Server error: {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("Error while connecting to the device")
        return False
    except Exception as e:
        print(f"An unexpected error occured: {e}")
        return False