import streamlit as st
import numpy as np
import base64
import os

# CREACIÓN AUTOMÁTICA DE CARPETAS DE CACHÉ
os.makedirs("audio_cache", exist_ok=True)

# CONFIGURACIÓN DE PÁGINA SUPREMA DE HARDWARE
st.set_page_config(page_title="SUNICFLOW // GENERATIVE MULTI-CHANNEL DAW", page_icon="🪐", layout="wide")

# INYECCIÓN DE DISEÑO INDUSTRIAL Y REPRODUCTOR PREMIUM EN CSS
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top center, #0b0d19 0%, #030407 100%);
        color: #cbd5e1;
        font-family: 'Courier New', Courier, monospace;
    }
    .sunic-rack {
        background: linear-gradient(180deg, #101424 0%, #090b14 100%);
        border: 1px solid #1e293b;
        border-top: 4px solid #00f2fe;
        border-radius: 8px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
    }
    .vocal-rack { border-top: 4px solid #ff007f; }
    .master-rack { border-top: 4px solid #eab308; }
    .social-card { background: #060811; border: 1px solid #1e293b; border-left: 4px solid #a855f7; padding: 16px; border-radius: 6px; margin-bottom: 12px; }
    
    /* REPRODUCTOR MULTIMEDIA CIBERNÉTICO PREMIUM CONTROL */
    .audio-player-container {
        background: #040712;
        border: 2px solid #10b981;
        border-radius: 6px;
        padding: 15px;
        margin-top: 15px;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
    }
    audio {
        width: 100%;
        filter: invert(1) hue-rotate(90deg); /* Adapta el color al verde neón de SunicFlow */
    }
    
    .lcd-screen {
        background-color: #03050a;
        border: 1px solid #1e293b;
        border-radius: 4px;
        padding: 12px;
        color: #00ffcc;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
        font-size: 0.8rem;
        margin-bottom: 15px;
    }
    .lcd-screen.pink { color: #ff007f; text-shadow: 0 0 10px rgba(255, 0, 127, 0.5); }
    .lcd-screen.yellow { color: #eab308; text-shadow: 0 0 10px rgba(234, 179, 8, 0.5); }
    
    .stButton>button {
        background: linear-gradient(90deg, #ff007f 0%, #7928ca 50%, #00f2fe 100%) !important;
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 1.4rem !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 20px 0px !important;
        width: 100%;
        letter-spacing: 4px;
        box-shadow: 0 0 35px rgba(121, 40, 202, 0.6);
        text-transform: uppercase;
    }
    .stButton>button:hover { box-shadow: 0 0 50px rgba(0, 242, 254, 0.9); }
    .led-bar { display: flex; gap: 6px; margin-bottom: 12px; }
    .led-dot { width: 8px; height: 8px; border-radius: 50%; background: #111422; }
    .led-dot.green { background: #22c55e; box-shadow: 0 0 10px #22c55e; }
    .led-dot.yellow { background: #eab308; box-shadow: 0 0 10px #eab308; }
    .led-dot.red { background: #ef4444; box-shadow: 0 0 10px #ef4444; }
    .hardware-label { font-size: 0.85rem; font-weight: 800; color: #475569; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 15px; display: flex; justify-content: space-between; border-bottom: 1px solid #1e293b; padding-bottom: 8px; }
    </style>
""", unsafe_allow_html=True)

# MARCO TELEMÉTRICO SUPERIOR
st.markdown("<div style='display: flex; justify-content: space-between; background: #020306; padding: 12px 24px; border-bottom: 2px solid #1e293b; font-size: 0.75rem; color: #475569; font-weight:bold;'><span>SUNICFLOW MAINFRAME // STATUS: ACTIVE</span><span>ENGINE: v6.0 HTML5 CONTROLS // INTEGRACIÓN DE BIBLIOTECA COMPLETA</span></div>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #fff; letter-spacing: 8px; font-weight: 900; margin-top:25px;'>🪐 SUNICFLOW STUDIO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00f2fe; font-size: 0.8rem; letter-spacing: 5px; margin-bottom: 35px;'>EL DAW GENERATIVO DE VANGUARDIA DE LA ERA SÚPER-INTELIGENTE</p>", unsafe_allow_html=True)

# 📁 INICIALIZACIÓN DE LA BASE DE DATOS LOCAL (SISTEMA DE BIBLIOTECA PERSISTENTE)
if "db_tracks" not in st.session_state:
    st.session_state.db_tracks = [
        {"nombre": "Esquinas Oscuras (Trap Urbano CL)", "fecha": "08/09/2026", "perfil": "Flaite Urbano", "tipo": "Remix / Cover"},
        {"nombre": "Sinfonía del Puerto (Neutro Mix)", "fecha": "08/09/2026", "perfil": "Neutro Chileno", "tipo": "Pure Instrumental"}
    ]

if "chat_reverb" not in st.session_state:
    st.session_state.chat_reverb = 35
if "chat_tune" not in st.session_state:
    st.session_state.chat_tune = 20

tab_create, tab_studio, tab_explore, tab_pricing = st.tabs(["⚡ 01. CREATE (GENERACIÓN)", "🎛️ 02. STUDIO 2.0 (DAW MULTITRACK)", "🪐 03. EXPLORE & COMMUNITY", "💎 04. PRICING & CLOUD"])

# ==================== PESTAÑA 1: CREATE ====================
with tab_create:
    interfaz_toggle = st.radio("MODO DE INTERFAZ DE GENERACIÓN:", ["Simple Mode", "Custom / Advanced Mode"], horizontal=True)
    col1, col2, col3 = st.columns([1.3, 1.3, 1.1], gap="large")
    
    with col1:
        st.markdown("<div class='sunic-rack'><div class='hardware-label'><span>CH 01 // COMPOSITION BUS</span><span>v6.0 SUPREME</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='lcd-screen'>[SUNICFLOW CORE ACTIVE]<br>GENERATION MAX: 8 MINUTES TOTAL</div>", unsafe_allow_html=True)
        prompt_musica = st.text_area("Describa la Instrumentación de Fondo (Prompt):", placeholder="Ej: Ritmo de Reggaeton pesado mezclado con guitarras...", key="txt_prompt")
        
        st.markdown("<p style='font-size:0.75rem; color:#00ffcc; font-weight:bold;'>✍️ LYRICS MANAGER / MOTOR DE LÍRICAS:</p>", unsafe_allow_html=True)
        tipo_ingreso_letra = st.radio("Tipo de Escritura:", ["Caja de Escritura Manual", "Generador Automático Coa/Urbano"], horizontal=True)
        
        if tipo_ingreso_letra == "Caja de Escritura Manual":
            letra_usuario = st.text_area("Escribe tus barras o rimas manuales:", placeholder="Pega tus versos aquí de forma manual...")
        else:
            tema_letra = st.text_input("Ingresa la temática para tus rimas:", placeholder="Ej: La pobla, maleanteo...")
            if st.button("📝 COMPONER BARRAS CALLEJERAS"):
                st.markdown("<div class='lcd-screen'>[LYRICS GENERATED]<br>De menor sorteando la balacera en la cera...<br>voh sai hermano que andamos a nuestra manera.</div>", unsafe_allow_html=True)
                
        if interfaz_toggle == "Custom / Advanced Mode":
            st.markdown("---")
            exclusiones = st.text_input("Instrumentos o Frecuencias Excluidas:", placeholder="Ej: No heavy bass...")
            weirdness_pot = st.slider("WEIRDNESS POTENTIOMETER", 0, 100, 15)
            style_pot = st.slider("STYLE POTENTIOMETER", 0, 100, 80)
        st.markdown("<div class='led-bar'><div class='led-dot green'></div><div class='led-dot green'></div><div class='led-dot green'></div><div class='led-dot yellow'></div><div class='led-dot'></div></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='sunic-rack vocal-rack'><div class='hardware-label' style='color:#ff007f;'><span>CH 02 // IDENTITY VOCAL GATE</span><span>PERSONAS & CLONES</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='lcd-screen pink'>[PERSONA SUITE CHILEAN EDITION]<br>SPECTRUM MATRIX: ACTIVE<br>VERIFICATION: IDENTITY SECURED</div>", unsafe_allow_html=True)
        genero_vocal = st.radio("Género y Espectro Vocal:", ["Voz Masculina (Barítono)", "Voz Femenina (Soprano)"], horizontal=True)
        
        acento_vocal = st.selectbox(
            "Configuración de Acento Geográfico e Idioma:",
            ["Español (Chile) - Coa / Flaite Urbano", "Español (Chile) - Neutro Chileno", "Español (Latinoamérica) - Neutro Internacional", "Español (Castellano - España)", "Inglés (EE.UU. - Hip-Hop Studio)", "Inglés (Reino Unido - London Drill)"]
        )
        ruteo_voz = st.selectbox("Estructura de Entrada Externa:", ["Voices (Usa tu propia voz)", "Upload Audio", "Personas", "Inspo / Covers / Remix"])
        audio_subido = st.file_uploader("Arrastra tu muestra de audio referencial (.wav):", type=["wav"])

    with col3:
        st.markdown("<div class='sunic-rack master-rack'><div class='hardware-label' style='color:#eab308;'><span>CH 03 // EXPORT & MASTER BUS</span><span>STEM EXTRACTOR</span></div></div>", unsafe_allow_html=True)
        st.markdown("<small style='font-size:0.7rem; color:#64748b;'>VU CLIP METER:</small><div class='led-bar'><div class='led-dot green'></div><div class='led-dot green'></div><div class='led-dot green'></div><div class='led-dot yellow'></div><div class='led-dot red'></div></div>", unsafe_allow_html=True)
        
        algoritmo_stem = st.selectbox("Modos de Separación:", ["Auto Alignment Mode", "Split from mix", "Advanced Multitrack"])
        
        st.markdown("<p style='font-size:0.75rem; color:#eab308; font-weight:bold;'>🎚️ CONSOLA DE EFECTOS ANALÓGICOS:</p>", unsafe_allow_html=True)
        reverb_3d = st.slider("REVERB ROOM SIZE (FADER)", 0, 100, int(st.session_state.chat_reverb))
        autotune_gate = st.slider("QUANTUM AUTOTUNE (GAIN)", 0, 100, int(st.session_state.chat_tune))
        
        activar_pultec = st.checkbox("Pultec Tube EQ Emulation", value=True)
        activar_ssl = st.checkbox("SSL G-Master Bus Compressor", value=True)

st.markdown("<br>", unsafe_allow_html=True)

# 🔌 PROCESADOR INTERNO GENERATIVO SEGURO CON REPRODUCTOR REMOTO EN HTML5 CON PERMISOS MÓVILES
if st.button("🔌 TRANSMITIR SEÑAL Y COMPILAR EN S_FLOW", use_container_width=True):
    st.success("🪐 COMPOSICIÓN Y TRATAMIENTO COMPLETADOS CON ÉXITO")
    
    # AGREGAR AUTOMÁTICAMENTE LA CANCIÓN A LA BIBLIOTECA AL PRESIONAR EL BOTÓN
    nuevo_nombre = prompt_musica if prompt_musica else "Nueva Mezcla Generada"
    st.session_state.db_tracks.insert(0, {
        "nombre": nuevo_nombre[:30] + "...",
