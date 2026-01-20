import time
import RPi.GPIO as GPIO
from terminal.config import *
from mfrc522 import MFRC522
import board
import neopixel
from terminal_client import verify_payment


def send_request(card_id, value):
    pin = input('Input pin number: ')
    return verify_payment(card_id, pin, value)


def read_card(value: int) -> bool:
    MIFAREReader = MFRC522()
    card_id = None

    try:
        while card_id is None:
            (status_req, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            (status_anti, uid) = MIFAREReader.MFRC522_Anticoll()

            if status_req == MIFAREReader.MI_OK and status_anti == MIFAREReader.MI_OK:
                card_id = "-".join(map(str, uid))

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nKoniec.")

    result = send_request(card_id, value)

    if result:
        confirm()
    else:
        deny()
    return result


def confirm():
    GPIO.output(buzzerPin, 0)
    flashLED(0, 255)
    GPIO.output(buzzerPin, 1)


def deny():
    flashLED(255, 0)


def flashLED(redVal, greenVal):
    pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0/32, auto_write=False)

    pixels.fill((redVal, greenVal, 0))
    pixels.show()
    time.sleep(0.2)

    pixels.fill((0, 0, 0))
    pixels.show()