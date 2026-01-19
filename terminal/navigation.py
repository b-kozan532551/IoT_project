from config import *
import RPi.GPIO as GPIO
from terminal.bank_communication.card_reader import read_card


def redButtonCallback(pin):
    pass  # Tu dodaj powrót do dodawania produktów


def main():
    GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=redButtonCallback, bouncetime=200)
