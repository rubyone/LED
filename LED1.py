#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.ls
import sys
import traceback
import threading

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

stop_animation = False # global variable to stop the animation

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

def check_for_quit():
    global stop_animation
    while True:
        user_input = input("Enter 'q' to stop the animation: ")
        if user_input.strip().lower() == 'q':
            stop_animation = True
            break

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

# Move the class definitions before the main function
class LEDController:
    def __init__(self, led_count=41, led_pin=18, led_freq_hz=800000, led_dma=10, 
                 led_brightness=255, led_invert=False, led_channel=0):
        self.strip = Adafruit_NeoPixel(led_count, led_pin, led_freq_hz, led_dma, 
                                      led_invert, led_brightness, led_channel)
        self.strip.begin()
        self.stop_animation = False
        self.last_led_states = [(0, 0, 0)] * led_count

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def colorWipe(self, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            printProgressBar(i + 1, self.strip.numPixels(), 
                           prefix='Animation Progress::', 
                           suffix='Animation Complete', 
                           autosize=True)
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def theaterChase(self, color, wait_ms=50):
        """Movie theater light style chaser animation."""
        while not self.stop_animation:
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, color)
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)

    def rainbow(self, wait_ms=20):
        """Draw rainbow that fades across all pixels at once."""
        j = 0
        while not self.stop_animation:
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)
            j = (j + 1) & 255

    def rainbowCycle(self, wait_ms=20):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        j = 0
        while not self.stop_animation:
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel(
                    (int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)
            j = (j + 1) % 256

    def theaterChaseRainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        j = 0
        while not self.stop_animation:
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, self.wheel((i + j) % 255))
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i + q, 0)
            j = (j + 1) % 256

    def get_color_input(self):
        """Get and validate RGB color input from user"""
        try:
            r = int(input("Red (0 - 255): ").strip())
            g = int(input("Green (0 - 255): ").strip())
            b = int(input("Blue (0 - 255): ").strip())
            
            # Validate color values
            for val in (r, g, b):
                if not 0 <= val <= 255:
                    raise ValueError("Color values must be between 0 and 255")
            
            return Color(r, g, b)
        except ValueError as e:
            print(f"Invalid input: {e}")
            return None

    def start_animation(self, animation_func, *args, **kwargs):
        """Safely start and control an animation"""
        self.stop_animation = False
        input_thread = threading.Thread(target=self.check_for_quit, daemon=True)
        input_thread.start()
        
        try:
            animation_func(*args, **kwargs)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_animation = True
            input_thread.join(timeout=1)

    # Add other LED control methods from the original code
    def check_for_quit(self):
        while True:
            user_input = input("Enter 'q' to stop the animation: ")
            if user_input.strip().lower() == 'q':
                self.stop_animation = True
                break

    def reset(self, wait_ms=50, preserve_state=False):
        if not preserve_state:
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(0, 0, 0))
                self.strip.show()
                time.sleep(wait_ms / 1000.0)

class LEDMenu:
    def __init__(self, controller):
        self.controller = controller
        self.menu_options = {
            'Static Colors': {
                'Red': lambda: self.controller.colorWipe(Color(255, 0, 0)),
                'Green': lambda: self.controller.colorWipe(Color(0, 255, 0)),
                'Blue': lambda: self.controller.colorWipe(Color(0, 0, 255))
                # 'Custom': self.custom_color
            },
            'Animations': {
                'Rainbow': lambda: self.controller.start_animation(self.controller.rainbow),
                'Rainbow Cycle': lambda: self.controller.start_animation(self.controller.rainbowCycle),
                'Theater Chase': lambda: self.controller.start_animation(self.controller.theaterChase, Color(127, 127, 127)),
                'Theater Chase Rainbow': lambda: self.controller.start_animation(self.controller.theaterChaseRainbow)
            }
        }

    def run(self):
        while True:
            questions = [
                inquirer.List('category',
                            message="Choose a category",
                            choices=list(self.menu_options.keys()) + ['Exit']
                            ),
            ]
            category = inquirer.prompt(questions)['category']
            
            if category == 'Exit':
                break
                
            options = list(self.menu_options[category].keys()) + ['Back']
            questions = [
                inquirer.List('option',
                            message=f"Choose {category}",
                            choices=options
                            ),
            ]
            option = inquirer.prompt(questions)['option']
            
            if option != 'Back':
                self.menu_options[category][option]()

# Then define the main function
def main():
    parser = argparse.ArgumentParser(description='LED Strip Controller')
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    parser.add_argument('-b', '--brightness', type=int, default=255, help='LED brightness (0-255)')
    args = parser.parse_args()

    try:
        controller = LEDController(led_brightness=args.brightness)
        menu = LEDMenu(controller)
        menu.run()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        if args.clear:
            controller.reset()

if __name__ == '__main__':
    main()
