const list = document.getElementById('projects');
const btn = document.getElementById('createProject');
async function refresh() {
  const r = await fetch('/api/v1/projects');
  const projects = await r.json();
  list.innerHTML = projects.map(p => `<li>${p.name}</li>`).join('');
}
btn?.addEventListener('click', async () => {
  await fetch('/api/v1/projects', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ name: document.getElementById('projectName').value || 'New project' })});
  await refresh();
});
refresh();
