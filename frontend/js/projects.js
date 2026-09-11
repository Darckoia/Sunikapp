// Projects functionality

const projectsGrid = document.getElementById('projectsGrid');
const emptyState = document.getElementById('emptyState');

// Sample projects data
let projects = [
    {
        id: 1,
        name: 'Electronic Album',
        description: 'A collection of electronic music tracks',
        tracks: 12,
        modified: 'Today'
    },
    {
        id: 2,
        name: 'Sound Design',
        description: 'Experimental sound design project',
        tracks: 8,
        modified: 'Yesterday'
    }
];

// Render projects
function renderProjects(projectsToRender) {
    projectsGrid.innerHTML = '';
    
    if (projectsToRender.length === 0) {
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    
    projectsToRender.forEach(project => {
        const projectCard = document.createElement('div');
        projectCard.className = 'project-card';
        projectCard.innerHTML = `
            <div class="project-icon">🎵</div>
            <div class="project-name">${project.name}</div>
            <div class="project-description">${project.description}</div>
            <div class="project-footer">
                <span>${project.tracks} tracks</span>
                <div class="project-actions">
                    <button class="btn btn-small" title="Edit">✏️</button>
                    <button class="btn btn-small" title="Delete">🗑️</button>
                </div>
            </div>
        `;
        projectsGrid.appendChild(projectCard);
    });
}

// Create new project
function createNewProject() {
    const name = prompt('Enter project name:', 'New Project');
    if (name) {
        const newProject = {
            id: projects.length + 1,
            name: name,
            description: 'New project',
            tracks: 0,
            modified: 'Now'
        };
        projects.push(newProject);
        renderProjects(projects);
    }
}

// Initial render
renderProjects(projects);
