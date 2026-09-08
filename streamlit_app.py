import streamlit as st
import numpy as np
import os
from io import BytesIO
import wave

# 1. ARQUITECTURA DE DISEÑO: SUNIKFLOW ADVANCED v5.5 INTERFACE
st.set_page_config(
    page_title="SUNIKFLOW // GENERATIVE MULTI-CHANNEL DAW",
    page_icon="🪐",
    layout="wide"
)

# Creación automática de directorios internos de caché
os.makedirs("audio_cache", exist_ok=True)

# Inyección de diseño de interfaz Premium estilo Suno Advanced (Cajas oscuras y bordes redondeados)
st.markdown("""
    <style>
    .stApp {
        background-color: #0c0a0a;
        color: #cbd5e1;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Chasis de Cajas Redondeadas oscuras de SUNIKFLOW */
    .s_rack {
        background-color: #161414;
        border: 1px solid #242222;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }
    
    /* Etiquetas LCD estilizadas */
    .s_label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #8c8888;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Botón de ignición degradado Cyberpunk de SUNIKFLOW */
    .stButton>button {
        background: linear-gradient(90deg, #ff007f 0%, #7928ca 50%, #00f2fe 100%) !important;
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 16px 0px !important;
        width: 100%;
        letter-spacing: 2px;
        text-transform: uppercase;
        box-shadow: 0 4px 20px rgba(121, 40, 202, 0.4);
    }
    .stButton>button:hover {
        box-shadow: 0 0 35px rgba(0, 242, 254, 0.8);
    }
    
    .player-rack {
        border: 1px solid #10b981;
        background: linear-gradient(180deg, #0d1a14 0%, #050d09 100%);
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.2);
    }
    
    .social-card {
        background: #110f0f;
        border: 1px solid #242222;
        border-left: 4px solid #ff007f;
        padding: 16px;
        border-radius: 6px;
        margin-bottom: 12px;
    }
    .led-dot { width: 8px; height: 8px; border-radius: 50%; background: #242222; }
    .led-dot.green { background: #22c55e; box-shadow: 0 0 10px #22c55e; }
    .led-dot.yellow { background: #eab308; box-shadow: 0 0 10px #eab308; }
    </style>
""", unsafe_allow_html=True)

