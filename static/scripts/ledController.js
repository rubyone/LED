let NUM_LEDS = 0;
let ledStates = [];

// Add animation-related properties
let animationFrame = null;
let currentAnimation = null;

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

    // If there's an active animation, don't update directly
    if (currentAnimation) return;

    ledStates.forEach((state, index) => {
        const led = document.getElementById(`led-${index}`);
        if (led) {
            if (state && typeof state.r !== 'undefined') {
                led.style.backgroundColor = `rgb(${state.r}, ${state.g}, ${state.b})`;
                const brightness = parseInt(document.getElementById('brightnessSlider').value);
                led.style.opacity = brightness / 255;
            }
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

// Add animation functions
function wheel(pos) {
    pos = pos % 256;
    if (pos < 85) {
        return { r: pos * 3, g: 255 - pos * 3, b: 0 };
    } else if (pos < 170) {
        pos -= 85;
        return { r: 255 - pos * 3, g: 0, b: pos * 3 };
    } else {
        pos -= 170;
        return { r: 0, g: pos * 3, b: 255 - pos * 3 };
    }
}

function startAnimation(type) {
    // Stop any existing animation
    stopAnimation();
    
    currentAnimation = type;
    let step = 0;

    const animate = () => {
        if (!currentAnimation) return;

        switch (type) {
            case 'rainbow':
                rainbowStep(step);
                break;
            case 'rainbow_cycle':
                rainbowCycleStep(step);
                break;
            case 'fire':
                fireStep();
                break;
            case 'theater_chase_rainbow':
                theaterChaseRainbowStep(step);
                break;
        }

        step = (step + 1) % 256;
        animationFrame = requestAnimationFrame(animate);
    };

    animate();
}

function stopAnimation() {
    if (animationFrame) {
        cancelAnimationFrame(animationFrame);
        animationFrame = null;
    }
    currentAnimation = null;
}

// Animation step functions
function rainbowStep(step) {
    const color = wheel(step);
    ledStates = new Array(NUM_LEDS).fill(color);
    updateLEDsWithStates();
}

function rainbowCycleStep(step) {
    ledStates = ledStates.map((_, i) => {
        const pos = ((i * 256 / NUM_LEDS) + step) % 256;
        return wheel(pos);
    });
    updateLEDsWithStates();
}

function fireStep() {
    ledStates = ledStates.map(() => {
        const flicker = Math.random() * 55;
        return {
            r: 255 - flicker,
            g: 35,
            b: 0
        };
    });
    updateLEDsWithStates();
}

function theaterChaseRainbowStep(step) {
    const q = Math.floor(step / 3) % 3;
    ledStates = ledStates.map((_, i) => {
        if ((i + q) % 3 === 0) {
            return wheel((i + step) % 255);
        }
        return { r: 0, g: 0, b: 0 };
    });
    updateLEDsWithStates();
}

function updateLEDsWithStates() {
    ledStates.forEach((state, index) => {
        const led = document.getElementById(`led-${index}`);
        if (led) {
            led.style.backgroundColor = `rgb(${state.r}, ${state.g}, ${state.b})`;
            const brightness = parseInt(document.getElementById('brightnessSlider').value);
            led.style.opacity = brightness / 255;
        }
    });
}

// Export methods instead of values
export default {
    getNUM_LEDS,
    setNUM_LEDS,
    getLedStates,
    setLedStates,
    initializeLEDStrip,
    updateLEDDisplay,
    isInitialized,
    startAnimation,
    stopAnimation
};
