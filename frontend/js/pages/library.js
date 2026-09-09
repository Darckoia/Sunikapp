(async () => {
  const el = document.getElementById('tracks');
  const r = await fetch('/api/v1/tracks');
  const tracks = await r.json();
  el.innerHTML = tracks.map(t => `<li>${t.title} · ${t.genre} · ${t.bpm} BPM</li>`).join('');
})();
