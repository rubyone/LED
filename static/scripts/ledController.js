let NUM_LEDS = 0; // Change from null to 0
let ledStates = []; // Change from null to empty array

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

// Add getter to check if initialized
function isInitialized() {
    return NUM_LEDS > 0; // Only check NUM_LEDS since ledStates can change
}

// Export as an object with all the values
export default {
    NUM_LEDS,
    ledStates,
    initializeLEDStrip,
    updateLEDDisplay,
    isInitialized,
    // Add setters for NUM_LEDS and ledStates
    setNUM_LEDS(value) {
        NUM_LEDS = value;
    },
    setLedStates(value) {
        ledStates = value;
    }
};
