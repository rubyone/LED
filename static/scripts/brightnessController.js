import ledController from './ledController.js';

function initializeBrightnessControl() {
    const brightnessSlider = document.getElementById('brightnessSlider');
    const brightnessValue = document.getElementById('brightnessValue');
    
    let lastUpdate = 0;
    brightnessSlider.addEventListener('input', (e) => {
        const now = Date.now();
        const value = e.target.value;
        brightnessValue.textContent = value;
        
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

    // Update LED display when brightness changes
    brightnessSlider.addEventListener('input', ledController.updateLEDDisplay);
}

export { initializeBrightnessControl }; 