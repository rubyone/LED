#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.ls
import sys
import traceback

# sys.path.append(os.path.realpath('.'))

# IDEA: WICHTIG
# wichtig - hier angeben wo das module liegt /sites_packages/inquirer (ohne inquirer)
sys.path.insert(0, "/home/pi/.local/lib/python3.9/site-packages/")
# normal importieren
import inquirer

import time, shutil
from rpi_ws281x import *
import argparse

# LED strip configuration:
LED_COUNT = 41  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', autosize = False):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        autosize    - Optional  : automatically resize the length of the progress bar to the terminal window (Bool)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    styling = '%s |%s| %s%% %s' % (prefix, fill, percent, suffix)
    if autosize:
        cols, _ = shutil.get_terminal_size(fallback = (length, 1))
        length = cols - len(styling)
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s' % styling.replace(fill, bar), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()

last_led_states = [(0, 0, 0)] * LED_COUNT  # Store RGB values for each LED

def save_led_states(strip):
    """Save the current LED colors to the global state"""
    global last_led_states
    for i in range(strip.numPixels()):
        color = strip.getPixelColor(i)
        # Convert 24-bit color to RGB components
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        last_led_states[i] = (r, g, b)

def restore_led_states(strip):
    """Restore the saved LED colors"""
    for i in range(strip.numPixels()):
        r, g, b = last_led_states[i]
        strip.setPixelColor(i, Color(r, g, b))
    strip.show()

# Modify the reset function to optionally preserve the last state
def reset(strip, wait_ms=50, preserve_state=False):
    if not preserve_state:
        items = list(range(strip.numPixels()))
        l = len(items)
        for i in range(strip.numPixels()):
            color = Color(0, 0, 0)
            printProgressBar(i + 1, l, prefix='Reset Animation ::', suffix='Reset Complete', autosize=True)
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
    else:
        restore_led_states(strip)

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    # A List of Items
    items = list(range(strip.numPixels()))
    l = len(items)
    # printProgressBar(0, l, prefix='Animation3 Progress:', suffix='Animation Complete', autosize=True)

    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        printProgressBar(i + 1, l, prefix='Animation Progress::', suffix='Animation Complete', autosize=True)

        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)
        # Update Progress Bar


def theaterChase(strip, color, wait_ms=50):
    """Movie theater light style chaser animation."""
    try:
        while True:
            for q in range(3):
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, color)
                strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, 0)
            if input() == 'q':
                raise KeyboardInterrupt
    except KeyboardInterrupt:
        reset(strip)


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


def rainbow(strip, wait_ms=20):
    """Draw rainbow that fades across all pixels at once."""
    j = 0
    try:
        while True:
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel((i + j) & 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            j = (j + 1) % 256
            if input() == 'q':
                raise KeyboardInterrupt
    except KeyboardInterrupt:
        reset(strip)


def rainbowCycle(strip, wait_ms=20):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    j = 0
    try:
        while True:
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            j = (j + 1) % 256
            if input() == 'q':
                raise KeyboardInterrupt
    except KeyboardInterrupt:
        reset(strip)


def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    j = 0
    try:
        while True:
            for q in range(3):
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, wheel((i + j) % 255))
                strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, strip.numPixels(), 3):
                    strip.setPixelColor(i + q, 0)
            j = (j + 1) % 256
            if input() == 'q':
                save_led_states(strip)  # Save the state before exiting
                raise KeyboardInterrupt
    except KeyboardInterrupt:
        reset(strip, preserve_state=True)  # Preserve the state when resetting


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

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')


    # def reset():
    #     colorWipe(strip, Color(0, 0, 0), 10)


    questions = [
        inquirer.List('size',
                      message="What mode do you want?",
                      choices=['Red', 'Green', 'Blue', 'TheaterChase', 'Own Wipe', 'Rainbow', 'RainbowCycle',
                               'TheaterChaseRainbow'],
                      ),
    ]
    # optionsRGB = [
    #     inquirer.List('options',
    #                   message="Which Color?",
    #                   choices=['Red', 'Green', 'Blue'],
    #                   ),
    # ]

    try:

        while True:

            try:
                answers = inquirer.prompt(questions)
                # value = None
                value = answers["size"]

                if value == "Red":
                    colorWipe(strip, Color(255, 0, 0))  # Red wipe

                elif value == "Green":
                    colorWipe(strip, Color(0, 255, 0))  # green wipe

                elif value == "Blue":
                    colorWipe(strip, Color(0, 0, 255))  # blue wipe

                elif value == "Own Wipe":

                    r = input("Red (0 - 255):")
                    g = input("Green (0 - 255):")
                    b = input("Blue (0 - 255):")
                    valueR = int(r)
                    valueG = int(g)
                    valueB = int(b)
                    colorWipe(strip, Color(valueR, valueG, valueB))  # own wipe

                elif value == "Rainbow":
                    rainbow(strip)
                elif value == "RainbowCycle":
                    rainbowCycle(strip)
                elif value == "TheaterChaseRainbow":
                    theaterChaseRainbow(strip)
                elif value == "TheaterChase":
                    theaterChase(strip, Color(127, 127, 127))

                else:
                    reset(strip)
            except:
                raise

    except Exception as ex:
        print(ex)
        reset(strip)

    except KeyboardInterrupt:
        if args.clear:
            # print ('Pressed "ctrl+c" exit')
            reset(strip)
    # traceback.print_exc()
