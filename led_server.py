from flask import Flask, render_template, jsonify
from LED1 import LEDController
from rpi_ws281x import Color

app = Flask(__name__)
controller = LEDController()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/animation/<name>')
def run_animation(name):
    try:
        if name == 'red':
            controller.colorWipe(Color(255, 0, 0))
        elif name == 'green':
            controller.colorWipe(Color(0, 255, 0))
        elif name == 'blue':
            controller.colorWipe(Color(0, 0, 255))
        elif name == 'rainbow':
            controller.start_animation(controller.rainbow)
        elif name == 'rainbow_cycle':
            controller.start_animation(controller.rainbowCycle)
        elif name == 'theater_chase':
            controller.start_animation(controller.theaterChase, Color(127, 127, 127))
        elif name == 'theater_chase_rainbow':
            controller.start_animation(controller.theaterChaseRainbow)
        elif name == 'stop':
            controller.stop_animation = True
        return jsonify({'status': 'success'})
    except Exception as e:
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