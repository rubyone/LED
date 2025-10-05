#!/usr/bin/env python3
"""
LED Strip Controller for Raspberry Pi using WS281x LEDs
Provides various animations and effects for LED strip control
"""
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, List, Optional, Tuple
import sys
import threading
from queue import Queue
import random
import time
import argparse
import json
import socket
import os

# Add site-packages path for inquirer
sys.path.insert(0, "/home/pi/.local/lib/python3.9/site-packages/")
import inquirer
from rpi_ws281x import Adafruit_NeoPixel, Color

def load_config():
    """Load configuration based on hostname and user"""
    try:
        hostname = socket.gethostname()
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        current_user = os.getenv('USER')
        
        with open(config_path, 'r') as f:
            configs = json.load(f)
            
        # If running as root, look for root_user flag
        if current_user == 'root':
            for machine_config in configs.values():
                if machine_config.get('root_user', False):
                    return machine_config
            # If no root configuration found, try to detect based on hostname
            if hostname in configs:
                return configs[hostname]
            raise ValueError("No root configuration found")
            
        # Try to get config for this machine based on username
        for machine_config in configs.values():
            if machine_config['username'] == current_user:
                return machine_config
                
        raise ValueError(f"No configuration found for user: {current_user}")
        
    except Exception as e:
        raise RuntimeError(f"Failed to load configuration: {str(e)}")

# LED strip configuration
@dataclass
class LEDConfig:
    """Configuration settings for LED strip"""
    COUNT: int = 120  # This will be overridden
    PIN: int = 18  # GPIO pin (18 uses PWM!)
    FREQ_HZ: int = 800000
    DMA: int = 10
    BRIGHTNESS: int = 255
    INVERT: bool = False
    CHANNEL: int = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
    
    @classmethod
    def from_machine_config(cls):
        """Create config from machine-specific settings"""
        config = load_config()
        return cls(
            COUNT=config['led_count'],
            PIN=config['led_pin']
        )

class AnimationType(Enum):
    """Available animation types"""
    RAINBOW = "Rainbow"
    RAINBOW_CYCLE = "Rainbow Cycle"
    THEATER_CHASE = "Theater Chase"
    THEATER_CHASE_RAINBOW = "Theater Chase Rainbow"
    BREATHE = "Breathe"
    FIRE = "Fire Effect"

class ColorPreset(Enum):
    """Preset colors for the LED strip"""
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    WARM_WHITE = (255, 147, 41)
    
    @property
    def color(self) -> int:
        """Convert RGB tuple to Color value"""
        r, g, b = self.value
        return Color(r, g, b)

class LEDController:
    """Controls LED strip animations and effects"""
    
    def __init__(self, config: LEDConfig = LEDConfig()):
        """Initialize LED controller with given configuration"""
        try:
            self.strip = Adafruit_NeoPixel(
                config.COUNT, config.PIN, config.FREQ_HZ,
                config.DMA, config.INVERT, config.BRIGHTNESS, config.CHANNEL
            )
            self.strip.begin()
            if not self.strip.numPixels():
                raise RuntimeError("Failed to initialize LED strip - no pixels detected")
            self.stop_animation = False
            self.animation_thread: Optional[threading.Thread] = None
            self.animation_queue: Queue = Queue()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize LED strip: {str(e)}")

    def wheel(self, pos: int) -> int:
        """Generate rainbow colors across 0-255 positions."""
        pos = pos % 256
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def colorWipe(self, color, wait_ms: int = 50) -> None:
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            if self.stop_animation:
                break
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms / 1000.0)

    def rainbow(self, wait_ms: int = 20) -> None:
        """Draw rainbow that fades across all pixels at once."""
        j = 0
        while not self.stop_animation:
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)
            j = (j + 1) & 255

    def rainbowCycle(self, wait_ms: int = 20) -> None:
        """Draw rainbow that uniformly distributes itself across all pixels."""
        j = 0
        while not self.stop_animation:
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel(
                    (int(i * 256 / self.strip.numPixels()) + j) & 255))
            self.strip.show()
            time.sleep(wait_ms / 1000.0)
            j = (j + 1) % 256

    def theaterChaseRainbow(self, wait_ms: int = 50) -> None:
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

    def breathe(self, color: int, speed_ms: int = 20) -> None:
        """Breathing effect that smoothly fades in and out"""
        while not self.stop_animation:
            # Fade in
            for brightness in range(0, 255, 2):
                self.strip.setBrightness(brightness)
                self.colorWipe(color, wait_ms=0)
                time.sleep(speed_ms/1000.0)
            # Fade out
            for brightness in range(255, 0, -2):
                self.strip.setBrightness(brightness)
                self.colorWipe(color, wait_ms=0)
                time.sleep(speed_ms/1000.0)

    def fire_effect(self) -> None:
        """Simulate fire effect"""
        while not self.stop_animation:
            for i in range(self.strip.numPixels()):
                flicker = random.randint(0, 55)
                self.strip.setPixelColor(i, Color(255 - flicker, 35, 0))
            self.strip.show()
            time.sleep(random.uniform(0.05, 0.2))

    def get_color_input(self) -> Optional[Color]:
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

    def start_animation(self, animation_type: AnimationType, *args, **kwargs) -> None:
        """Safely start and control an animation"""
        animation_map = {
            AnimationType.RAINBOW: self.rainbow,
            AnimationType.RAINBOW_CYCLE: self.rainbowCycle,
            AnimationType.THEATER_CHASE: self.theaterChaseRainbow,
            AnimationType.BREATHE: self.breathe,
            AnimationType.FIRE: self.fire_effect
        }
        
        self.stop_current_animation()
        
        if animation_func := animation_map.get(animation_type):
            self.stop_animation = False
            self.animation_thread = threading.Thread(
                target=animation_func,
                args=args,
                kwargs=kwargs,
                daemon=True
            )
            self.animation_thread.start()

    def stop_current_animation(self) -> None:
        """Stop the currently running animation"""
        self.stop_animation = True
        if self.animation_thread and self.animation_thread.is_alive():
            self.animation_thread.join(timeout=1.0)

    def cleanup(self) -> None:
        """Clean up resources and turn off LEDs"""
        self.stop_current_animation()
        self.reset()
        self.turn_off()

    def check_for_quit(self):
        while True:
            user_input = input("Enter 'q' to stop the animation: ")
            if user_input.strip().lower() == 'q':
                self.stop_animation = True
                break

    def reset(self, wait_ms: int = 50, preserve_state: bool = False) -> None:
        if not preserve_state:
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(0, 0, 0))
                self.strip.show()
                time.sleep(wait_ms / 1000.0)

    def set_brightness(self, brightness: int) -> None:
        """Set the brightness level (0-255)"""
        if not 0 <= brightness <= 255:
            raise ValueError("Brightness must be between 0 and 255")
        self.strip.setBrightness(brightness)
        self.strip.show()
    
    def turn_off(self) -> None:
        """Turn off the LED strip"""
        self.strip.setBrightness(0)
        self.strip.show()

    def get_leds(self) -> int:
        """Get the number of LEDs"""
        return self.strip.numPixels()
    
    def set_custom_color(self) -> None:
        """Set a custom color from user input"""
        try:
            if color := self.controller.get_color_input():
                self.controller.colorWipe(color)
                print("Custom color applied successfully")
        except Exception as e:
            print(f"Error setting custom color: {e}")

