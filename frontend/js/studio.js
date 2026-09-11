// Studio functionality

const frequencyInput = document.getElementById('frequency');
const frequencyValue = document.getElementById('frequencyValue');
const durationInput = document.getElementById('duration');
const playBtn = document.getElementById('playBtn');
const stopBtn = document.getElementById('stopBtn');
const playbackPosition = document.getElementById('playbackPosition');
const playbackTime = document.getElementById('playbackTime');

// Update frequency display
if (frequencyInput) {
    frequencyInput.addEventListener('input', (e) => {
        frequencyValue.textContent = e.target.value;
    });
}

// Generate audio function
async function generateAudio() {
    const frequency = parseFloat(frequencyInput.value);
    const duration = parseFloat(durationInput.value);
    
    console.log(`Generating audio: ${frequency}Hz for ${duration}s`);
    
    // Call API to generate audio
    try {
        const response = await fetch('/api/v1/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                frequency: frequency,
                duration: duration,
                type: 'sine'
            })
        });
        
        if (response.ok) {
            console.log('Audio generated successfully');
        }
    } catch (error) {
        console.error('Error generating audio:', error);
    }
}

// Export functions
function exportWAV() {
    console.log('Exporting as WAV...');
    // Implementation for WAV export
}

function exportMP3() {
    console.log('Exporting as MP3...');
    // Implementation for MP3 export
}

// Add track function
function addTrack() {
    console.log('Adding new track...');
    // Implementation for adding tracks
}

// Playback controls
if (playBtn) {
    playBtn.addEventListener('click', () => {
        console.log('Playing audio...');
    });
}

if (stopBtn) {
    stopBtn.addEventListener('click', () => {
        console.log('Stopping audio...');
    });
}
