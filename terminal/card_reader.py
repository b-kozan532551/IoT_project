import time
import RPi.GPIO as GPIO
from terminal.config import *
from mfrc522 import MFRC522
import board
import neopixel
import screen


button_pressed = False


def redButtonCallback(pin):
    global button_pressed
    button_pressed = True


def read_card(value: int):
    global button_pressed
    button_pressed = False
    MIFAREReader = MFRC522()
    card_id = None

    try:
        GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=redButtonCallback, bouncetime=200)
    except RuntimeError:
        GPIO.remove_event_detect(buttonRed)
        GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=redButtonCallback, bouncetime=200)

    screen.total_value_display(value)

    try:
        while card_id is None:
            if button_pressed:
                screen.clear_screen()
                screen.payment_failed()

                GPIO.remove_event_detect(buttonRed)
                return None
            
            (status_req, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            (status_anti, uid) = MIFAREReader.MFRC522_Anticoll()

            if status_req == MIFAREReader.MI_OK and status_anti == MIFAREReader.MI_OK:
                card_id = "-".join(map(str, uid))

            time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.remove_event_detect(buttonRed)
        print("\nKoniec.")

    card_read()
    GPIO.remove_event_detect(buttonRed)
    screen.clear_screen()
    screen.input_pin()

    pin = input('Input pin number: ')
    screen.clear_screen()
    return {"card_id": card_id, "pin": pin}


def card_read():
    GPIO.output(buzzerPin, 0)
    flashLED(0, 255)
    GPIO.output(buzzerPin, 1)


def flashLED(redVal, greenVal):
    try:
        pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0/32, auto_write=False)

        pixels.fill((redVal, greenVal, 0))
        pixels.show()

        time.sleep(0.2)

        pixels.fill((0, 0, 0))
        pixels.show()
    except Exception as e:
        print(f"Błąd LED: {e}")