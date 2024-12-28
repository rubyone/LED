#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.ls
import sys
import traceback
import os


# from tkinter import messagebox
import tkinter as tk
import os
#from tkinter.colorchooser import askcolor
# from tkinter import choosecolor
# from tkinter import colorchooser



# sys.path.append(os.path.realpath('.'))

# # IDEA: WICHTIG
# # wichtig - hier angeben wo das module liegt /sites_packages/inquirer (ohne inquirer)
sys.path.insert(0, "/home/pi/.local/lib/python3.9/site-packages/")
# # normal importieren
# import inquirer

import time
from rpi_ws281x import *
import argparse

# LED strip configuration:
LED_COUNT = 30  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbowCycle(strip, wait_ms=20, iterations=1):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

def reset():
    colorWipe(strip, Color(0, 0, 0), 10)


def print_hi():
    if os.environ.get('DISPLAY', '') == '':
        print('no display found. Using :0.0')
        os.environ.__setitem__('DISPLAY', ':0.0')

    # create main window
#    master = tk.Tk()
 #   master.title("tester")
 #   master.geometry("350x300")
#
    # color chooser
    def choose_color():
        # variable to store hexadecimal code of color
        color_code = askcolor(title="Choose color")
        # get rgb from color_code tuple
        rgb = color_code[0]
        # extract r,g,b from rgb
        r = int(rgb[0])
        g = int(rgb[1])
        b = int(rgb[2])
        # print(r,g,b)
        reset()
        # pass r,g,b to color whipe
        master.configure(background=color_code[1])
        colorWipe(strip, Color(r, g, b))  # Red wipe
    # r,g,b function
    def red():
        reset()
        colorWipe(strip, Color(255, 0, 0))  # Red wipe
        master.configure(background='red')
    def green():
        reset()
        colorWipe(strip, Color(0, 255, 0))  # green wipe
        master.configure(background='green')
    def blue():
        reset()
        colorWipe(strip, Color(0, 0, 255))  # blue wipe
        master.configure(background='blue')

    R = Button(master, text="RED", command=red)
    G = Button(master, text="GREEN", command=green)
    B = Button(master, text="BLUE", command=blue)
    # choose
    C = Button(master, text="Select color", command=choose_color)

    R.place(x=0, y=0)
    G.place(x=0, y=50)
    B.place(x=0, y=100)
    C.place(x=0, y=150)

    # Run forever!
    master.mainloop()


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    print_hi()

