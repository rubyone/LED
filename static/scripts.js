let isLEDOn = true; // Track LED strip state
let lastActiveAnimation = null; // Track last active animation button
let lastAnimationName = null; // Track the name of the last animation
let isPlaying = true; // Add this to track play/pause state

function runAnimation(name) {
    console.log(name);
    const pauseButton = document.querySelector('.control-btn.stop');

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
        
    } else if (name === 'turn_on') {
        isLEDOn = true;
        // Restore brightness to previous value
        const brightnessSlider = document.getElementById('brightnessSlider');
        const brightnessValue = document.getElementById('brightnessValue');
        brightnessSlider.value = 255; // Or store previous brightness value
        brightnessValue.textContent = 255;
        fetch('/api/brightness/255');

        // Update button states
        document.querySelector('.control-btn.turn_on').classList.add('active');
        document.querySelector('.control-btn.turn_off').classList.remove('active');
        
        // Restore last active animation if there was one
        if (lastActiveAnimation && lastAnimationName) {
            lastActiveAnimation.classList.add('active');
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
        // For colors and animations

        if (!isLEDOn) {
            // If LED is off, turn it on first
            isLEDOn = true;
            document.querySelector('.control-btn.turn_on').classList.add('active');
            document.querySelector('.control-btn.turn_off').classList.remove('active');
            
            // Restore brightness
            const brightnessSlider = document.getElementById('brightnessSlider');
            const brightnessValue = document.getElementById('brightnessValue');
            brightnessSlider.value = 255;
            brightnessValue.textContent = 255;
            fetch('/api/brightness/255');
        }
    }

    // Update button states for animations and colors
    const clickedButton = event.currentTarget;
    
    if (name !== 'turn_off' && name !== 'stop') {
        // Remove active class from other animation/color buttons
        document.querySelectorAll('.control-btn:not(.turn_on):not(.turn_off)').forEach(btn => {
            btn.classList.remove('active');
        });
        clickedButton.classList.add('active');
        // Make sure "on" button is active for colors and animations
        if (name !== 'turn_on') {
            document.querySelector('.control-btn.turn_on').classList.add('active');
            document.querySelector('.control-btn.turn_off').classList.remove('active');
            lastActiveAnimation = clickedButton;
            lastAnimationName = name;
        }
    }
    
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

// Brightness control
document.addEventListener('DOMContentLoaded', () => {
    const brightnessSlider = document.getElementById('brightnessSlider');
    const brightnessValue = document.getElementById('brightnessValue');
    
    // Add throttling for smoother performance
    let lastUpdate = 0;
    brightnessSlider.addEventListener('input', (e) => {
        const now = Date.now();
        const value = e.target.value;
        brightnessValue.textContent = value;
        
        // Only update if 50ms have passed since last update
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
}); 