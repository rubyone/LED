"""
Mock implementation of rpi_ws281x for development on non-Raspberry Pi systems
"""

class Color:
    @staticmethod
    def __call__(red, green, blue, white=0):
        """Create a color value from RGB components"""
        return (white << 24) | (red << 16) | (green << 8) | blue

def Color(red, green, blue, white=0):
    """Create a color value from RGB components"""
    return (white << 24) | (red << 16) | (green << 8) | blue

class Adafruit_NeoPixel:
    """Mock NeoPixel class for development"""
    
    def __init__(self, num, pin, freq_hz=800000, dma=10, invert=False, brightness=255, channel=0):
        self.num = num
        self.pin = pin
        self.brightness = brightness
        self._pixels = [0] * num
        print(f"Mock NeoPixel initialized: {num} LEDs on pin {pin}")
    
    def begin(self):
        """Initialize the library"""
        print("Mock NeoPixel: begin() called")
    
    def show(self):
        """Update the LED strip with current pixel values"""
        print("Mock NeoPixel: show() called - updating LEDs")
    
    def setPixelColor(self, n, color):
        """Set the color of a specific pixel"""
        if 0 <= n < self.num:
            self._pixels[n] = color
            # Extract RGB values for display
            r = (color >> 16) & 0xFF
            g = (color >> 8) & 0xFF
            b = color & 0xFF
            print(f"Mock: Set pixel {n} to RGB({r}, {g}, {b})")
    
    def getPixelColor(self, n):
        """Get the color of a specific pixel"""
        if 0 <= n < self.num:
            return self._pixels[n]
        return 0
    
    def setBrightness(self, brightness):
        """Set the overall brightness"""
        self.brightness = brightness
        print(f"Mock NeoPixel: brightness set to {brightness}")
    
    def getBrightness(self):
        """Get the current brightness"""
        return self.brightness
    
    def numPixels(self):
        """Get the number of pixels"""
        return self.num
