from flask import Flask, render_template, jsonify
import logging
from logging.handlers import RotatingFileHandler
from LED1 import LEDController
from rpi_ws281x import Color

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
handler = RotatingFileHandler('/var/log/led-server.log', maxBytes=10000, backupCount=3)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)
app.logger.info('LED Server startup')

controller = LEDController()

@app.route('/')
def index():
    app.logger.info('Homepage accessed')
    return render_template('index.html')

@app.route('/api/animation/<name>')
def run_animation(name):
    try:
        app.logger.info(f'Running animation: {name}')
        if name == 'red':
            controller.stop_animation = True
            controller.colorWipe(Color(255, 0, 0))
        elif name == 'green':
            controller.stop_animation = True
            controller.colorWipe(Color(0, 255, 0))
        elif name == 'blue':
            controller.stop_animation = True
            controller.colorWipe(Color(0, 0, 255))
        elif name == 'rainbow':
            controller.start_animation(controller.rainbow)
        elif name == 'fire':
            controller.start_animation(controller.fire_effect)
        elif name == 'rainbow_cycle':
            controller.start_animation(controller.rainbowCycle)
        elif name == 'theater_chase_rainbow':
            controller.start_animation(controller.theaterChaseRainbow)
        elif name == 'stop':
            controller.stop_animation = True
        elif name == 'turn_off':
            controller.turn_off()
        elif name == 'turn_on':
            controller.set_brightness(255)
        return jsonify({'status': 'success'})
    except Exception as e:
        app.logger.error(f'Error running animation {name}: {str(e)}')
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/brightness/<int:level>')
def set_brightness(level):
    try:
        controller.set_brightness(level)
        return jsonify({'status': 'success', 'brightness': level})
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 