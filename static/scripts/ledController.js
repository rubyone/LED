let NUM_LEDS = 0;
let ledStates = [];

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
    
    if (!ledStates || ledStates.length === 0) {
        console.error("LED states not properly initialized");
        return;
    }

    ledStates.forEach((state, index) => {
        const led = document.getElementById(`led-${index}`);
        if (led) {
            if (state && typeof state.r !== 'undefined') {
                led.style.backgroundColor = `rgb(${state.r}, ${state.g}, ${state.b})`;
                const brightness = parseInt(document.getElementById('brightnessSlider').value);
                led.style.opacity = brightness / 255;
            } else {
                console.error(`Invalid LED state for index ${index}:`, state);
            }
        } else {
            console.error(`LED element not found for index ${index}`);
        }
    });
}

function isInitialized() {
    return NUM_LEDS > 0;
}

function getLedStates() {
    return ledStates;
}

function setLedStates(value) {
    ledStates = [...value]; // Create a new array to ensure proper update
}

function getNUM_LEDS() {
    return NUM_LEDS;
}

function setNUM_LEDS(value) {
    NUM_LEDS = value;
}

// Export methods instead of values
export default {
    getNUM_LEDS,
    setNUM_LEDS,
    getLedStates,
    setLedStates,
    initializeLEDStrip,
    updateLEDDisplay,
    isInitialized
};
