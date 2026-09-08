import streamlit as st
import numpy as np
import os
import requests
from datetime import datetime
from io import BytesIO
import wave

# 1. AJUSTES DE HARDWARE PREMIUM (SUNICFLOW v6.0)
st.set_page_config(
    page_title="SUNICFLOW // GENERATIVE MULTI-CHANNEL DAW",
    page_icon="🪐",
    layout="wide"
)

# Creación automática de directorios internos de caché
os.makedirs("audio_cache", exist_ok=True)

# Inyección de diseño industrial y texturas oscuras en CSS
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
    .player-rack {
        border-top: 4px solid #10b981;
        background: linear-gradient(180deg, #091a14 0%, #040d09 100%);
        box-shadow: 0 0 30px rgba(16, 185, 129, 0.2);
    }
    .social-card {
        background: #060811;
        border: 1px solid #1e293b;
        border-left: 4px solid #00f2fe;
        padding: 16px;
        border-radius: 6px;
        margin-bottom: 12px;
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
    .stButton>button {
        background: linear-gradient(90deg, #ff007f 0%, #7928ca 50%, #00f2fe 100%) !important;
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 18px 0px !important;
        width: 100%;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    .led-bar { display: flex; gap: 6px; margin-bottom: 12px; }
    .led-dot { width: 8px; height: 8px; border-radius: 50%; background: #111422; }
    .led-dot.green { background: #22c55e; box-shadow: 0 0 10px #22c55e; }
    .led-dot.yellow { background: #eab308; box-shadow: 0 0 10px #eab308; }
    .led-dot.red { background: #ef4444; box-shadow: 0 0 10px #ef4444; }
    .hardware-label {
        font-size: 0.85rem; font-weight: 800; color: #475569;
        letter-spacing: 2px; text-transform: uppercase; margin-bottom: 15px;
        display: flex; justify-content: space-between;
        border-bottom: 1px solid #1e293b; padding-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# BARRA SUPERIOR DE CONSOLA
st.markdown(
    "<div style='display:flex;justify-content:space-between;background:#020306;padding:12px 24px;border-bottom:2px solid #1e293b;font-size:0.75rem;color:#475569;font-weight:bold;'>"
    "<span>SUNICFLOW MAINFRAME // STATUS: ACTIVE</span>"
    "<span>ENGINE: v6.0 HYBRID ELEVENLABS REAL PIPELINE</span></div>",
    unsafe_allow_html=True
)
st.markdown("<h1 style='text-align:center;color:#fff;letter-spacing:8px;font-weight:900;margin-top:25px;'>🪐 SUNICFLOW STUDIO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#00f2fe;font-size:0.8rem;letter-spacing:4px;margin-bottom:30px;'>ESTACIÓN DE AUDIO GENERATIVA • CLON CLOUD AUTO-HOSPEDADO</p>", unsafe_allow_html=True)

# 2. INICIALIZACIÓN DE LA BASE DE DATOS DE HISTORIAL DE COMPOSICIONES
if "db_tracks" not in st.session_state:
    st.session_state.db_tracks = [
        {"nombre": "Esquinas Oscuras (Trap Urbano CL)", "fecha": "08/09/2026", "perfil": "Flaite Urbano", "tipo": "Original Track"},
        {"nombre": "Sinfonía del Puerto (Neutro Mix)", "fecha": "07/09/2026", "perfil": "Neutro Chileno", "tipo": "Pure Instrumental"}
    ]
if "chat_reverb" not in st.session_state:
    st.session_state.chat_reverb = 35
if "chat_tune" not in st.session_state:
    st.session_state.chat_tune = 20

# 3. MOTOR DE AUDIO NATIVO COMPLETO (SÍNTESIS CIENTÍFICA DE RITMOS URBANOS)
def sintetizar_beat_local(prompt, reverb_amt, duracion=6.0, sr=22050):
    t = np.linspace(0, duracion, int(sr * duracion), endpoint=False)
    texto = (prompt or "").lower()

    # Calibración del ritmo según el Prompt de Entrada (Estilos del Clon de 2026)
    if "reggaeton" in texto or "perreo" in texto:
        kick_step, hat_step, bass_hz = 0.5, 0.25, 50
    elif "drill" in texto or "london" in texto:
        kick_step, hat_step, bass_hz = 0.4, 0.125, 45
    else:
        kick_step, hat_step, bass_hz = 0.5, 0.125, 55  # Trap por defecto

    # Generación de ondas analógicas virtuales
    kick = np.sin(2 * np.pi * bass_hz * t) * np.exp(-4.0 * (t % kick_step))
    ruido = np.random.normal(0, 1, len(t))
    env_hat = ((t % hat_step) < 0.03).astype(float)
    hats = ruido * env_hat * 0.20

    snare_env = ((np.round((t % 1.0), 2) == 0.50)).astype(float)
    snare = ruido * snare_env * np.exp(-8.0 * (t % 0.5)) * 0.30

    mix = kick * 0.7 + hats + snare

    # Efecto de Espacialidad / Reverb en el bus maestro
    if reverb_amt > 0:
        delay = int(sr * 0.08)
        wet = np.zeros_like(mix)
        if delay < len(mix):
            wet[delay:] = mix[:-delay] * (reverb_amt / 200.0)
        mix = mix + wet

    # Compresión y Normalización comercial de picos
    mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.85
    audio_i16 = np.int16(mix * 32767)

    buffer = BytesIO()
    with wave.open(buffer, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(audio_i16.tobytes())
    buffer.seek(0)
    return buffer.read()

# 4. MOTOR VOCAL REAL (CONEXIÓN DIRECTA CON LA API DE ELEVENLABS CLONE)
def generar_voz_elevenlabs_real(texto_lírica, acento):
    api_key = st.secrets.get("ELEVENLABS_API_KEY", "")
    if not api_key:
        return None  # Si no hay llave, el sistema hace bypass automático
        
    # Mapeo de IDs de voces según el menú táctil
    id_voz = "pNInz6obpgfr9ff95uU0"  # ID por defecto (Latam)
    if "Flaite Urbano" in acento:
        id_voz = "pNInz6obpgfr9ff95uU0"  # Aquí puedes cambiarlo por tu ID de voz clonada
        
    url = f"https://elevenlabs.io{id_voz}"
    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "text": texto_lírica,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.40, "similarity_boost": 0.80}
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.content
    except Exception:
        return None
    return None

# PESTAÑAS DE LA SUITE INDUSTRIAL CON EL ECOVISTEMA DE 2026 COMPLETE
tab_create, tab_studio, tab_explore, tab_pricing = st.tabs([
    "⚡ 01. CREATE (CONSOLA)",
    "🎛️ 02. STUDIO 2.0 (DAW)",
    "📁 03. LIBRARY & COMMUNITY",
    "💎 04. PLANES & CREDITS"
])

with tab_create:
    interfaz_toggle = st.radio(
        "MODO DE INTERFAZ DE GENERACIÓN:",
        ["Simple Mode", "Custom / Advanced Mode"],
        horizontal=True
    )
    col1, col2, col3 = st.columns([1.3, 1.3, 1.1], gap="large")

    with col1:
        st.markdown("<div class='sunic-rack'><div class='hardware-label'><span>CH 01 // COMPOSITION BUS</span><span>v6.0</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='lcd-screen'>[SUNICFLOW CORE ACTIVE]<br>SYNTH REAL: TEXT-TO-AUDIO CLONE</div>", unsafe_allow_html=True)
        prompt_musica = st.text_area(
            "Describe la composición / beat instrumental:",
            placeholder="Ej: Beat de Trap chileno, bajo 808 masivo, hi-hats rápidos o ritmos de Reggaeton..."
        )
        tipo_ingreso_letra = st.radio(
            "Tipo de estructura de letra:",
            ["Caja de Escritura Manual", "Generador Automático Coa/Urbano"],
            horizontal=True
        )
        letra_final_texto = ""
        if tipo_ingreso_letra == "Caja de Escritura Manual":
            letra_final_texto = st.text_area("Letras manuales del artista:", placeholder="Escribe tus rimas urbanas aquí para pasarlas al clon de voz...")
        else:
            tema_letra = st.text_input("Temática para barras automáticas:", placeholder="Ej: Superación, la pobla, maleanteo...")
            if st.button("📝 COMPONER BARRAS POR IA"):
                letra_final_texto = "De menor sorteando la balacera en la cera, voh sai hermano que andamos a nuestra manera."
                st.markdown(f"<div class='lcd-screen'>[LYRICS GENERATED]<br>{letra_final_texto}</div>", unsafe_allow_html=True)
        if interfaz_toggle == "Custom / Advanced Mode":
            st.markdown("---")
            exclusiones = st.text_input("Excluir de la mezcla (Exclusions):", placeholder="Ej: No heavy bass...")
            weirdness_pot = st.slider("WEIRDNESS CONTROL", 0, 100, 15)
            style_pot = st.slider("STYLE MATCH RATIO", 0, 100, 80)

    with col2:
        st.markdown("<div class='sunic-rack vocal-rack'><div class='hardware-label' style='color:#ff007f;'><span>CH 02 // IDENTITY VOCAL GATE</span><span>STYLE TTS2 / SEED-VC</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='lcd-screen pink'>[PERSONA & VOICE SYNTH]<br>ENGINE PIPELINE: INTEGRATED</div>", unsafe_allow_html=True)
        genero_vocal = st.radio("Género de voz neural:", ["Voz Masculina (Barítono)", "Voz Femenina (Soprano)"], horizontal=True)
        acento_vocal = st.selectbox("Mapeo de Acento y Dialecto:", [
            "Español (Chile) - Coa / Flaite Urbano",