class LEDMenu:
    """Interactive menu system for LED control"""
    
    def __init__(self, controller: LEDController):
        self.controller = controller
        self.setup_menu_options()

    def setup_menu_options(self) -> None:
        """Setup the menu structure"""
        self.menu_options = {
            'Static Colors': {
                color.name: lambda c=color: self.controller.colorWipe(c.color)
                for color in ColorPreset
            },
            'Animations': {
                anim.value: lambda a=anim: self.controller.start_animation(a)
                for anim in AnimationType
            },
            'Settings': {
                'Set Brightness': self.set_brightness,
                'Custom Color': self.set_custom_color
            }
        }

    def run(self) -> None:
        """Run the interactive menu"""
        try:
            while True:
                category = self.prompt_category()
                if category == 'Exit':
                    break
                
                self.handle_category_selection(category)
        except KeyboardInterrupt:
            print("\nExiting menu...")
        finally:
            self.controller.cleanup()

    def prompt_category(self) -> str:
        """Prompt user for category selection"""
        questions = [
            inquirer.List('category',
                         message="Choose a category",
                         choices=list(self.menu_options.keys()) + ['Exit']
                         ),
        ]
        return inquirer.prompt(questions)['category']

    def set_brightness(self) -> None:
        try:
            brightness = int(input("Enter brightness (0-255): ").strip())
            self.controller.set_brightness(brightness)
            print(f"Brightness set to {brightness}")
        except ValueError as e:
            print(f"Invalid input: {e}")

    def set_custom_color(self) -> None:
        """Set a custom color from user input"""
        try:
            if color := self.controller.get_color_input():
                self.controller.colorWipe(color)
                print("Custom color applied successfully")
        except Exception as e:
            print(f"Error setting custom color: {e}")

    def handle_category_selection(self, category: str) -> None:
        """Handle the selection of a menu category"""
        if category in self.menu_options:
            options = list(self.menu_options[category].keys()) + ['Back']
            questions = [
                inquirer.List('option',
                             message=f"Choose {category}",
                             choices=options
                             ),
            ]
            
            if option := inquirer.prompt(questions)['option']:
                if option != 'Back':
                    try:
                        # Execute the selected option
                        self.menu_options[category][option]()
                    except Exception as e:
                        print(f"Error executing {option}: {e}")

def main() -> None:
    """Main entry point for the LED controller"""
    parser = argparse.ArgumentParser(description='LED Strip Controller')
    parser.add_argument('-c', '--clear', action='store_true',
                       help='clear the display on exit')
    parser.add_argument('-b', '--brightness', type=int, default=255,
                       help='LED brightness (0-255)')
    args = parser.parse_args()

    # Load machine-specific config
    config = LEDConfig.from_machine_config()
    config.BRIGHTNESS = args.brightness
    
    try:
        controller = LEDController(config)
        menu = LEDMenu(controller)
        menu.run()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if args.clear:
            controller.cleanup()

if __name__ == '__main__':
    main()
