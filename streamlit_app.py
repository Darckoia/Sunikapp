import streamlit as st
import time

# Configuración de página al estilo Web App de Suno
st.set_page_config(
    page_title="Suno - Create",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS idénticos a Suno 2.0 (Dark UI, Sidebar, Cards, Player)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    /* Reset global y fondo oscuro Suno */
    .stApp {
        background-color: #09090b !important;
        color: #f4f4f5 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    header, footer, #MainMenu { visibility: hidden !important; }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* Layout Principal tipo SPA de Suno */
    .suno-app-container {
        display: flex;
        height: 100vh;
        width: 100vw;
        overflow: hidden;
    }

    /* Sidebar Izquierdo */
    .suno-sidebar {
        width: 240px;
        background-color: #121215;
        border-right: 1px solid #27272a;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 24px 16px;
        flex-shrink: 0;
    }

    .suno-logo {
        font-size: 1.6rem;
        font-weight: 900;
        letter-spacing: -1px;
        color: #ffffff;
        margin-bottom: 30px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .nav-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 14px;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 600;
        color: #a1a1aa;
        cursor: pointer;
        transition: all 0.2s;
        margin-bottom: 4px;
    }

    .nav-item:hover, .nav-item.active {
        background-color: #27272a;
        color: #ffffff;
    }

    .nav-item.active {
        background: linear-gradient(90deg, rgba(99, 102, 241, 0.15), rgba(168, 85, 247, 0.15));
        border-left: 3px solid #8b5cf6;
        color: #ffffff;
    }

    /* Contenido Central */
    .suno-main {
        flex-grow: 1;
        display: flex;
        flex-direction: column;
        height: 100vh;
        overflow-y: auto;
        background-color: #09090b;
    }

    /* Top Navigation Bar */
    .suno-topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 32px;
        border-bottom: 1px solid #27272a;
        background-color: #09090b;
        position: sticky;
        top: 0;
        z-index: 100;
    }

    .search-bar {
        background-color: #18181b;
        border: 1px solid #27272a;
        border-radius: 9999px;
        padding: 8px 16px;
        width: 320px;
        color: #a1a1aa;
        font-size: 0.85rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .user-profile-area {
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .credits-pill {
        background-color: #18181b;
        border: 1px solid #3f3f46;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #e4e4e7;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Workspace / Create Grid */
    .workspace-grid {
        display: grid;
        grid-template-columns: 420px 1fr;
        gap: 32px;
        padding: 32px;
        max-width: 1600px;
        margin: 0 auto;
        width: 100%;
        padding-bottom: 140px;
    }

    /* Create Panel (Izquierda) */
    .create-panel {
        background-color: #121215;
        border: 1px solid #27272a;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .panel-section-title {
        font-size: 0.78rem;
        font-weight: 700;
        color: #a1a1aa;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 8px;
        margin-top: 16px;
    }

    /* Estilización de Inputs Streamlit */
    .stTextInput input, .stTextArea textarea {
        background-color: #18181b !important;
        color: #ffffff !important;
        border: 1px solid #27272a !important;
        border-radius: 10px !important;
        font-size: 0.9rem !important;
        padding: 10px 14px !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 1px #8b5cf6 !important;
    }

    /* Botón Create de Suno (Gradient Rosa/Morado/Azul) */
    .stButton>button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        border-radius: 9999px !important;
        border: none !important;
        padding: 14px 0px !important;
        width: 100%;
        margin-top: 20px;
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.4);
        transition: transform 0.1s, opacity 0.2s;
    }

    .stButton>button:hover {
        opacity: 0.95;
        transform: translateY(-1px);
    }

    /* Tarjetas de Canciones (Feed Derecho) */
    .feed-header {
        font-size: 1.25rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .song-card {
        background-color: #121215;
        border: 1px solid #27272a;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 14px;
        display: flex;
        gap: 16px;
        align-items: center;
        transition: border-color 0.2s, transform 0.1s;
    }

    .song-card:hover {
        border-color: #3f3f46;
        transform: translateY(-1px);
    }

    .song-cover {
        width: 72px;
        height: 72px;
        border-radius: 10px;
        background: linear-gradient(135deg, #3b82f6, #ec4899);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
        font-weight: 900;
        color: white;
        flex-shrink: 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    .song-details {
        flex-grow: 1;
    }

    .song-title-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 4px;
    }

    .song-name {
        font-size: 1.05rem;
        font-weight: 700;
        color: #ffffff;
    }

    .version-badge {
        background-color: #27272a;
        color: #38bdf8;
        font-size: 0.7rem;
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 700;
    }

    .song-style {
        font-size: 0.82rem;
        color: #a1a1aa;
        margin-bottom: 6px;
    }

    .song-meta {
        font-size: 0.75rem;
        color: #71717a;
    }

    /* Reproductor Inferior Fijo */
    .suno-player {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 72px;
        background-color: #121215;
        border-top: 1px solid #27272a;
        padding: 0 32px;
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    /* Responsive para móviles */
    @media (max-width: 900px) {
        .workspace-grid {
            grid-template-columns: 1fr;
            padding: 16px;
        }
        .suno-sidebar {
            display: none;
        }
    }
</style>
""", unsafe_allow_html=True)

# Estado de canciones generadas
if "songs" not in st.session_state:
    st.session_state.songs = [
        {"title": "Esquinas Oscuras", "version": "v4.5", "style": "Chilean Trap / Reggaeton Urbano, 95 BPM, heavy bass", "duration": "3:24", "cover": "🎵"},
        {"title": "Esquinas Oscuras", "version": "v4.5", "style": "Chilean Trap / Alternative Melancholic, 95 BPM", "duration": "3:12", "cover": "🔥"},
        {"title": "Sinfonía del Puerto", "version": "v4.0", "style": "Ambient Instrumental / Cinematic Synthwave", "duration": "2:45", "cover": "🎹"}
    ]

# Estructura Contenedor Principal
st.markdown("<div class='suno-app-container'>", unsafe_allow_html=True)

# 1. Sidebar Fijo Izquierdo (Suno Nav)
st.markdown("""
<div class='suno-sidebar'>
    <div>
        <div class='suno-logo'>🎵 suno</div>
        <div class='nav-item'>🏠 Home</div>
        <div class='nav-item'>🧭 Explore</div>
        <div class='nav-item active'>✨ Create</div>
        <div class='nav-item'>📚 Library</div>
    </div>
    <div>
        <div style='background-color: #18181b; border: 1px solid #27272a; border-radius: 12px; padding: 12px; text-align: center;'>
            <div style='font-size: 0.8rem; color: #a1a1aa; margin-bottom: 4px;'>Plan Gratuito</div>
            <div style='font-size: 0.9rem; font-weight: 700; color: #fff; margin-bottom: 8px;'>⚡ 2,500 Créditos</div>
            <div style='background: #27272a; color: #fff; font-size: 0.75rem; font-weight: 600; padding: 6px; border-radius: 6px;'>Obtener más</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. Main Area (Topbar + Workspace)
st.markdown("<div class='suno-main'>", unsafe_allow_html=True)

# Top Bar
st.markdown("""
<div class='suno-topbar'>
    <div class='search-bar'>
        🔍 Buscar canciones, estilos o artistas...
    </div>
    <div class='user-profile-area'>
        <div class='credits-pill'>⚡ 2,500 Credits</div>
        <div style='width:36px; height:36px; border-radius:50%; background:linear-gradient(135deg, #6366f1, #ec4899); display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:0.9rem;'>D</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Workspace Grid: Panel de Creación e Historial en Grid
st.markdown("<div class='workspace-grid'>", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.3], gap="large")

with col_left:
    st.markdown("<div class='create-panel'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 1.1rem; font-weight: 800; margin-bottom: 16px; color:#fff;'>Crear Canción</div>", unsafe_allow_html=True)
    
    c_mod1, c_mod2 = st.columns([1, 1])
    with c_mod1:
        custom_mode = st.toggle("Custom Mode", value=True)
    with c_mod2:
        instrumental = st.checkbox("Instrumental", value=False)
        
    if custom_mode:
        st.markdown("<div class='panel-section-title'>Letra (Lyrics)</div>", unsafe_allow_html=True)
        lyrics = st.text_area(
            "Lyrics",
            placeholder="[Verse 1]\nEscribe o pega tu letra aquí...\n\n[Chorus]\nCoro principal...",
            height=140,
            label_visibility="collapsed"
        )
        
        st.markdown("<div class='panel-section-title'>Estilo de Música (Style of Music)</div>", unsafe_allow_html=True)
        style = st.text_input(
            "Style of Music",
            placeholder="Ej: Chilean trap, reggaeton oscuro, 95 bpm, bajo pesado",
            label_visibility="collapsed"
        )
        
        st.markdown("<div class='panel-section-title'>Título (Title)</div>", unsafe_allow_html=True)
        title = st.text_input(
            "Title",
            placeholder="Nombre de tu canción",
            label_visibility="collapsed"
        )
    else:
        st.markdown("<div class='panel-section-title'>Descripción de la Canción</div>", unsafe_allow_html=True)
        prompt = st.text_area(
            "Description",
            placeholder="Describe el estilo y temática de la canción que quieres crear...",
            height=120,
            label_visibility="collapsed"
        )
        title = "Pista Suno"
        style = "Auto-Style"

    # Botón Create Exacto
    if st.button("Create (50 Credits)"):
        with st.spinner("Generando audio neural en Suno v4.5..."):
            time.sleep(2)
            t_name = title if title else "Sin Título"
            st.session_state.songs.insert(0, {
                "title": t_name, "version": "v4.5", "style": style if style else "Pop Urbano", "duration": "3:15", "cover": "⚡"
            })
            st.session_state.songs.insert(0, {
                "title": t_name, "version": "v4.5", "style": style if style else "Pop Urbano (Part 2)", "duration": "3:20", "cover": "⚡"
            })
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='feed-header'><span>Generaciones Recientes</span></div>", unsafe_allow_html=True)
    
    for song in st.session_state.songs:
        st.markdown(f"""
        <div class='song-card'>
            <div class='song-cover'>{song['cover']}</div>
            <div class='song-details'>
                <div class='song-title-row'>
                    <span class='song-name'>{song['title']}</span>
                    <span class='version-badge'>{song['version']}</span>
                </div>
                <div class='song-style'>{song['style']}</div>
                <div class='song-meta'>Generado recientemente • {song['duration']}</div>
            </div>
            <div style='display: flex; gap: 8px;'>
                <div style='background:#18181b; border:1px solid #27272a; color:#fff; border-radius:50%; width:36px; height:36px; display:flex; align-items:center; justify-content:center; cursor:pointer;'>▶</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True) # fin workspace-grid
st.markdown("</div>", unsafe_allow_html=True) # fin suno-main
st.markdown("</div>", unsafe_allow_html=True) # fin suno-app-container

# 3. Reproductor Inferior Fijo (Sticky Bottom Player)
st.markdown("""
<div class='suno-player'>
    <div style='display:flex; align-items:center; gap:16px;'>
        <div style='width:46px; height:46px; background:linear-gradient(135deg, #6366f1, #ec4899); border-radius:8px; display:flex; align-items:center; justify-content:center; font-weight:bold;'>🎵</div>
        <div>
            <div style='font-weight:700; font-size:0.95rem; color:#fff;'>Esquinas Oscuras (Part 1)</div>
            <div style='font-size:0.75rem; color:#a1a1aa;'>Chilean Trap / Reggaeton • Suno v4.5</div>
        </div>
    </div>
    <div style='display:flex; align-items:center; gap:20px; color:#a1a1aa; font-size:0.85rem;'>
        <span>⏮️</span>
        <span style='background:#fff; color:#000; width:32px; height:32px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:bold;'>⏸</span>
        <span>⏭️</span>
        <span style='color:#71717a;'>0:00 / 3:24</span>
    </div>
    <div style='display:flex; align-items:center; gap:12px; color:#a1a1aa; font-size:0.85rem;'>
        <span>🔊 Vol 100%</span>
        <span>❤️</span>
        <span>⋯</span>
    </div>
</div>
""", unsafe_allow_html=True)
