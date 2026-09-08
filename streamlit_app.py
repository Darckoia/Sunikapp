import streamlit as st
import time

# Configuración de página al estilo Web App
st.set_page_config(
    page_title="Suno",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS exactos para replicar la UI de Suno (Dark Mode Puro, Cards, Player)
st.markdown("""
<style>
    /* Reset Global */
    .stApp {
        background-color: #09090b !important;
        color: #f4f4f5;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    header, footer, #MainMenu { visibility: hidden; }

    /* Sidebar / Create Panel */
    [data-testid="stSidebar"] {
        background-color: #121215 !important;
        border-right: 1px solid #27272a;
        padding-top: 1rem;
    }
    
    /* Top Bar */
    .suno-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 24px;
        background-color: #09090b;
        border-bottom: 1px solid #27272a;
        margin-bottom: 15px;
    }
    
    .suno-logo {
        font-weight: 900;
        font-size: 1.5rem;
        letter-spacing: -1px;
        color: #ffffff;
    }
    
    .credits-pill {
        background-color: #18181b;
        border: 1px solid #3f3f46;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #a1a1aa;
    }

    /* Targetas de Canciones (Suno Grid Cards) */
    .suno-card {
        background-color: #141417;
        border: 1px solid #27272a;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 16px;
        display: flex;
        gap: 16px;
        align-items: center;
        transition: transform 0.1s ease, border-color 0.2s;
    }
    
    .suno-card:hover {
        border-color: #52525b;
        transform: translateY(-2px);
    }
    
    .cover-art {
        width: 80px;
        height: 80px;
        border-radius: 8px;
        background: linear-gradient(135deg, #2563eb 0%, #d946ef 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 1.2rem;
        color: white;
        flex-shrink: 0;
    }
    
    .song-info {
        flex-grow: 1;
    }
    
    .song-title {
        font-size: 1rem;
        font-weight: 700;
        color: #f4f4f5;
        margin-bottom: 4px;
    }
    
    .song-tags {
        font-size: 0.78rem;
        color: #71717a;
        margin-bottom: 8px;
    }
    
    .badge-v5 {
        background: #27272a;
        color: #38bdf8;
        font-size: 0.7rem;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
    }

    /* Botón Crear de Suno (Azul / Magenta Gradient) */
    .stButton>button {
        background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border-radius: 9999px !important;
        border: none !important;
        padding: 12px 0px !important;
        width: 100%;
        margin-top: 15px;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.5);
    }

    /* Sticky Bottom Audio Player */
    .suno-player {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 70px;
        background-color: #121215;
        border-top: 1px solid #27272a;
        padding: 0 30px;
        z-index: 9999;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
</style>
""", unsafe_allow_html=True)

# Estado de la base de datos de canciones
if "suno_feed" not in st.session_state:
    st.session_state.suno_feed = [
        {"id": 1, "title": "Esquinas Oscuras", "part": "v5.5 - Part 1", "style": "Chilean Trap / Reggaeton", "duration": "3:24", "cover": "🎵"},
        {"id": 2, "title": "Esquinas Oscuras", "part": "v5.5 - Part 2", "style": "Chilean Trap / Heavy Bass", "duration": "3:10", "cover": "🔥"},
        {"id": 3, "title": "Sinfonía del Puerto", "part": "v4.5 - Instrumental", "style": "Ambient / Beats", "duration": "2:45", "cover": "🎹"}
    ]

# ==================== BARRA LATERAL (CREATE PANEL EXACTO DE SUNO) ====================
with st.sidebar:
    st.markdown("<div class='suno-logo'>suno</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Switch Custom
    custom_mode = st.toggle("Custom Mode", value=True)
    st.caption("v5.5 Engine Active")
    
    st.markdown("---")
    
    if custom_mode:
        # Modo Custom Exacto: Lyrics + Style + Title
        lyrics = st.text_area(
            "Lyrics",
            placeholder="[Verse 1]\nEscribe o pega tu letra aquí...\n\n[Chorus]\nUsa etiquetas como [Chorus] o [Bridge]...",
            height=180
        )
        
        c_inst, c_gen = st.columns([1, 1])
        with c_inst:
            instrumental = st.checkbox("Instrumental", value=False)
        with c_gen:
            if st.button("✨ Auto-Lyrics"):
                lyrics = "[Verse 1]\nDe menor en la calle buscando el destino...\n\n[Chorus]\nY seguimos coronando..."
                
        style = st.text_input(
            "Style of Music",
            placeholder="Ej: Reggaeton, Trap Urbano, 95 BPM"
        )
        
        title = st.text_input(
            "Title",
            placeholder="Nombre de la canción"
        )
    else:
        # Modo Simple
        prompt = st.text_area(
            "Song Description",
            placeholder="Describe el tipo de canción que quieres que Suno cree...",
            height=120
        )
        instrumental = st.checkbox("Instrumental", value=False)
        title = "Pista Generada"
        style = "Auto Style"

    st.markdown("---")
    st.markdown("**Vocal Identity / Persona**")
    vocal_select = st.selectbox(
        "Vocal Profile",
        ["Chile - Flaite Urbano / Coa", "Chile - Neutro", "Latino - Pro Voice", "English - Studio"]
    )

    # Botón Create (Genera 2 versiones exactas como en Suno)
    if st.button("Create (50 Credits)"):
        with st.spinner("Creando 2 variaciones de audio..."):
            time.sleep(2)
            t_name = title if title else "Sin Título"
            
            st.session_state.suno_feed.insert(0, {
                "id": len(st.session_state.suno_feed) + 1,
                "title": t_name,
                "part": "v5.5 - Part 2",
                "style": style,
                "duration": "3:15",
                "cover": "⚡"
            })
            st.session_state.suno_feed.insert(0, {
                "id": len(st.session_state.suno_feed) + 1,
                "title": t_name,
                "part": "v5.5 - Part 1",
                "style": style,
                "duration": "3:30",
                "cover": "⚡"
            })
            st.rerun()

# ==================== CONTENIDO PRINCIPAL (FEED DE CANCIONES Y PANEL DERECHO) ====================

st.markdown("""
<div class='suno-nav'>
    <div style='font-size: 1.2rem; font-weight: 700;'>Create Workspace</div>
    <div class='credits-pill'>⚡ 2,500 Credits</div>
</div>
""", unsafe_allow_html=True)

col_feed, col_inspector = st.columns([2, 1], gap="large")

with col_feed:
    st.markdown("#### **Mis Generaciones**")
    
    # Renderizado en pares/tarjetas al estilo exacto del feed de Suno
    for track in st.session_state.suno_feed:
        st.markdown(f"""
        <div class='suno-card'>
            <div class='cover-art'>{track['cover']}</div>
            <div class='song-info'>
                <div class='song-title'>{track['title']} <span class='badge-v5'>{track['part']}</span></div>
                <div class='song-tags'>{track['style']} • {track['duration']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_inspector:
    st.markdown("#### **Detalles & Edición (DAW)**")
    st.info("Pista activa lista para edición.")
    
    # Reproducción
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("✂️ Reuse Prompt & Style")
    st.button("➕ Extend Track (Continuar canción)")
    st.button("🎙️ Separate Stems (Voces / Beats)")
    st.button("📥 Download MP3 / WAV")

# ==================== REPRODUCTOR FLOTANTE INFERIOR ====================
st.markdown("""
<div class='suno-player'>
    <div style='display:flex; align-items:center; gap:15px;'>
        <div style='width:42px; height:42px; background:linear-gradient(135deg, #2563eb, #7c3aed); border-radius:6px; display:flex; align-items:center; justify-content:center; font-weight:bold;'>🎵</div>
        <div>
            <div style='font-weight:700; font-size:0.95rem;'>Esquinas Oscuras (Part 1)</div>
            <div style='font-size:0.75rem; color:#a1a1aa;'>Chilean Trap / Reggaeton • Suno v5.5</div>
        </div>
    </div>
    <div style='font-size:0.85rem; color:#71717a;'>
        ▶️ 0:00 / 3:24 🔊
    </div>
</div>
""", unsafe_allow_html=True)
