let NUM_LEDS = 0;
let ledStates = [];

// Add animation-related properties
let animationFrame = null;
let currentAnimation = null;

function initializeLEDStrip() {
    const ledStrip = document.getElementById('ledStrip');
    ledStrip.innerHTML = ''; // Clear existing LEDs
    
    // Create LED elements with enhanced features
    for (let i = 0; i < NUM_LEDS; i++) {
        const ledContainer = document.createElement('div');
        ledContainer.className = 'led-container';
        
        const led = document.createElement('div');
        led.className = 'led';
        led.id = `led-${i}`;
        led.setAttribute('data-index', i);
        
        // Add LED number indicator
        const ledNumber = document.createElement('div');
        ledNumber.className = 'led-number';
        ledNumber.textContent = i + 1;
        
        // Add click handler for individual LED control
        led.addEventListener('click', () => handleLEDClick(i));
        led.addEventListener('mouseenter', () => showLEDInfo(i));
        led.addEventListener('mouseleave', () => hideLEDInfo());
        
        ledContainer.appendChild(led);
        ledContainer.appendChild(ledNumber);
        ledStrip.appendChild(ledContainer);
    }
    
    // Add LED info tooltip
    createLEDInfoTooltip();
}

function createLEDInfoTooltip() {
    const tooltip = document.createElement('div');
    tooltip.id = 'led-tooltip';
    tooltip.className = 'led-tooltip';
    document.body.appendChild(tooltip);
}

function showLEDInfo(index) {
    const tooltip = document.getElementById('led-tooltip');
    const led = document.getElementById(`led-${index}`);
    const state = ledStates[index] || { r: 0, g: 0, b: 0 };
    
    if (tooltip && led) {
        const rect = led.getBoundingClientRect();
        tooltip.innerHTML = `
            <div class="tooltip-content">
                <div class="tooltip-header">LED ${index + 1}</div>
                <div class="tooltip-color">
                    <div class="color-preview" style="background: rgb(${state.r}, ${state.g}, ${state.b})"></div>
                    <div class="color-values">
                        <div>R: ${state.r}</div>
                        <div>G: ${state.g}</div>
                        <div>B: ${state.b}</div>
                    </div>
                </div>
            </div>
        `;
        
        tooltip.style.left = `${rect.left + rect.width / 2}px`;
        tooltip.style.top = `${rect.top - 10}px`;
        tooltip.style.opacity = '1';
        tooltip.style.visibility = 'visible';
    }
}

function hideLEDInfo() {
    const tooltip = document.getElementById('led-tooltip');
    if (tooltip) {
        tooltip.style.opacity = '0';
        tooltip.style.visibility = 'hidden';
    }
}

function handleLEDClick(index) {
    // Toggle individual LED or apply current color picker color
    const colorPicker = document.getElementById('colorPicker');
    if (colorPicker) {
        const hex = colorPicker.value;
        const rgb = hexToRgb(hex);
        
        // Update the specific LED
        if (!ledStates[index] || (ledStates[index].r === 0 && ledStates[index].g === 0 && ledStates[index].b === 0)) {
            ledStates[index] = rgb;
        } else {
            ledStates[index] = { r: 0, g: 0, b: 0 };
        }
        
        updateLEDDisplay();
        
        // Add visual feedback
        const led = document.getElementById(`led-${index}`);
        led.classList.add('clicked');
        setTimeout(() => led.classList.remove('clicked'), 200);
    }
}

function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : { r: 255, g: 0, b: 0 };
}

// Initialize LED controls
function initializeLEDControls() {
    const showNumbersBtn = document.getElementById('showNumbers');
    const clearAllBtn = document.getElementById('clearAll');
    const fillAllBtn = document.getElementById('fillAll');
    const randomizeBtn = document.getElementById('randomize');
    const ledStrip = document.getElementById('ledStrip');
    
    if (showNumbersBtn) {
        showNumbersBtn.addEventListener('click', () => {
            ledStrip.classList.toggle('show-numbers');
            showNumbersBtn.classList.toggle('active');
        });
    }
    
    if (clearAllBtn) {
        clearAllBtn.addEventListener('click', () => {
            ledStates = new Array(NUM_LEDS).fill({ r: 0, g: 0, b: 0 });
            updateLEDDisplay();
            
            // Visual feedback
            clearAllBtn.style.transform = 'scale(0.9)';
            setTimeout(() => {
                clearAllBtn.style.transform = '';
            }, 150);
        });
    }
    
    if (fillAllBtn) {
        fillAllBtn.addEventListener('click', () => {
            const colorPicker = document.getElementById('colorPicker');
            if (colorPicker) {
                const rgb = hexToRgb(colorPicker.value);
                ledStates = new Array(NUM_LEDS).fill(rgb);
                updateLEDDisplay();
                
                // Visual feedback
                fillAllBtn.style.transform = 'scale(0.9)';
                setTimeout(() => {
                    fillAllBtn.style.transform = '';
                }, 150);
            }
        });
    }
    
    if (randomizeBtn) {
        randomizeBtn.addEventListener('click', () => {
            ledStates = new Array(NUM_LEDS).fill().map(() => ({
                r: Math.floor(Math.random() * 256),
                g: Math.floor(Math.random() * 256),
                b: Math.floor(Math.random() * 256)
            }));
            updateLEDDisplay();
            
            // Visual feedback with longer animation
            randomizeBtn.style.transform = 'scale(0.9) rotate(180deg)';
            setTimeout(() => {
                randomizeBtn.style.transform = '';
            }, 300);
        });
    }
}

