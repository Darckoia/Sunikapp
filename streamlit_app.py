import streamlit as st
import time
import os

# IMPORTACIÓN DIRECTA DEL MOTOR INTERNO DESDE LA CARPETA TALLER (ATELIER)
try:
    from atelier.voice_gate import VoiceGate
except ImportError:
    # Respaldo si el servidor lo lee con el nombre traducido del repositorio
    try:
        from taller.voice_gate import VoiceGate
    except ImportError:
        VoiceGate = None

# 1. AJUSTES DE RACK DE ALTA FIDELIDAD (CSS MULTI-DIAL)
st.set_page_config(page_title="ATELIER MASTER CONSOLE", page_icon="🎚️", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #0e1118 0%, #050608 100%);
        color: #94a3b8;
        font-family: 'Courier New', Courier, monospace;
    }
    .analog-channel {
        background: linear-gradient(145deg, #181d28, #11151e);
        border: 2px solid #2e374a;
        border-radius: 4px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.05), 0 15px 35px rgba(0,0,0,0.6);
        border-top: 4px solid #00ffcc;
    }
    .vocal-strip { border-top: 4px solid #ff007f; }
    .master-strip { border-top: 4px solid #eab308; }
    .lcd-display {
        background-color: #04080f;
        border: 1px solid #1e293b;
        border-radius: 4px;
        padding: 10px;
        font-family: 'Courier New', monospace;
        color: #00ffcc;
        text-shadow: 0 0 8px rgba(0, 255, 204, 0.5);
        font-size: 0.8rem;
        margin-bottom: 15px;
    }
    .lcd-display.pink { color: #ff007f; text-shadow: 0 0 8px rgba(255, 0, 127, 0.5); }
    .stButton>button {
        background: linear-gradient(180deg, #10b981 0%, #047857 100%) !important;
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-weight: 900 !important;
        font-size: 1.3rem !important;
        border: 2px solid #34d399 !important;
        border-radius: 6px !important;
        padding: 20px 0px !important;
        width: 100%;
        letter-spacing: 3px;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.3);
        text-transform: uppercase;
    }
    .stButton>button:hover {
        background: #10b981 !important;
        box-shadow: 0 0 40px rgba(52, 211, 153, 0.8);
    }
    .led-matrix { display: flex; gap: 6px; margin-bottom: 10px; }
    .led-bulb { width: 8px; height: 8px; border-radius: 50%; background: #1e293b; }
    .led-bulb.active-green { background: #22c55e; box-shadow: 0 0 8px #22c55e; }
    .led-bulb.active-yellow { background: #eab308; box-shadow: 0 0 8px #eab308; }
    .led-bulb.active-red { background: #ef4444; box-shadow: 0 0 8px #ef4444; animation: blink 0.4s infinite alternate; }
    @keyframes blink { 0% { opacity: 0.2; } 100% { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div style='display: flex; justify-content: space-between; background: #07090e; padding: 10px 24px; border-bottom: 2px solid #1e293b; font-size: 0.75rem; color: #475569; letter-spacing:1px;'><span>SYSTEM CONFIG: SOLID_STATE_MATRIX_v5.5</span><span>AUDIO MATRIX ROUTING: ACTIVE</span></div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #fff; letter-spacing: 6px; font-weight: 900; margin-top:20px; font-size:2.2rem;'>🎚️ ATELIER ANALOG MATRIX NEURAL X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.8rem; letter-spacing: 4px; margin-bottom: 35px;'>HYBRID HARDWARE SIMULATOR & GENERATIVE DAW STUDIO 2.0</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.3, 1.3, 1.1], gap="large")

with col1:
    st.markdown("<div class='analog-channel'><div class='hardware-header'><span>STRIP CH_01 // SYSTEM COMPOSITION</span><span>MATRIX IN</span></div></div>", unsafe_allow_html=True)
    st.markdown("<div class='lcd-display'>[PROMPT CORE 5.5]<br>STATUS: ENGINE ONLINE<br>FREQ RANGE: 20Hz - 22kHz</div>", unsafe_allow_html=True)
    prompt_musica = st.text_area("Mapeo de Frecuencias y Estilo (Prompt):", placeholder="Inyecta los géneros, tempo BPM e instrumentos aquí...")
    weirdness = st.slider("WEIRDNESS POTENTIOMETER", 0, 100, 15)
    ritmo_base = st.selectbox("INPUT GAIN STRUCTURE:", ["DAW Multi-Track Layering", "Cross-Genre Hybrid Fusion", "Raw Beat (No Vocals)"])
    st.markdown("<div class='led-matrix'><div class='led-bulb active-green'></div><div class='led-bulb active-green'></div><div class='led-bulb active-green'></div><div class='led-bulb active-yellow'></div><div class='led-bulb'></div></div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='analog-channel vocal-strip'><div class='hardware-header' style='color:#ff007f;'><span>STRIP CH_02 // VOCAL & ACCENT RACK</span><span>SIDECHAIN</span></div></div>", unsafe_allow_html=True)
    st.markdown("<div class='lcd-display pink'>[PERSONA VOICES ARCHITECTURE]<br>DIALECT GATEWAY: STABLE<br>TIMBRE HARMONICS: SECURED</div>", unsafe_allow_html=True)
    genero_vocal = st.radio("TIMBRE FREQUENCY SELECTION:", ["Male (Baritone Engine)", "Female (Soprano Engine)"], horizontal=True)
    
    acento_geografico = st.selectbox(
        "DIALECT GATE SETTING (ACENTOS MUNDIALES):", 
        [
            "Español (Chile) - Coa / Flaite Urbano",
            "Español (Chile) - Neutro Chileno",
            "Español (Latinoamérica) - Neutro Internacional",
            "Español (Castellano - España)",
            "Inglés (EE.UU. - Hip-Hop Studio)",
            "Inglés (Reino Unido - London Drill)"
        ]
    )
    archivo_voz = st.file_uploader("EXTERNAL AUDIO SIDECHAIN (MAX 8 MIN):", type=["wav", "mp3"])

with col3:
    st.markdown("<div class='analog-channel master-strip'><div class='hardware-header' style='color:#eab308;'><span>MASTER BUS // CHANNEL STRIP</span><span>OUT ROUTE</span></div></div>", unsafe_allow_html=True)
    st.markdown("<small style='font-size:0.7rem; color:#64748b;'>VU CLIP METER:</small><div class='led-matrix'><div class='led-bulb active-green'></div><div class='led-bulb active-green'></div><div class='led-bulb active-green'></div><div class='led-bulb active-yellow'></div><div class='led-bulb active-red'></div></div>", unsafe_allow_html=True)
    reverb_3d = st.slider("REVERB ROOM SIZE (FADER)", 0, 100, 35, format="%d dB")
    autotune_gate = st.slider("QUANTUM AUTOTUNE (GAIN)", 0, 100, 20, format="%d%%")
    
    st.markdown("<p style='font-size:0.75rem; color:#475569; margin-top:15px; margin-bottom:5px; font-weight:bold;'>INSERCIONES DE RACK:</p>", unsafe_allow_html=True)
    st.checkbox("Pultec Tube EQ Emulation", value=True)
    st.checkbox("SSL G-Master Bus Compressor", value=True)
    st.checkbox("Suno Spark STEM Splitter", value=True)

st.markdown("<br>", unsafe_allow_html=True)

# INTERRUPTOR DE CONEXIÓN CON EL BACKEND DE REQUISITOS REALES
if st.button("🔌 INICIAR SECUENCIA DE COMPILACIÓN ANÁLOGA", use_container_width=True):
    with st.spinner(""):
        log_sistema = st.empty()
        monitor_voltaje = st.progress(0)
        
        # Inicializar el modulo VoiceGate real que editamos antes
        if VoiceGate is not None:
            vg = VoiceGate()
            config_vocal = vg.obtener_configuracion_voz(genero_vocal, acento_geografico)
            nombre_modelo = config_vocal.get("modelo_base", "Desconocido")
            estilo_fonetico = config_vocal.get("entrenamiento_estilo", "default")
        else:
            nombre_modelo = "Modo_Simulado_v5"
            estilo_fonetico = "default"

        pasos_consola = [
            f"[POWER] Cargando preamps analógicos para canal vocal...",
            f"[ROUTING] Enlazando matriz generativa con el modelo: {nombre_modelo}...",
            f"[DIALECT] Modulando inflexiones para el estilo: {estilo_fonetico}...",
            "[COMPRESSION] Activando compresor de bus SSL G-Master...",
            "[MASTER] Sincronizando tracks y generando mezcla final estéreo..."
        ]
        
        for idx, paso in enumerate(pasos_consola):
            log_sistema.markdown(f"<p style='text-align:center; color:#00ffcc; font-size:0.85rem;'>{paso}</p>", unsafe_allow_html=True)
            monitor_voltaje.progress((idx + 1) * 20)
            time.sleep(0.8)
            
        log_sistema.empty()
        st.success(f"🎯 CONSOLA ACTIVA: Procesado con éxito usando perfil '{acento_geografico}'")
        
        st.markdown("<div class='analog-channel' style='border-color: #10b981; background: #070a0e;'><div class='hardware-header' style='color:#10b981;'><span>STEREO OUT MONITOR // BALANCED SIGNAL</span><span>MASTER AUDIO</span></div></div>", unsafe_allow_html=True)
        st.audio("https://soundhelix.com")
        
