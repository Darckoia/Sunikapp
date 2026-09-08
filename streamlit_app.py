import streamlit as st
import time

# Configuración de página para replicar la app web de Suno
st.set_page_config(
    page_title="Suno - Create",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS exactos al layout de Suno (Modo Oscuro, Sidebar fija, Audio Player en Bottom)
st.markdown("""
<style>
    /* Estilos globales */
    .stApp {
        background-color: #0a0a0c;
        color: #f3f4f6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Ocultar elementos nativos de Streamlit */
    header { visibility: hidden; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    
    /* Panel lateral de creación (Left Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #121318;
        border-right: 1px solid #27272a;
        padding-top: 0rem;
    }
    
    /* Encabezado de Suno */
    .suno-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 20px;
        background-color: #0d0e12;
        border-bottom: 1px solid #27272a;
        margin-bottom: 20px;
    }
    
    .suno-logo {
        font-weight: 800;
        font-size: 1.4rem;
        letter-spacing: -0.5px;
        color: #ffffff;
    }
    
    .credits-badge {
        background-color: #1e1f26;
        border: 1px solid #3f3f46;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        color: #a1a1aa;
    }

    /* Tarjetas del Feed de canciones (Right Workspace) */
    .song-card {
        background-color: #121318;
        border: 1px solid #27272a;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: border-color 0.2s;
    }
    .song-card:hover {
        border-color: #3f3f46;
    }
    
    .song-title {
        font-size: 1rem;
        font-weight: 600;
        color: #ffffff;
    }
    
    .song-meta {
        font-size: 0.8rem;
        color: #71717a;
        margin-top: 4px;
    }
    
    /* Botón Create estilo Suno */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px 0px !important;
        width: 100%;
        margin-top: 10px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #60a5fa 0%, #2563eb 100%) !important;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.4);
    }
    
    /* Reproductor inferior sticky */
    .bottom-player {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #0f1015;
        border-top: 1px solid #27272a;
        padding: 12px 24px;
        z-index: 999;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
</style>
""", unsafe_allow_html=True)

# Estado global de la librería de canciones
if "suno_library" not in st.session_state:
    st.session_state.suno_library = [
        {"id": 1, "title": "Esquinas Oscuras v2", "style": "Trap Urbano / Reggaeton", "duration": "3:24", "date": "Hace 2 horas", "vocal": "Flaite Urbano CL"},
        {"id": 2, "title": "Esquinas Oscuras v1", "style": "Trap Urbano / Reggaeton", "duration": "3:10", "date": "Hace 2 horas", "vocal": "Flaite Urbano CL"},
        {"id": 3, "title": "Sinfonía del Puerto", "style": "Instrumental / Ambient", "duration": "2:45", "date": "Ayer", "vocal": "Instrumental"}
    ]

# ==================== BARRA LATERAL IZQUIERDA (PANEL SUNO CREATE) ====================
with st.sidebar:
    st.markdown("<div class='suno-logo'>🎵 Suno <span style='font-size:0.8rem; color:#3b82f6;'>v5.5</span></div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Toggle Custom Mode (Fiel a la UI de Suno)
    custom_mode = st.toggle("Custom", value=True)
    
    st.markdown("---")
    
    if custom_mode:
        # Modo Custom: Letra + Estilo + Título
        lyrics_input = st.text_area(
            "Lyrics", 
            placeholder="[Verse 1]\nEscribe o pega tus letras aquí...\n\n[Chorus]\nAgrega etiquetas para guiar la estructura...", 
            height=200
        )
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🪄 Auto Lyrics"):
                lyrics_input = "[Verse 1]\nCaminando en la noche oscura\nBuscando el camino y la aventura\n\n[Chorus]\nY seguimos coronando en la calle..."
        with c2:
            instrumental_only = st.checkbox("Instrumental", value=False)
            
        style_input = st.text_input(
            "Style of Music", 
            placeholder="Ej: Chilean Trap, Reggaeton, 95 BPM, Heavy Bass"
        )
        
        title_input = st.text_input(
            "Title", 
            placeholder="Nombre de tu canción"
        )
    else:
        # Modo Simple: Song Description
        prompt_input = st.text_area(
            "Song Description", 
            placeholder="Describe el estilo y tema de la canción que quieres que Suno componga...", 
            height=150
        )
        instrumental_only = st.checkbox("Instrumental", value=False)
        title_input = "Canción Generada"
        style_input = "Auto-Style"

    # Perfil Vocal / Persona
    st.markdown("---")
    st.markdown("**Vocal Identity / Persona**")
    vocal_profile = st.selectbox(
        "Voice Model",
        [
            "Español (Chile) - Coa / Flaite Urbano",
            "Español (Chile) - Neutro Chileno",
            "Español (Latinoamérica) - Pro Voice",
            "Inglés (EE.UU.) - Studio Voice"
        ]
    )
    
    # Botón Principal de Generación
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Create (50 Credits)"):
        with st.spinner("Compuesto 2 variaciones..."):
            time.sleep(2)
            
            # Insertar las 2 variaciones automáticas en el feed superior
            new_title = title_input if title_input else "Sin Título"
            st.session_state.suno_library.insert(0, {
                "id": len(st.session_state.suno_library) + 1,
                "title": f"{new_title} (Part 2)",
                "style": style_input,
                "duration": "3:18",
                "date": "Ahora",
                "vocal": vocal_profile
            })
            st.session_state.suno_library.insert(0, {
                "id": len(st.session_state.suno_library) + 1,
                "title": f"{new_title} (Part 1)",
                "style": style_input,
                "duration": "3:30",
                "date": "Ahora",
                "vocal": vocal_profile
            })
            st.rerun()

# ==================== ÁREA PRINCIPAL (WORKSPACE / FEED DE CANCIONES) ====================

# Encabezado superior
st.markdown("""
<div class='suno-header'>
    <div style='font-weight: 600; font-size: 1.1rem;'>Explore & My Workspace</div>
    <div class='credits-badge'>⚡ 2,500 Credits Available</div>
</div>
""", unsafe_allow_html=True)

col_main, col_details = st.columns([2.2, 1], gap="medium")

with col_main:
    st.markdown("### 📋 Feed de Canciones Generadas")
    
    # Muestra la lista de canciones al estilo suno.com/create
    for track in st.session_state.suno_library:
        st.markdown(f"""
        <div class='song-card'>
            <div>
                <div class='song-title'>🎵 {track['title']}</div>
                <div class='song-meta'>Estilo: {track['style']} • Voz: {track['vocal']} • {track['date']}</div>
            </div>
            <div style='text-align: right;'>
                <span style='background:#1e293b; color:#38bdf8; font-size:0.75rem; padding:4px 8px; border-radius:4px;'>{track['duration']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_details:
    st.markdown("### 🎧 Monitor Activo")
    st.info("Selecciona o reproduce una canción para ver su espectro y opciones de edición (Studio DAW / Stems).")
    
    # Reproductor embebido de la pista actual
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    
    st.markdown("---")
    st.markdown("**Opciones de la Pista:**")
    st.button("✂️ Extension / Extend Track")
    st.button("🎙️ Separate Stems (Vocals / Drums)")
    st.button("📥 Download WAV / MP3")

# ==================== REPRODUCTOR INFERIOR FLOTANTE (BOTTOM PLAYER) ====================
st.markdown("""
<div class='bottom-player'>
    <div style='display:flex; align-items:center; gap:12px;'>
        <div style='width:40px; height:40px; background:#2563eb; border-radius:4px; display:flex; align-items:center; justify-content:center; font-weight:bold;'>🎵</div>
        <div>
            <div style='font-size:0.9rem; font-weight:600; color:#fff;'>Esquinas Oscuras (Part 1)</div>
            <div style='font-size:0.75rem; color:#9ca3af;'>Suno v5.5 Engine • Flaite Urbano CL</div>
        </div>
    </div>
    <div style='font-size:0.85rem; color:#6b7280;'>
        0:00 / 3:30
    </div>
</div>
""", unsafe_allow_html=True)
