from flask import Flask, render_template, jsonify
import logging
from logging.handlers import RotatingFileHandler
from LED1 import LEDController, LEDConfig, AnimationType, ColorPreset
# Import Color from appropriate library based on platform
try:
    from rpi_ws281x import Color
except ImportError:
    from mock_rpi_ws281x import Color
import traceback
import sys
import os
import socket

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
# Use local directory for log file on development systems
log_file = '/var/log/led-server.log' if os.path.exists('/var/log') and os.access('/var/log', os.W_OK) else 'led-server.log'
handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=3)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
app.logger.info('LED Server startup')

def log_system_info():
    """Log relevant system information for debugging"""
    app.logger.info(f"Current user: {os.getenv('USER')}")
    app.logger.info(f"Hostname: {socket.gethostname()}")
    app.logger.info(f"Working directory: {os.getcwd()}")
    app.logger.info(f"Script location: {os.path.dirname(os.path.abspath(__file__))}")

log_system_info()

# Modify the initialization part
try:
    app.logger.info("Loading LED configuration...")
    config = LEDConfig.from_machine_config()
    app.logger.info(f"Configuration loaded: LED count={config.COUNT}, PIN={config.PIN}")
    controller = LEDController(config)
    app.logger.info('LED Controller initialized successfully')
except Exception as e:
    app.logger.error(f'Failed to initialize LED Controller: {str(e)}')
    app.logger.error(traceback.format_exc())
    sys.exit(1)

@app.route('/')
def index():
    app.logger.info('Homepage accessed')
    return render_template('index.html')

@app.route('/api/animation/<name>')
def run_animation(name):
    controller.stop_current_animation()
    try:
        app.logger.info(f'Running animation: {name}')
                
        if name == 'red':
            app.logger.info('Setting red color')
            for i in range(controller.strip.numPixels()):
                controller.strip.setPixelColor(i, ColorPreset.RED.color)
        elif name == 'green':
            app.logger.info('Setting green color')
            for i in range(controller.strip.numPixels()):
                controller.strip.setPixelColor(i, ColorPreset.GREEN.color)
        elif name == 'blue':
            app.logger.info('Setting blue color')
            for i in range(controller.strip.numPixels()):
                controller.strip.setPixelColor(i, ColorPreset.BLUE.color)
        controller.strip.show()

        # Handle animations
        if name == 'rainbow':
            app.logger.info('Starting rainbow animation')
            controller.start_animation(AnimationType.RAINBOW)
        elif name == 'fire':
            app.logger.info('Starting fire animation')
            controller.start_animation(AnimationType.FIRE)
        elif name == 'rainbow_cycle':
            app.logger.info('Starting rainbow cycle animation')
            controller.start_animation(AnimationType.RAINBOW_CYCLE)
        elif name == 'theater_chase_rainbow':
            app.logger.info('Starting theater chase rainbow animation')
            controller.start_animation(AnimationType.THEATER_CHASE_RAINBOW)
        # Handle control commands
        elif name == 'stop':
            app.logger.info('Stopping animation')
            controller.stop_current_animation()
        elif name == 'turn_off':
            app.logger.info('Turning off LEDs')
            controller.turn_off()
        elif name == 'turn_on':
            app.logger.info('Setting maximum brightness')
            controller.set_brightness(255)
            
        return jsonify({'status': 'success'})
    except Exception as e:
        app.logger.error(f'Error running animation {name}: {str(e)}')
        app.logger.error(traceback.format_exc())
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/brightness/<int:level>')
def set_brightness(level):
    try:
        controller.set_brightness(level)
        return jsonify({'status': 'success', 'brightness': level})
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/animation/custom_color/<int:r>/<int:g>/<int:b>')
def set_custom_color_rgb(r, g, b):
    try:
        app.logger.info(f'Setting custom color RGB: ({r}, {g}, {b})')
        controller.stop_current_animation()
        # Set the color directly like we do with static colors
        for i in range(controller.strip.numPixels()):
            controller.strip.setPixelColor(i, Color(r, g, b))
        controller.strip.show()
        app.logger.info('Custom color applied successfully')
        return jsonify({'status': 'success'})
    except Exception as e:
        app.logger.error(f'Error setting custom color: {str(e)}')
        app.logger.error(traceback.format_exc())
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/leds')
def get_leds():
    app.logger.info(f'Getting LEDs: {controller.get_leds()}')
    return jsonify({'status': 'success', 'leds': controller.get_leds()})

# @app.route('/api/test_color/<name>')
# def test_color(name):
#     try:
#         if name == 'red':
#             for i in range(controller.strip.numPixels()):
#                 controller.strip.setPixelColor(i, Color(255, 0, 0))
#         elif name == 'green':
#             for i in range(controller.strip.numPixels()):
#                 controller.strip.setPixelColor(i, Color(0, 255, 0))
#         elif name == 'blue':
#             for i in range(controller.strip.numPixels()):
#                 controller.strip.setPixelColor(i, Color(0, 0, 255))
#         controller.strip.show()
#         return jsonify({'status': 'success'})
#     except Exception as e:
#         app.logger.error(f'Error in test_color: {str(e)}')
#         return jsonify({'status': 'error', 'message': str(e)})

# Add cleanup handler
def cleanup():
    controller.cleanup()

# Register cleanup handler
import atexit
atexit.register(cleanup)

if __name__ == '__main__':
    # Make sure to run with sudo (only needed on Raspberry Pi with real hardware)
    using_mock = 'mock_rpi_ws281x' in sys.modules
    if not using_mock and os.geteuid() != 0:
        app.logger.error("This script must be run with sudo privileges")
        sys.exit(1)
    elif using_mock:
        app.logger.info("Running in development mode with mock hardware")
    
    app.run(host='0.0.0.0', port=5001) 