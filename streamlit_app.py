import streamlit as st
import time

st.set_page_config(
    page_title="Suno Create",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    .stApp {
        background-color: #0c0d12 !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    header, footer, #MainMenu { visibility: hidden !important; }
    
    .suno-topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 20px;
        background-color: #0c0d12;
        border-bottom: 1px solid #1f2029;
        position: sticky;
        top: 0;
        z-index: 999;
    }
    
    .suno-logo {
        font-weight: 800;
        font-size: 1.3rem;
        letter-spacing: -0.5px;
        color: #ffffff;
    }
    
    .suno-credits {
        background-color: #1a1b24;
        border: 1px solid #2a2b38;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        color: #a1a1aa;
    }

    .create-container {
        background-color: #13141d;
        border: 1px solid #1f2029;
        border-radius: 16px;
        padding: 20px;
        margin: 16px 0;
    }

    .section-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }

    /* Estilización de inputs para que parezcan idénticos a Suno */
    stTextInput input, stTextArea textarea {
        background-color: #1a1b24 !important;
        color: #ffffff !important;
        border: 1px solid #2a2b38 !important;
        border-radius: 10px !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 14px 0px !important;
        width: 100%;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
        margin-top: 10px;
    }

    .suno-card {
        background-color: #13141d;
        border: 1px solid #1f2029;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
        display: flex;
        gap: 14px;
        align-items: center;
    }

    .cover-box {
        width: 64px;
        height: 64px;
        border-radius: 8px;
        background: linear-gradient(135deg, #3b82f6, #ec4899);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        flex-shrink: 0;
    }

    .bottom-player {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #13141d;
        border-top: 1px solid #1f2029;
        padding: 12px 20px;
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
</style>
""", unsafe_allow_html=True)

if "feed" not in st.session_state:
    st.session_state.feed = [
        {"title": "Esquinas Oscuras", "version": "v5.5 • Part 1", "style": "Chilean Trap, 95 BPM", "duration": "3:24"},
        {"title": "Esquinas Oscuras", "version": "v5.5 • Part 2", "style": "Chilean Trap, Heavy Bass", "duration": "3:12"}
    ]

# Barra Superior Suno
st.markdown("""
<div class='suno-topbar'>
    <div class='suno-logo'>suno <span style='color:#6366f1; font-size:0.75rem;'>CREATE</span></div>
    <div class='suno-credits'>⚡ 2,500 Credits</div>
</div>
""", unsafe_allow_html=True)

# Panel Principal de Creación (Formulario exacto a suno.com/create)
with st.container():
    st.markdown("<div class='create-container'>", unsafe_allow_html=True)
    
    col_mode1, col_mode2 = st.columns([1, 1])
    with col_mode1:
        custom_mode = st.toggle("Custom Mode", value=True)
    with col_mode2:
        instrumental = st.checkbox("Instrumental", value=False)

    if custom_mode:
        st.markdown("<p class='section-title'>Lyrics</p>", unsafe_allow_html=True)
        lyrics = st.text_area("Lyrics", placeholder="[Verse 1]\nEscribe tu letra aquí...\n\n[Chorus]\nCoro principal...", height=130, label_visibility="collapsed")
        
        st.markdown("<p class='section-title' style='margin-top:12px;'>Style of Music</p>", unsafe_allow_html=True)
        style = st.text_input("Style of Music", placeholder="Ej: Reggaeton chileno, bajo pesado, melancólico", label_visibility="collapsed")
        
        st.markdown("<p class='section-title' style='margin-top:12px;'>Title</p>", unsafe_allow_html=True)
        title = st.text_input("Title", placeholder="Nombre de la canción", label_visibility="collapsed")
    else:
        st.markdown("<p class='section-title'>Song Description</p>", unsafe_allow_html=True)
        prompt = st.text_area("Song Description", placeholder="Describe el estilo y temática de tu canción...", height=100, label_visibility="collapsed")
        title = "Pista Suno"
        style = "Auto-Style"

    if st.button("Create"):
        with st.spinner("Generando audio neural..."):
            time.sleep(2)
            t_name = title if title else "Sin Título"
            st.session_state.feed.insert(0, {"title": t_name, "version": "v5.5 • Part 1", "style": style, "duration": "3:15"})
            st.session_state.feed.insert(0, {"title": t_name, "version": "v5.5 • Part 2", "style": style, "duration": "3:20"})
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# Feed de Canciones (Generaciones recientes)
st.markdown("<p style='font-size:0.9rem; font-weight:700; color:#cbd5e1; margin: 20px 0 10px 0;'>Recent Generations</p>", unsafe_allow_html=True)

for item in st.session_state.feed:
    st.markdown(f"""
    <div class='suno-card'>
        <div class='cover-box'>🎵</div>
        <div style='flex-grow: 1;'>
            <div style='font-weight: 700; font-size: 0.95rem; color: #ffffff;'>{item['title']} <span style='color:#6366f1; font-size:0.7rem; background:#1e1b4b; padding:2px 6px; border-radius:4px;'>{item['version']}</span></div>
            <div style='font-size: 0.75rem; color: #94a3b8; margin-top: 3px;'>{item['style']}</div>
        </div>
        <div style='font-size: 0.75rem; color: #64748b;'>{item['duration']}</div>
    </div>
    """, unsafe_allow_html=True)

# Reproductor Inferior Fijo (Sticky Audio Player)
st.markdown("""
<div class='bottom-player' style='margin-bottom: 50px;'>
    <div style='display:flex; align-items:center; gap:12px;'>
        <div style='width:36px; height:36px; background:linear-gradient(135deg, #6366f1, #a855f7); border-radius:6px; display:flex; align-items:center; justify-content:center; font-size:0.9rem;'>▶️</div>
        <div>
            <div style='font-weight:600; font-size:0.85rem; color:#fff;'>Esquinas Oscuras (Part 1)</div>
            <div style='font-size:0.7rem; color:#94a3b8;'>Suno v5.5 Engine</div>
        </div>
    </div>
    <div style='font-size:0.75rem; color:#64748b;'>0:00 / 3:24</div>
</div>
""", unsafe_allow_html=True)
