import ledPreviewController from './ledPreviewController.js';
import { initializeBrightnessControl } from './brightnessController.js';
import { initializeColorPicker } from './colorPicker.js';
import { initializeAnimationController } from './animationController.js';

document.addEventListener('DOMContentLoaded', () => {
    // Fetch LED count and initialize
    fetch('/api/leds') 
        .then(response => response.json())
        .then(data => {
            if (data.status === 'error') {
                console.error('Error:', data.message);
                return;
            }
            console.log('Number of LEDs:', data.leds);
            ledPreviewController.setNUM_LEDS(data.leds);
            
            // Initialize with black color
            const initialStates = new Array(data.leds).fill().map(() => ({r: 0, g: 0, b: 0}));
            ledPreviewController.setLedStates(initialStates);
            
            // Initialize the LED strip
            ledPreviewController.initializeLEDStrip();
            
            // Initialize all controllers
            initializeBrightnessControl();
            initializeColorPicker();
            initializeAnimationController();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error getting LED count');
        });
});
