import streamlit as st
import numpy as np
import os
from datetime import datetime
from io import BytesIO
import wave

st.set_page_config(
    page_title="SUNICFLOW // GENERATIVE MULTI-CHANNEL DAW",
    page_icon="🪐",
    layout="wide"
)

os.makedirs("audio_cache", exist_ok=True)

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
        border-top: 4px solid #ff007f;
        background: linear-gradient(180deg, #15091a 0%, #09050d 100%);
        box-shadow: 0 0 30px rgba(255, 0, 127, 0.2);
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

st.markdown(
    "<div style='display:flex;justify-content:space-between;background:#020306;padding:12px 24px;border-bottom:2px solid #1e293b;font-size:0.75rem;color:#475569;font-weight:bold;'>"
    "<span>SUNICFLOW MAINFRAME // STATUS: ACTIVE</span>"
    "<span>ENGINE: v6.0 HYBRID URBAN SYNTH</span></div>",
    unsafe_allow_html=True
)
st.markdown("<h1 style='text-align:center;color:#fff;letter-spacing:8px;font-weight:900;margin-top:25px;'>🪐 SUNICFLOW STUDIO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#00f2fe;font-size:0.8rem;letter-spacing:4px;margin-bottom:30px;'>DAW GENERATIVO • BEAT SYNTH LOCAL</p>", unsafe_allow_html=True)

if "db_tracks" not in st.session_state:
    st.session_state.db_tracks = [
        {"nombre": "Esquinas Oscuras (Trap Urbano CL)", "fecha": "08/09/2026", "perfil": "Flaite Urbano", "tipo": "Original Track"},
        {"nombre": "Sinfonía del Puerto (Neutro Mix)", "fecha": "07/09/2026", "perfil": "Neutro Chileno", "tipo": "Pure Instrumental"}
    ]
if "chat_reverb" not in st.session_state:
    st.session_state.chat_reverb = 35
if "chat_tune" not in st.session_state:
    st.session_state.chat_tune = 20

def sintetizar_beat(prompt, acento, reverb_amt, duracion=6.0, sr=22050):
    t = np.linspace(0, duracion, int(sr * duracion), endpoint=False)
    texto = (prompt or "").lower()

    # Tempo / color según el texto (muy básico)
    if "reggaeton" in texto:
        kick_step, hat_step, bass_hz = 0.5, 0.25, 50
    elif "drill" in texto:
        kick_step, hat_step, bass_hz = 0.4, 0.125, 45
    else:
        kick_step, hat_step, bass_hz = 0.5, 0.125, 55  # trap default

    kick = np.sin(2 * np.pi * bass_hz * t) * np.exp(-4.0 * (t % kick_step))
    ruido = np.random.normal(0, 1, len(t))
    env_hat = ((t % hat_step) < 0.03).astype(float)
    hats = ruido * env_hat * 0.25

    snare_env = ((np.round((t % 1.0), 2) == 0.50)).astype(float)
    snare = ruido * snare_env * np.exp(-8.0 * (t % 0.5)) * 0.35

    mix = kick * 0.7 + hats + snare

    if reverb_amt > 0:
        delay = int(sr * 0.08)
        wet = np.zeros_like(mix)
        if delay < len(mix):
            wet[delay:] = mix[:-delay] * (reverb_amt / 200.0)
        mix = mix + wet

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

tab_create, tab_studio, tab_explore, tab_pricing = st.tabs([
    "⚡ 01. CREATE",
    "🎛️ 02. STUDIO",
    "📁 03. LIBRARY",
    "💎 04. PLANES"
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
        st.markdown("<div class='lcd-screen'>[SUNICFLOW CORE ACTIVE]<br>SYNTH LOCAL: 808 + HATS</div>", unsafe_allow_html=True)
        prompt_musica = st.text_area(
            "Describe la canción / beat:",
            placeholder="Ej: Beat de Trap chileno, bajo 808 masivo, hi-hats rápidos..."
        )
        tipo_ingreso_letra = st.radio(
            "Tipo de escritura:",
            ["Caja de Escritura Manual", "Generador Automático Coa/Urbano"],
            horizontal=True
        )
        if tipo_ingreso_letra == "Caja de Escritura Manual":
            letra_usuario = st.text_area("Letras:", placeholder="Pega tus versos...")
        else:
            tema_letra = st.text_input("Temática:", placeholder="Ej: Superación, la pobla...")
            if st.button("📝 COMPONER BARRAS"):
                st.markdown(
                    "<div class='lcd-screen'>[LYRICS GENERATED]<br>De menor sorteando la balacera en la cera,<br>voh sai hermano que andamos a nuestra manera.</div>",
                    unsafe_allow_html=True
                )
        if interfaz_toggle == "Custom / Advanced Mode":
            exclusiones = st.text_input("Excluir:", placeholder="Ej: No heavy bass...")
            weirdness_pot = st.slider("WEIRDNESS", 0, 100, 15)
            style_pot = st.slider("STYLE", 0, 100, 80)

    with col2:
        st.markdown("<div class='sunic-rack vocal-rack'><div class='hardware-label' style='color:#ff007f;'><span>CH 02 // VOCAL GATE</span><span>PERSONAS</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='lcd-screen pink'>[PERSONA SUITE]<br>VOICE ENGINE: PENDING</div>", unsafe_allow_html=True)
        genero_vocal = st.radio("Género vocal:", ["Voz Masculina (Barítono)", "Voz Femenina (Soprano)"], horizontal=True)
        acento_vocal = st.selectbox("Acento:", [
            "Español (Chile) - Coa / Flaite Urbano",
            "Español (Chile) - Neutro Chileno",
            "Español (Latinoamérica) - Neutro Internacional"
        ])
        ruteo_voz = st.selectbox("Entrada:", ["Voices", "Upload Audio", "Personas", "Inspo / Covers"])
        audio_subido = st.file_uploader("Audio referencial:", type=["wav", "mp3"])

    with col3:
        st.markdown("<div class='sunic-rack master-rack'><div class='hardware-label' style='color:#eab308;'><span>CH 03 // MASTER</span><span>STEMS</span></div></div>", unsafe_allow_html=True)
        algoritmo_stem = st.selectbox("Separación:", ["Auto Alignment Mode", "Split from mix", "Advanced Multitrack"])
        reverb_3d = st.slider("REVERB", 0, 100, int(st.session_state.chat_reverb))
        autotune_gate = st.slider("AUTOTUNE", 0, 100, int(st.session_state.chat_tune))
        activar_pultec = st.checkbox("Pultec Tube EQ", value=True)
        activar_ssl = st.checkbox("SSL G-Master Compressor", value=True)

    if st.button("🔌 TRANSMITIR SEÑAL Y COMPILAR EN S_FLOW", use_container_width=True):
        wav_bytes = sintetizar_beat(prompt_musica, acento_vocal, reverb_3d)
        nombre = (prompt_musica[:30] + "...") if prompt_musica and len(prompt_musica) > 30 else (prompt_musica or "Nueva Mezcla")
        st.session_state.db_tracks.insert(0, {
            "nombre": nombre,
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "perfil": acento_vocal,
            "tipo": ruteo_voz
        })
        st.success("Beat sintetizado (808 + hats). No es una canción con voz.")
        st.markdown("<div class='sunic-rack player-rack'><div class='hardware-label' style='color:#ff007f;'><span>MASTER OUTPUT</span><span>LOCAL SYNTH</span></div></div>", unsafe_allow_html=True)
        st.audio(wav_bytes, format="audio/wav")
        st.download_button("Descargar WAV", data=wav_bytes, file_name="sunicflow_beat.wav", mime="audio/wav")

with tab_studio:
    st.subheader("Studio 2.0")
    st.info("Lista de pistas. El synth local no separa stems reales todavía.")
    for track in st.session_state.db_tracks:
        st.markdown(f"**{track['nombre']}**  \n{track['perfil']} · {track['tipo']} · {track['fecha']}")
        st.divider()

with tab_explore:
    st.subheader("Library & Community")
    for track in st.session_state.db_tracks:
        st.markdown(
            f"<div class='social-card'><b>{track['nombre']}</b><br>{track['perfil']} · {track['tipo']}</div>",
            unsafe_allow_html=True
        )

with tab_pricing:
    st.subheader("Planes")
    c1, c2, c3 = st.columns(3)
    c1.markdown("### Free\n10 beats/día")
    c2.markdown("### Pro\nMás créditos")
    c3.markdown("### Premier\nStudio + stems")
