// Settings functionality

function switchSettings(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.settings-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    
    // Remove active class from all links
    const links = document.querySelectorAll('.settings-link');
    links.forEach(link => {
        link.classList.remove('active');
    });
    
    // Show selected section
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.classList.add('active');
    }
    
    // Add active class to clicked link
    event.target.classList.add('active');
}
