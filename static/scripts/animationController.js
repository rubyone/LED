import ledPreviewController from './ledPreviewController.js';

let isLEDOn = true; // Track LED strip state
let lastActiveAnimation = null; // Track last active animation button
let lastAnimationName = null; // Track the name of the last animation
let isPlaying = true; // Add this to track play/pause state
let isInitialized = false;

function runAnimation(name, clickedButton) {
    if (!isInitialized && name !== 'turn_off') {
        console.error('LED Controller not initialized yet');
        return;
    }

    console.log(name);
    const pauseButton = document.querySelector('.control-btn.stop');

    // Stop any existing animation when changing modes
    ledPreviewController.stopAnimation();

    if (name === 'stop') {
        isPlaying = !isPlaying; // Toggle play state
        if (isPlaying) {
            // Resume last animation
            pauseButton.textContent = 'Pause';
            if (lastAnimationName) {
                fetch(`/api/animation/${lastAnimationName}`);
            }
        } else {
            // Pause current animation
            pauseButton.textContent = 'Play';
            fetch(`/api/animation/stop`);
        }
        return;
    }

    // Reset play state when starting a new animation
    if (name !== 'turn_off' && name !== 'turn_on') {
        isPlaying = true;
        pauseButton.textContent = 'Pause';
    }

    // Handle power state
    if (name === 'turn_off') {
        isLEDOn = false;
        // Store last active animation before turning off
        lastActiveAnimation = document.querySelector('.control-btn.active:not(.turn_on):not(.turn_off)');
        if (lastActiveAnimation) {
            lastAnimationName = lastActiveAnimation.getAttribute('onclick').match(/'([^']+)'/)[1];
        }
        
        // Set brightness to 0
        const brightnessSlider = document.getElementById('brightnessSlider');
        const brightnessValue = document.getElementById('brightnessValue');
        brightnessSlider.value = 0;
        brightnessValue.textContent = 0;
        fetch('/api/brightness/0');

        // Update button states
        document.querySelectorAll('.control-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector('.control-btn.turn_off').classList.add('active');
        document.querySelector('.control-btn.turn_on').classList.remove('active');
        
        // Set all LEDs to black and stop any running animations
        ledPreviewController.stopAnimation();
        const blackState = { r: 0, g: 0, b: 0 };
        ledPreviewController.setLedStates(new Array(ledPreviewController.getNUM_LEDS()).fill(blackState));
        ledPreviewController.updateLEDDisplay();

    } else if (name === 'turn_on') {
        isLEDOn = true;
        // Restore brightness to previous value
        const brightnessSlider = document.getElementById('brightnessSlider');
        const brightnessValue = document.getElementById('brightnessValue');
        brightnessSlider.value = 255;
        brightnessValue.textContent = 255;
        fetch('/api/brightness/255');
        
        // Update button states
        document.querySelector('.control-btn.turn_on').classList.add('active');
        document.querySelector('.control-btn.turn_off').classList.remove('active');
        
        // Restore last active animation if there was one
        if (lastActiveAnimation && lastAnimationName) {
            lastActiveAnimation.classList.add('active');
            
            // Restore the animation preview
            if (['rainbow', 'rainbow_cycle', 'fire', 'theater_chase_rainbow'].includes(lastAnimationName)) {
                ledPreviewController.startAnimation(lastAnimationName);
            } else {
                // For static colors
                let color;
                switch (lastAnimationName) {
                    case 'red':
                        color = { r: 255, g: 0, b: 0 };
                        break;
                    case 'green':
                        color = { r: 0, g: 255, b: 0 };
                        break;
                    case 'blue':
                        color = { r: 0, g: 0, b: 255 };
                        break;
                    default:
                        color = { r: 255, g: 255, b: 255 };
                }
                ledPreviewController.setLedStates(new Array(ledPreviewController.getNUM_LEDS()).fill(color));
                ledPreviewController.updateLEDDisplay();
            }

            fetch(`/api/animation/${lastAnimationName}`)
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'error') {
                        alert('Error: ' + data.message);
                        lastActiveAnimation.classList.remove('active');
                        lastActiveAnimation = null;
                        lastAnimationName = null;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error running animation');
                    lastActiveAnimation.classList.remove('active');
                    lastActiveAnimation = null;
                    lastAnimationName = null;
                });
            return;
        }
    } else if (name === 'stop') {
        lastActiveAnimation = null;
        lastAnimationName = null;
        // Remove active class from animation/color buttons but keep power state
        document.querySelectorAll('.control-btn:not(.turn_on):not(.turn_off)').forEach(btn => {
            btn.classList.remove('active');
        });

    } else {
        // Handle animations
        switch (name) {
            case 'rainbow':
            case 'rainbow_cycle':
            case 'fire':
            case 'theater_chase_rainbow':
                ledPreviewController.startAnimation(name);
                break;
            case 'red':
                ledPreviewController.setLedStates(new Array(ledPreviewController.getNUM_LEDS()).fill({ r: 255, g: 0, b: 0 }));
                ledPreviewController.updateLEDDisplay();
                break;
            case 'green':
                ledPreviewController.setLedStates(new Array(ledPreviewController.getNUM_LEDS()).fill({ r: 0, g: 255, b: 0 }));
                ledPreviewController.updateLEDDisplay();
                break;
            case 'blue':
                ledPreviewController.setLedStates(new Array(ledPreviewController.getNUM_LEDS()).fill({ r: 0, g: 0, b: 255 }));
                ledPreviewController.updateLEDDisplay();
                break;
            case 'turn_off':
                ledPreviewController.setLedStates(new Array(ledPreviewController.getNUM_LEDS()).fill({ r: 0, g: 0, b: 0 }));
                ledPreviewController.updateLEDDisplay();
                break;
        }
    }

    // Update button states for animations and colors
    if (name !== 'turn_off' && name !== 'stop') {
        // Remove active class from other animation/color buttons
        document.querySelectorAll('.control-btn:not(.turn_on):not(.turn_off)').forEach(btn => {
            btn.classList.remove('active');
        });
        if (clickedButton) {
            clickedButton.classList.add('active');
        }
        // Make sure "on" button is active for colors and animations
        if (name !== 'turn_on') {
            document.querySelector('.control-btn.turn_on').classList.add('active');
            document.querySelector('.control-btn.turn_off').classList.remove('active');
            lastActiveAnimation = clickedButton;
            lastAnimationName = name;
        }
    }
    
    // Send animation command to API
    fetch(`/api/animation/${name}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'error') {
                alert('Error: ' + data.message);
                clickedButton.classList.remove('active');
                if (clickedButton === lastActiveAnimation) {
                    lastActiveAnimation = null;
                    lastAnimationName = null;
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error running animation');
            clickedButton.classList.remove('active');
            if (clickedButton === lastActiveAnimation) {
                lastActiveAnimation = null;
                lastAnimationName = null;
            }
        });
        
}

function initializeAnimationController() {
    isInitialized = true;
}

export { runAnimation, initializeAnimationController };