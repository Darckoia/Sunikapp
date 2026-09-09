const createBtn = document.getElementById('create');
const result = document.getElementById('result');
createBtn?.addEventListener('click', async () => {
  const payload = {
    prompt: document.getElementById('prompt').value,
    genre: document.getElementById('genre').value,
    duration: Number(document.getElementById('duration').value || 10),
    bpm: Number(document.getElementById('bpm').value || 120),
    scale: 'C Minor',
    instrumental_mode: true,
  };
  const r = await fetch('/api/v1/audio/generate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  result.textContent = JSON.stringify(await r.json(), null, 2);
});
