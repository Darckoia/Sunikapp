# Host Streamlit Cloud + UI HTML (se ve como Suno).
# requirements.txt:
# streamlit>=1.36.0

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Suno", layout="centered", initial_sidebar_state="collapsed")
st.markdown(
    """
<style>
#MainMenu, footer, header, .stDeployButton, [data-testid="stToolbar"] {display:none!important;}
.stApp { background:#121212; }
.block-container { padding:0 !important; max-width:430px !important; }
</style>
""",
    unsafe_allow_html=True,
)

HTML = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
  * { box-sizing:border-box; margin:0; padding:0; }
  body { font-family: Inter, Segoe UI, Helvetica, Arial, sans-serif; background:#121212; color:#f5f5f5; }
  .wrap { max-width:430px; margin:0 auto; padding:12px 16px 96px; }
  header { display:flex; justify-content:space-between; align-items:center; padding:8px 0 16px; }
  .logo { font-weight:800; letter-spacing:.28em; font-size:15px; }
  .chip { background:#2a2a2e; border-radius:999px; padding:5px 10px; font-size:12px; }
  h1 { font-size:34px; font-weight:800; margin:0 0 16px; }
  .modes { display:flex; background:#1a1a1d; border:1px solid #2a2a2e; border-radius:999px; padding:4px; margin-bottom:14px; }
  .modes button { flex:1; border:0; background:transparent; color:#a1a1aa; padding:8px 6px; border-radius:999px; font-weight:600; }
  .modes button.on { background:#3f3f46; color:#fff; }
  .ver { font-size:13px; color:#d4d4d8; padding:8px 10px; }
  .card { background:#18181b; border:1px solid #2a2a2e; border-radius:16px; padding:12px; margin:10px 0; }
  .lab { font-size:13px; color:#a1a1aa; margin-bottom:8px; display:flex; justify-content:space-between; }
  textarea, input, select {
    width:100%; background:#0f0f12; color:#eee; border:1px solid #3f3f46;
    border-radius:12px; padding:10px 12px; font: inherit;
  }
  textarea { min-height:78px; resize:vertical; }
  .tags span { display:inline-block; background:#27272a; border:1px solid #3f3f46; border-radius:999px; padding:4px 8px; font-size:11px; margin:4px 4px 0 0; }
  .create {
    width:100%; margin-top:12px; border:0; border-radius:999px; padding:14px;
    font-weight:800; color:#fff; font-size:16px;
    background:linear-gradient(90deg,#ec4899,#f97316,#eab308);
  }
  .take { background:#18181b; border:1px solid #2a2a2e; border-radius:14px; padding:12px; margin-top:10px; }
  .muted { color:#a1a1aa; font-size:12px; }
  .player {
    position:fixed; left:0; right:0; bottom:0; max-width:430px; margin:0 auto;
    background:#18181b; border-top:1px solid #2a2a2e; padding:10px 16px 14px;
    display:flex; gap:10px; align-items:center;
  }
  .cover { width:40px; height:40px; border-radius:8px; background:#3f3f46; }
  .hidden { display:none; }
  .opt { background:#0f0f12; border:1px solid #2a2a2e; border-radius:12px; padding:10px 12px; margin-top:8px; font-size:13px; color:#a1a1aa; display:flex; justify-content:space-between; }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="logo">SUNO</div>
    <div class="chip" id="chip">Free · 50</div>
  </header>
  <h1>Create</h1>
  <div class="modes">
    <button class="on" id="mSimple" onclick="setMode('simple')">Simple</button>
    <button id="mCustom" onclick="setMode('custom')">Advanced</button>
    <div class="ver">v5.5</div>
  </div>

  <div id="pSimple">
    <div class="card">
      <div class="lab"><span>Styles</span></div>
      <textarea id="stylesS" placeholder="Resistente, tambores ligeros, rap afro, dizi, hueco"></textarea>
      <div class="tags"><span>resiliente</span><span>tambores</span></div>
    </div>
    <div class="card">
      <div class="lab"><span>Lyrics</span></div>
      <textarea id="lyricsS" placeholder="Start writing the lyrics, or leave this blank for the instrumental part."></textarea>
    </div>
  </div>

  <div id="pCustom" class="hidden">
    <div class="card">
      <div class="lab"><span>Title</span></div>
      <input id="titleC" value="Midnight Rain">
    </div>
    <div class="card">
      <div class="lab"><span>Styles</span></div>
      <textarea id="stylesC">dark synth pop, analog bass, intimate female vocal</textarea>
    </div>
    <div class="card">
      <div class="lab"><span>Lyrics</span></div>
      <textarea id="lyricsC">[Verse]
...
[Chorus]
...</textarea>
    </div>
    <div class="card">
      <div class="lab"><span>More options</span></div>
      <div class="opt">Exclude styles <input id="ex" placeholder="country" style="max-width:55%"></div>
      <div class="opt">Vocal gender
        <select id="vg" style="max-width:45%"><option>Auto</option><option>Male</option><option>Female</option></select>
      </div>
      <div class="opt">Weirdness <input id="w" type="range" min="0" max="100" value="50" style="max-width:45%"></div>
      <div class="opt">Style influence <input id="si" type="range" min="0" max="100" value="70" style="max-width:45%"></div>
    </div>
  </div>

  <button class="create" onclick="create()">Create</button>
  <div id="out"></div>
</div>
<div class="player">
  <div class="cover"></div>
  <div>
    <div id="np" style="font-size:13px;font-weight:600">Nada en cola</div>
    <div class="muted">Suno clone · demo local</div>
  </div>
</div>
<script>
let credits = 50, mode = 'simple';
function setMode(m){
  mode = m;
  document.getElementById('mSimple').className = m==='simple' ? 'on' : '';
  document.getElementById('mCustom').className = m==='custom' ? 'on' : '';
  document.getElementById('pSimple').className = m==='simple' ? '' : 'hidden';
  document.getElementById('pCustom').className = m==='custom' ? '' : 'hidden';
}
function create(){
  const style = mode==='simple' ? document.getElementById('stylesS').value : document.getElementById('stylesC').value;
  const lyrics = mode==='simple' ? document.getElementById('lyricsS').value : document.getElementById('lyricsC').value;
  const title = mode==='simple' ? 'Untitled' : (document.getElementById('titleC').value || 'Untitled');
  if(!style && !lyrics){ alert('Escribe styles o lyrics'); return; }
  if(credits < 10){ alert('Sin creditos'); return; }
  credits -= 10;
  document.getElementById('chip').textContent = 'Free · ' + credits;
  document.getElementById('np').textContent = title + ' (Take A)';
  document.getElementById('out').innerHTML =
    take(title,'A',style||lyrics) + take(title,'B',style||lyrics);
}
function take(title,tag,style){
  return '<div class="take"><b>'+title+' ('+tag+')</b><div class="muted">v5.5 · '+mode+' · demo</div><div class="muted">'+style+'</div></div>';
}
</script>
</body>
</html>
"""

components.html(HTML, height=780, scrolling=True)
