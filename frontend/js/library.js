// Library functionality

const searchInput = document.getElementById('searchInput');
const sortBy = document.getElementById('sortBy');
const tracksGrid = document.getElementById('tracksGrid');
const emptyState = document.getElementById('emptyState');

// Sample tracks data
let tracks = [
    {
        id: 1,
        title: 'First Track',
        duration: 120,
        created: '2 hours ago',
        project: 'Project 1'
    },
    {
        id: 2,
        title: 'Second Track',
        duration: 180,
        created: '5 hours ago',
        project: 'Project 2'
    }
];

// Render tracks
function renderTracks(tracksToRender) {
    tracksGrid.innerHTML = '';
    
    if (tracksToRender.length === 0) {
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    
    tracksToRender.forEach(track => {
        const trackCard = document.createElement('div');
        trackCard.className = 'track-card';
        trackCard.innerHTML = `
            <div class="track-card-header">
                <div class="track-card-title">${track.title}</div>
                <div class="track-card-meta">${track.project}</div>
            </div>
            <div class="track-card-body">
                <div class="track-waveform"></div>
                <div class="track-card-meta">Duration: ${track.duration}s</div>
                <div class="track-card-meta">${track.created}</div>
            </div>
            <div class="track-card-actions">
                <button class="btn btn-small btn-primary">Play</button>
                <button class="btn btn-small">Download</button>
            </div>
        `;
        tracksGrid.appendChild(trackCard);
    });
}

// Search functionality
if (searchInput) {
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        const filtered = tracks.filter(track => 
            track.title.toLowerCase().includes(query)
        );
        renderTracks(filtered);
    });
}

// Sort functionality
if (sortBy) {
    sortBy.addEventListener('change', (e) => {
        const sorted = [...tracks];
        switch (e.target.value) {
            case 'name':
                sorted.sort((a, b) => a.title.localeCompare(b.title));
                break;
            case 'duration':
                sorted.sort((a, b) => a.duration - b.duration);
                break;
            case 'recent':
            default:
                // Keep original order
                break;
        }
        renderTracks(sorted);
    });
}

// Initial render
renderTracks(tracks);
