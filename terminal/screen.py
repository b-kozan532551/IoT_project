#!/usr/bin/env python3

import time
from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331


disp = None


def display_message(line1, line2, color="WHITE"):
    image = Image.new("RGB", (disp.width, disp.height), "BLACK")
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype('./lib/oled/Font.ttf', 14)
    except IOError:
        font = ImageFont.load_default()
    
    w1, h1 = draw.textsize(line1, font=font)
    x1 = (disp.width - w1) / 2
    y1 = (disp.height / 2) - h1 - 2 
    
    w2, h2 = draw.textsize(line2, font=font)
    x2 = (disp.width - w2) / 2
    y2 = (disp.height / 2) + 2
    
    draw.text((x1, y1), line1, font=font, fill=color)
    draw.text((x2, y2), line2, font=font, fill=color)
    
    disp.ShowImage(image, 0, 0)


def payment_failed():
    display_message("PAYMENT", "FAILED")
    time.sleep(5)
    disp.clear()


def payment_successful():
    display_message("PAYMENT", "SUCCESSFUL")
    time.sleep(5)
    disp.clear()


def total_value_display(value):
    display_message("TOTAL VALUE", str(value / 100) + " pln")


def input_pin():
    display_message("PIN NUMBER")


def clear_screen():
    disp.clear()


def init_screen():    
    try:
        disp = SSD1331.SSD1331()
        disp.Init()
        disp.clear()
        
        time.sleep(5) 
        
    except KeyboardInterrupt:
        print("\nPrzerwano.")
    finally:
        disp.clear()
        disp.reset()

if __name__ == "__main__":
    init_screen()