import ledController from './ledPreviewController.js';

function hexToRGB(hex) {
    hex = hex.replace('#', '');
    const r = parseInt(hex.substring(0, 2), 16);
    const g = parseInt(hex.substring(2, 4), 16);
    const b = parseInt(hex.substring(4, 6), 16);
    return { r, g, b };
}

function initializeColorPicker() {
    const colorPicker = document.getElementById('colorPicker');
    
    // Update preview while picking color
    colorPicker.addEventListener('input', (e) => {
        if (!ledController.isInitialized()) {
            console.error('LED Controller not initialized yet');
            return;
        }
        const rgb = hexToRGB(e.target.value);    
        
        // Create new array with the color
        const newStates = new Array(ledController.getNUM_LEDS()).fill().map(() => ({...rgb}));
        ledController.setLedStates(newStates);
        ledController.updateLEDDisplay();

        // Send the RGB values to the API
        fetch(`/api/animation/custom_color/${rgb.r}/${rgb.g}/${rgb.b}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'error') {
                    alert('Error: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error setting custom color');
            });

        // Remove active class from animation/color buttons but keep power state
        document.querySelectorAll('.control-btn:not(.turn_on):not(.turn_off)').forEach(btn => {
            btn.classList.remove('active');
        });
    });
}

export { hexToRGB, initializeColorPicker };
