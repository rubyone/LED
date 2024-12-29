let NUM_LEDS = null; // Adjust this to match your actual LED strip length
let ledStates = null;

function initializeLEDStrip() {
    const ledStrip = document.getElementById('ledStrip');
    ledStrip.innerHTML = ''; // Clear existing LEDs
    
    // Create LED elements
    for (let i = 0; i < NUM_LEDS; i++) {
        const led = document.createElement('div');
        led.className = 'led';
        led.id = `led-${i}`;
        ledStrip.appendChild(led);
    }
}

function updateLEDDisplay() {
    ledStates.forEach((state, index) => {
        const led = document.getElementById(`led-${index}`);
        if (led) {
            led.style.backgroundColor = `rgb(${state.r}, ${state.g}, ${state.b})`;
            // Adjust brightness
            const brightness = parseInt(document.getElementById('brightnessSlider').value);
            led.style.opacity = brightness / 255;
        }
    });
}

// Export as an object with all the values
export default {
    NUM_LEDS,
    ledStates,
    initializeLEDStrip,
    updateLEDDisplay,
    // Add setters for NUM_LEDS and ledStates
    setNUM_LEDS(value) {
        NUM_LEDS = value;
    },
    setLedStates(value) {
        ledStates = value;
    }
};
