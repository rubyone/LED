import ledPreviewController from './ledPreviewController.js';

function initializeBrightnessControl() {
    const brightnessSlider = document.getElementById('brightnessSlider');
    const brightnessValue = document.getElementById('brightnessValue');
    
    let lastUpdate = 0;
    brightnessSlider.addEventListener('input', (e) => {
        const now = Date.now();
        const value = e.target.value;
        brightnessValue.textContent = value;
        
        // Update LED display immediately for visual feedback
        ledPreviewController.updateLEDDisplay();
        
        // Throttle API calls
        if (now - lastUpdate > 50) {
            lastUpdate = now;
            fetch(`/api/brightness/${value}`)
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'error') {
                        alert('Error: ' + data.message);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error setting brightness');
                });
        }
    });
}

export { initializeBrightnessControl }; 