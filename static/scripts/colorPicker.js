import ledController from './ledController.js';

function hexToRGB(hex) {
    hex = hex.replace('#', '');
    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);
    return { r, g, b };
}

function initializeColorPicker() {
    const colorPicker = document.getElementById('colorPicker');
    colorPicker.addEventListener('input', (e) => {
        const rgb = hexToRGB(e.target.value);
        ledController.setLedStates(new Array(ledController.NUM_LEDS).fill(rgb));
        ledController.updateLEDDisplay();
    });
}

export { hexToRGB, initializeColorPicker };