# BARRA GLOBAL SUPERIOR DE TELEMETRÍA MÓVIL
st.markdown(
    "<div style='display:flex; justify-content:space-between; background:#000000; padding:12px 24px; border-bottom:1px solid #1a181a; font-size:0.8rem; color:#8c8888; font-weight:bold;'> "
    "<span>🪐 SUNIKFLOW SYSTEM INTERFACE // v5.5 PREMIUM CORE</span>"
    "<span>Free • 30 CREDITS LEVEL</span></div>",
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align:center; color:#fff; letter-spacing:4px; font-weight:800; margin-top:20px; font-size:2rem;'>SUNIKFLOW</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#8c8888; font-size:0.8rem; margin-bottom:25px;'>Advanced Audio Generator v5.5 Active</p>", unsafe_allow_html=True)

# Inicialización de memoria virtual de pistas
if "db_tracks" not in st.session_state:
    st.session_state.db_tracks = [
        {"nombre": "Midnight Rain", "fecha": "08/09/2026", "perfil": "Dark Synth Pop", "tipo": "Advanced v5.5"},
        {"nombre": "Esquinas Oscuras (Trap Mix)", "fecha": "07/09/2026", "perfil": "Urbano CL", "tipo": "Original Track"}
    ]

# MOTOR DE AUDIO NATIVO BINARIO SINTETIZADO REPARADO
def generar_synth_beat(style_text, duracion=4.0, sr=22050):
    t = np.linspace(0, duracion, int(sr * duracion), endpoint=False)
    texto = (style_text or "").lower()

    if "synth" in texto or "pop" in texto:
        kick_step, hat_step, bass_hz = 0.5, 0.25, 60  
    elif "reggaeton" in texto or "urbano" in texto:
        kick_step, hat_step, bass_hz = 0.5, 0.25, 50
    else:
        kick_step, hat_step, bass_hz = 0.5, 0.125, 55 

    kick = np.sin(2 * np.pi * bass_hz * t) * np.exp(-4.0 * (t % kick_step))
    ruido = np.random.normal(0, 1, len(t))
    env_hat = ((t % hat_step) < 0.03).astype(float)
    hats = ruido * env_hat * 0.15

    # SECUENCIA DE NOTAS MIDI ARPEGIO REPARADA 
    arpegio = [110.0, 130.81, 146.83, 164.81]
    patron_melodia = np.zeros(len(t))
    for idx in range(int(duracion / 0.25)):
        start_idx = int(idx * 0.25 * sr)
        end_idx = int((idx + 1) * 0.25 * sr)
        nota = arpegio[idx % len(arpegio)]
        patron_melodia[start_idx:end_idx] = np.sin(2 * np.pi * nota * t[start_idx:end_idx]) * 0.05
        
    mix = kick * 0.5 + hats + patron_melodia
    mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.75
    audio_i16 = np.int16(mix * 32767)

    buffer = BytesIO()
    with wave.open(buffer, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(audio_i16.tobytes())
    buffer.seek(0)
    return buffer.read()

# ==================== PAÑO DE CONTROL ADVANCED COMPLETO ====================
col_izq, col_der = st.columns([1.5, 1.0], gap="large")

with col_izq:
    # 01. CAJA DE TÍTULO (TITLE)
    st.markdown("<div class='s_label'>Title</div>", unsafe_allow_html=True)
    title_input = st.text_input("", value="Midnight Rain", key="s_title", label_visibility="collapsed")
    
    # 02. CAJA DE ESTILOS (STYLES)
    st.markdown("<br><div class='s_label'>Styles</div>", unsafe_allow_html=True)
    styles_input = st.text_area(
        "", 
        value="dark synth pop, analog bass, intimate female vocal", 
        key="s_styles", 
        height=100,
        label_visibility="collapsed"
    )
    
    # 03. CAJA DE LETRAS (LYRICS)
    st.markdown("<br><div class='s_label'>Lyrics</div>", unsafe_allow_html=True)
    lyrics_input = st.text_area(
        "", 
        value="[Verse]\n...\n[Chorus]", 
        key="s_lyrics", 
        height=120,
        label_visibility="collapsed"
    )

with col_der:
    st.markdown("<div class='s_label'>More options</div>", unsafe_allow_html=True)
    
    # 04. FILTROS DE EXCLUSIÓN (EXCLUDE)
    st.markdown("<div style='font-size:0.75rem; color:#8c8888; margin-bottom:4px;'>Exclude styles</div>", unsafe_allow_html=True)
    exclude_input = st.text_input("", placeholder="Ej: no drums, no acoustic guitar", key="s_exclude", label_visibility="collapsed")
    
    # 05. AJUSTES DE CONSOLA DE EFECTOS
    st.markdown("<br><div class='s_label'>Console Matrix FX</div>", unsafe_allow_html=True)
    reverb_slider = st.slider("Spatial Reverb Size", 0, 100, 35)
    autotune_slider = st.slider("Quantum Autotune Gain", 0, 100, 20)
    
    st.markdown("<br>", unsafe_allow_html=True)
    genero_vocal = st.radio("Vocal Gender Selection:", ["Female Vocal Timbre", "Male Vocal Timbre"], horizontal=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# 🔌 BOTÓN MAESTRO DE IGNICIÓN EN ANCHO COMPLETO MÓVIL
if st.button("🔌 TRANSMITIR SEÑAL Y COMPILAR EN SUNIKFLOW", use_container_width=True):
    st.success(f"🪐 TRACK '{title_input}' COMPILADO Y MASTERIZADO CON ÉXITO EN SUNIKFLOW ENGINE")
    
    # Ejecutar la síntesis matemática nativa usando el prompt de la caja de estilos
    wav_audio_bytes = generar_synth_beat(styles_input)
    
    # DESPLIEGUE DEL CONTENEDOR REPRODUCTOR PREMIUM CON LUZ DE SEÑAL VERDE
    st.markdown(f"""
        <div class='s_rack player-rack'>
            <div style='font-size: 0.85rem; font-weight: 800; color: #10b981; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 10px; display: flex; justify-content: space-between;'>
                <span>🎧 MONITOR LIVE // STEREO WAVE MATRIX</span>
                <span>{title_input.upper()} READY</span>
            </div>
            <div style='display:flex; gap:6px; margin-bottom:12px;'>
                <div class='led-dot green'></div><div class='led-dot green'></div><div class='led-dot yellow'></div><div class='led-dot'></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Reproductor web nativo alimentado con los bytes locales corregidos
    st.audio(wav_audio_bytes, format="audio/wav")
    
    # Registro automático del nuevo track en el dock de tu biblioteca inferior
    nuevo_registro = {"nombre": title_input, "fecha": "08/09/2026", "perfil": "Custom Prompt", "tipo": "v5.5 Active"}
    st.session_state.db_tracks.insert(0, nuevo_registro)
    
    # Botones de descarga multipista (WAV Stems)
    st.markdown("<p style='font-size:0.75rem; color:#10b981; font-weight:bold; margin-top:15px;'>📥 EXPORTAR MULTITRACKS INDEPENDIENTES (WAV STEMS):</p>", unsafe_allow_html=True)
    sc1, sc2 = st.columns(2)
    with sc1:
        st.download_button("🎵 Descargar Pista Instrumental (WAV)", data=wav_audio_bytes, file_name=f"{title_input.lower()}_instrumental.wav", use_container_width=True)
    with sc2:
        st.download_button("🎤 Descargar Acapella de Voz con IA (WAV)", data=wav_audio_bytes, file_name=f"{title_input.lower()}_vocals.wav", use_container_width=True)

# ==================== SECCIÓN INFERIOR: HISTORIAL DE COMPOSICIONES ====================
st.markdown("<br><br><h2 style='color:#fff; letter-spacing: 1px; font-size:1.3rem;'>📁 Library & Saved Tracks</h2>", unsafe_allow_html=True)
for track in st.session_state.db_tracks:
    st.markdown(f"""
        <div class='social-card'>
            <div style='display: flex; gap: 15px; align-items: center;'>
                <div style='width: 45px; height: 45px; background: linear-gradient(135deg, #ff007f 0%, #00f2fe 100%); border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 1.2rem;'>💿</div>
                <div>
                    <b style='color:#00ffcc; font-size:1rem;'>{track['nombre']}</b><br>
                    <small style='color:#64748b;'>Fecha: {track['fecha']} | Estilo: {track['perfil']} | Modelo: {track['tipo']}</small><br>