// Add LED pattern functions
function createPattern(patternType) {
    switch (patternType) {
        case 'gradient':
            return createGradientPattern();
        case 'alternating':
            return createAlternatingPattern();
        case 'chase':
            return createChasePattern();
        default:
            return ledStates;
    }
}

function createGradientPattern() {
    const colorPicker = document.getElementById('colorPicker');
    const startColor = colorPicker ? hexToRgb(colorPicker.value) : { r: 255, g: 0, b: 0 };
    const endColor = { r: 0, g: 0, b: 255 };
    
    return new Array(NUM_LEDS).fill().map((_, i) => {
        const ratio = i / (NUM_LEDS - 1);
        return {
            r: Math.round(startColor.r + (endColor.r - startColor.r) * ratio),
            g: Math.round(startColor.g + (endColor.g - startColor.g) * ratio),
            b: Math.round(startColor.b + (endColor.b - startColor.b) * ratio)
        };
    });
}

function createAlternatingPattern() {
    const colorPicker = document.getElementById('colorPicker');
    const color1 = colorPicker ? hexToRgb(colorPicker.value) : { r: 255, g: 0, b: 0 };
    const color2 = { r: 0, g: 255, b: 0 };
    
    return new Array(NUM_LEDS).fill().map((_, i) => 
        i % 2 === 0 ? color1 : color2
    );
}

function createChasePattern() {
    const colorPicker = document.getElementById('colorPicker');
    const activeColor = colorPicker ? hexToRgb(colorPicker.value) : { r: 255, g: 255, b: 255 };
    const offColor = { r: 0, g: 0, b: 0 };
    
    return new Array(NUM_LEDS).fill().map((_, i) => 
        i % 3 === 0 ? activeColor : offColor
    );
}

function updateLEDDisplay() {
    if (!ledStates || ledStates.length === 0) {
        console.error("LED states not properly initialized");
        return;
    }

    // If there's an active animation, don't update directly
    if (currentAnimation) return;

    ledStates.forEach((state, index) => {
        updateSingleLED(index, state);
    });
}

function updateSingleLED(index, state) {
    const led = document.getElementById(`led-${index}`);
    if (led && state && typeof state.r !== 'undefined') {
        const brightness = parseInt(document.getElementById('brightnessSlider')?.value || 255);
        const adjustedR = Math.round((state.r * brightness) / 255);
        const adjustedG = Math.round((state.g * brightness) / 255);
        const adjustedB = Math.round((state.b * brightness) / 255);
        
        const color = `rgb(${adjustedR}, ${adjustedG}, ${adjustedB})`;
        led.style.backgroundColor = color;
        led.style.color = color; // For the glow effect
        
        // Add/remove active class based on whether LED is on
        const isOn = adjustedR > 0 || adjustedG > 0 || adjustedB > 0;
        led.classList.toggle('active', isOn);
        
        // Calculate and apply intensity for realistic glow
        const intensity = (adjustedR + adjustedG + adjustedB) / 3;
        const glowIntensity = Math.min(intensity / 255, 1);
        
        if (isOn) {
            led.style.boxShadow = `
                inset 0 2px 4px rgba(0, 0, 0, 0.3),
                0 4px 15px rgba(0, 0, 0, 0.4),
                0 0 ${20 * glowIntensity}px ${color},
                0 0 ${40 * glowIntensity}px ${color}
            `;
        } else {
            led.style.boxShadow = `
                inset 0 2px 4px rgba(0, 0, 0, 0.5),
                0 2px 8px rgba(0, 0, 0, 0.3)
            `;
        }
    }
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
        updateSingleLED(index, state);
    });
}

// Export methods instead of values
export default {
    getNUM_LEDS,
    setNUM_LEDS,
    getLedStates,
    setLedStates,
    initializeLEDStrip,
    initializeLEDControls,
    updateLEDDisplay,
    updateSingleLED,
    isInitialized,
    startAnimation,
    stopAnimation,
    createPattern
};