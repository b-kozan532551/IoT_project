from config import *
import RPi.GPIO as GPIO
from terminal.bank_communication.card_reader import read_card


def greenButtonCallback(pin):
    value = None  # Tu dodaj aby value przy kliknięciu przycisku brało aktualnie nabitą kwotę do zapłaty
    read_card(value)


def redButtonCallback(pin):
    pass  # Tu dodaj powrót do dodawania produktów


def main():
    GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=redButtonCallback, bouncetime=200)
    GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=greenButtonCallback, bouncetime=200)