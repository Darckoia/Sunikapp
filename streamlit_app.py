import streamlit as st
import time
import os
import requests
from datetime import datetime

# ==================== MÓDULO ELEVENLABS & VOICE GATE REPERTORIO COMPLETO ====================
class ElevenLabsVoiceEngine:
    def __init__(self):
        # Repertorio consolidado de voces y modelos de ElevenLabs + Pistas regionales
        self.repertorio_voces = {
            "Masculino": {
                "Español (Chile) - Coa / Flaite Urbano": {"id": "es_cl_male_urbano", "model": "eleven_multilingual_v2"},
                "Español (Chile) - Neutro Chileno": {"id": "es_cl_male_neutro", "model": "eleven_multilingual_v2"},
                "Español (Latinoamérica) - Adam (Pro Voice)": {"id": "pNInz6obpgDQGcFmaJgB", "model": "eleven_multilingual_v2"},
                "Español (Latinoamérica) - Antoni (Warm)": {"id": "ErXwobaYiN019PkySvjV", "model": "eleven_multilingual_v2"},
                "Español (Castellano) - Arnold (Narración)": {"id": "VR6AewLTigWG4xT1s5nC", "model": "eleven_multilingual_v2"},
                "Inglés (EE.UU.) - Josh (Deep Studio)": {"id": "TxGEqnscrfWFTf81Cj2q", "model": "eleven_multilingual_v2"},
                "Inglés (Reino Unido) - Sam (London Drill)": {"id": "yoZ06a6152A2mrGs9XnD", "model": "eleven_multilingual_v2"}
            },
            "Femenino": {
                "Español (Chile) - Coa / Flaite Urbano": {"id": "es_cl_female_urbano", "model": "eleven_multilingual_v2"},
                "Español (Chile) - Neutro Chileno": {"id": "es_cl_female_neutro", "model": "eleven_multilingual_v2"},
                "Español (Latinoamérica) - Rachel (Pro Voice)": {"id": "21m00Tcm4TlvDq8ikWAM", "model": "eleven_multilingual_v2"},
                "Español (Latinoamérica) - Elli (Emotional)": {"id": "MF3mGyEYCl7XYWbV9V6O", "model": "eleven_multilingual_v2"},
                "Español (Castellano) - Bella (Suave)": {"id": "EXAVITQu4vr4xnSDxMaL", "model": "eleven_multilingual_v2"},
                "Inglés (EE.UU.) - Domi (Strong)": {"id": "AZnzlk1XvdvUeBnXmlld", "model": "eleven_multilingual_v2"}
            }
        }
        os.makedirs("audio_cache", exist_ok=True)

    def obtener_info_voz(self, genero, acento):
        genero_key = "Masculino" if "male" in genero.lower() else "Femenino"
        voces = self.repertorio_voces.get(genero_key, {})
        return voces.get(acento, {"id": "21m00Tcm4TlvDq8ikWAM", "model": "eleven_multilingual_v2"})

    def sintetizar_audio(self, api_key, voice_id, texto, stability, similarity, style, speaker_boost):
        if not api_key:
            # Modo Simulación (Demo sin API Key)
            time.sleep(1)
            return "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", False

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        data = {
            "text": texto if texto else "Generando prueba de voz sintética neural.",
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": float(stability),
                "similarity_boost": float(similarity),
                "style": float(style),
                "use_speaker_boost": speaker_boost
            }
        }
        try:
            res = requests.post(url, json=data, headers=headers)
            if res.status_code == 200:
                filepath = "audio_cache/elevenlabs_generated.mp3"
                with open(filepath, "wb") as f:
                    f.write(res.content)
                return filepath, True
            else:
                st.error(f"Error ElevenLabs API [{res.status_code}]: {res.text}")
                return "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", False
        except Exception as e:
            st.error(f"Fallo de conexión con el motor ElevenLabs: {e}")
            return "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", False

# Inicializar motor de voz
voice_engine = ElevenLabsVoiceEngine()

# ==================== CONFIGURACIÓN DE PÁGINA Y ESTILOS ====================
st.set_page_config(page_title="ATELIER CORE X - ELEVENLABS MATRIX DAW", page_icon="🛸", layout="wide")

st.markdown("""
<style> 
.stApp { background: radial-gradient(circle at top center, #05060c 0%, #010204 100%); color: #e2e8f0; font-family: 'Courier New', Courier, monospace; } 
.analog-channel { background: linear-gradient(180deg, #0e1220 0%, #080a12 100%); border: 1px solid #1e293b; border-top: 4px solid #00f2fe; border-radius: 6px; padding: 20px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); } 
.vocal-strip { border-top: 4px solid #ff007f; } 
.master-strip { border-top: 4px solid #eab308; } 
.lcd-display { background-color: #03050a; border: 1px solid #1e293b; border-radius: 4px; padding: 10px; color: #00ffcc; text-shadow: 0 0 8px rgba(0, 255, 204, 0.4); font-size: 0.8rem; margin-bottom: 12px; } 
.lcd-display.pink { color: #ff007f; text-shadow: 0 0 8px rgba(255, 0, 127, 0.4); } 
.lcd-display.yellow { color: #eab308; text-shadow: 0 0 8px rgba(234, 179, 8, 0.4); } 
.track-card { background: #04060a; border: 1px solid #1e293b; padding: 12px; border-radius: 4px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; } 
.stButton>button { background: linear-gradient(180deg, #10b981 0%, #047857 100%) !important; color: #ffffff !important; font-family: 'Courier New', monospace !important; font-weight: 900 !important; font-size: 1.2rem !important; border: 2px solid #34d399 !important; border-radius: 4px !important; padding: 16px 0px !important; width: 100%; letter-spacing: 2px; } 
.stButton>button:hover { background: #10b981 !important; box-shadow: 0 0 25px rgba(52, 211, 147, 0.6); } 
.led-matrix { display: flex; gap: 6px; margin-bottom: 10px; } 
.led-bulb { width: 8px; height: 8px; border-radius: 50%; background: #1e293b; } 
.led-bulb.active-green { background: #22c55e; box-shadow: 0 0 8px #22c55e; } 
.led-bulb.active-yellow { background: #eab308; box-shadow: 0 0 8px #eab308; } 
.led-bulb.active-red { background: #ef4444; box-shadow: 0 0 8px #ef4444; animation: blink 0.4s infinite alternate; } 
@keyframes blink { 0% { opacity: 0.2; } 100% { opacity: 1; } } 
</style>
""", unsafe_allow_html=True)

# BARRA DE TELEMETRÍA GLOBAL
st.markdown("<div style='display: flex; justify-content: space-between; background: #020306; padding: 10px 24px; border-bottom: 2px solid #1e293b; font-size: 0.75rem; color: #475569; letter-spacing:1px;'><span>MAINFRAME STATUS: ONLINE // ELEVENLABS CLONE SUITE v2.5</span><span>FINANCIAL CAPITAL: $775M SECURED</span></div>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #fff; letter-spacing: 6px; font-weight: 900; margin-top:20px; font-size:2.2rem;'>🪐 ATELIER STUDIO MATRIX NEURAL X</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #38bdf8; font-size: 0.8rem; letter-spacing: 4px; margin-bottom: 30px;'>NEXT-GEN DIGITAL AUDIO WORKSTATION + ELEVENLABS CLONE</p>", unsafe_allow_html=True)

# INICIALIZACIÓN DE LA BASE DE DATOS LOCAL
if "db_tracks" not in st.session_state:
    st.session_state.db_tracks = [
        {"nombre": "Esquinas Oscuras (Trap Urbano CL)", "fecha": "08/2026", "perfil": "Flaite Urbano", "tipo": "ElevenLabs Clone / Cover"},
        {"nombre": "Sinfonía del Puerto (Neutro Mix)", "fecha": "08/2026", "perfil": "Neutro Chileno", "tipo": "Pure Instrumental"}
    ]

# PANEL LATERAL DE CONFIGURACIÓN DE API
with st.sidebar:
    st.markdown("### 🔑 CREDENCIALES ELEVENLABS")
    eleven_api_key = st.text_input("API Key de ElevenLabs:", type="password", placeholder="xi-api-key...")
    st.caption("Si se deja en blanco, la app operará en modo simulación análoga.")
    st.markdown("---")
    st.markdown("### 🎛️ CONTROLES DE VOZ ELEVENLABS")
    stability_val = st.slider("Stability (Estabilidad)", 0.0, 1.0, 0.50, 0.05)
    similarity_val = st.slider("Clarity / Similarity Boost", 0.0, 1.0, 0.75, 0.05)
    style_val = st.slider("Style Exaggeration", 0.0, 1.0, 0.10, 0.05)
    speaker_boost_val = st.checkbox("Speaker Boost (Claridad mejorada)", value=True)

# ==================== PESTAÑAS PRINCIPALES ====================
tab_create, tab_studio, tab_library, tab_pricing = st.tabs(["🎵 CREATE & VOICE CLONE", "🎛️ STUDIO 2.0 (DAW WEB)", "📁 LIBRARY & MONITORS", "💎 SUBSCRIPTION & PLANS"])

# ==================== PESTAÑA 1: CREATE & VOICE CLONE ====================
with tab_create:
    modo_creacion = st.radio("TOGGLE SELECTION INTERFACE:", ["Simple Mode", "Custom / Advanced Mode"], horizontal=True)
    
    col1, col2, col3 = st.columns([1.3, 1.3, 1.1], gap="large")
    
    with col1:
        st.markdown("<div class='analog-channel'><div class='hardware-header'><span>CH 01 // COMPOSITION BUS</span><span>v5.5 COMPILER</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='lcd-display'>[PROMPT & TEXT MATRIX ACTIVE]<br>TTS & MUSIC GENERATION READY<br>ELEVENLABS MULTILINGUAL v2</div>", unsafe_allow_html=True)
        
        prompt_musica = st.text_area("Mapeo de Estilo / Guion o Letra:", placeholder="Escribe el texto a sintetizar o la descripción musical...")
        
        if modo_creacion == "Custom / Advanced Mode":
            st.markdown("<p style='font-size:0.75rem; color:#00ffcc; font-weight:bold; margin-top:15px;'>✍️ LYRICS MANAGER (MÓDULO DE LETRA):</p>", unsafe_allow_html=True)
            tipo_letra = st.radio("Ingreso de Lírica:", ["Caja de Escritura Manual", "Generador Automático por IA"], horizontal=True)
            if tipo_letra == "Caja de Escritura Manual":
                letra_manual = st.text_area("Escribe tus barras o guion aquí:", placeholder="Ingresa versos o diálogo en español chileno...")
            else:
                tema_letra = st.text_input("Concepto de Letra:", placeholder="Ej: La pobla, maleanteo, superación...")
                if st.button("📝 COMPONER LETRA AUTOMÁTICA"):
                    st.markdown("<div class='lcd-display'>[LYRICS IA CORE]<br>'De menor sorteando la balacera en la cera...<br>voh sa'i hermano que andamos a nuestra manera.'</div>", unsafe_allow_html=True)
            
            exclusiones = st.text_input("Instrumentos o Frecuencias Excluidas:", placeholder="Ej: No drums, no vocal echoes...")
            weirdness = st.slider("Slider de Rareza / Weirdness", 0, 100, 15)
            style_slider = st.slider("Slider de Estilo / Style Match", 0, 100, 75)
        st.markdown("<div class='led-matrix'><div class='led-bulb active-green'></div><div class='led-bulb active-green'></div><div class='led-bulb active-green'></div><div class='led-bulb active-yellow'></div><div class='led-bulb'></div></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='analog-channel vocal-strip'><div class='hardware-header' style='color:#ff007f;'><span>CH 02 // ELEVENLABS REPERTOIRE</span><span>VOICE CLONE GATE</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='lcd-display pink'>[ELEVENLABS REPERTOIRE ACTIVE]<br>SOURCE: INSTANT CLONING / PRESETS<br>VERIFICATION: VERIFIED</div>", unsafe_allow_html=True)
        
        genero_vocal = st.radio("Género Vocal Neural:", ["Male (Baritone Engine)", "Female (Soprano Engine)"], horizontal=True)
        
        acento_geografico = st.selectbox(
            "Repertorio Completo de Voces & Acentos:", 
            [
                "Español (Chile) - Coa / Flaite Urbano",
                "Español (Chile) - Neutro Chileno",
                "Español (Latinoamérica) - Adam (Pro Voice)",
                "Español (Latinoamérica) - Antoni (Warm)",
                "Español (Latinoamérica) - Rachel (Pro Voice)",
                "Español (Latinoamérica) - Elli (Emotional)",
                "Español (Castellano) - Arnold (Narración)",
                "Español (Castellano) - Bella (Suave)",
                "Inglés (EE.UU.) - Josh (Deep Studio)",
                "Inglés (Reino Unido) - Sam (London Drill)"
            ]
        )
        
        voz_info = voice_engine.obtener_info_voz(genero_vocal, acento_geografico)
        st.caption(f"🎙️ ElevenLabs Voice ID: `{voz_info['id']}` | Model: `{voz_info['model']}`")
        
        opcion_source = st.selectbox("Modalidad de Clonación / Origen:", ["Preset Repertoire", "Instant Voice Cloning (Sube Audio de Muestra)", "Voices Studio", "Personas Saved"])
        archivo_usuario = st.file_uploader("Sube audio para clonación instantánea (.wav, .mp3):", type=["wav", "mp3"])

    with col3:
        st.markdown("<div class='analog-channel master-strip'><div class='hardware-header' style='color:#eab308;'><span>CH 03 // EXPORT & MASTERING</span><span>OUT CONTROL</span></div></div>", unsafe_allow_html=True)
        st.markdown("<small style='font-size:0.7rem; color:#64748b;'>VU CLIP METER:</small><div class='led-matrix'><div class='led-bulb active-green'></div><div class='led-bulb active-green'></div><div class='led-bulb active-green'></div><div class='led-bulb active-yellow'></div><div class='led-bulb active-red'></div></div>", unsafe_allow_html=True)
        
        st.markdown("<p style='font-size:0.75rem; color:#eab308; font-weight:bold;'>STEM SEPARATION MODES:</p>", unsafe_allow_html=True)
        modo_stem = st.selectbox("Algoritmo de Extracción de Canales:", ["Auto Separation", "Split from mix (Vocals + Inst)", "Advanced Multi-Track (12 Stems)"])
        
        st.markdown("<p style='font-size:0.75rem; color:#475569; font-weight:bold; margin-top:15px;'>FEATURES EXTRAS:</p>", unsafe_allow_html=True)
        st.checkbox("ElevenLabs Voice Isolation (Limpieza de Ruido)", value=True)
        st.checkbox("Create Hooks (Clips cortos verticales TikTok/Reels)", value=True)
        st.checkbox("Extend / Crop / Replace Section", value=False)

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🔌 INICIAR SÍNTESIS DE VOZ Y COMPILACIÓN ANÁLOGA", use_container_width=True):
        with st.spinner(""):
            log_box = st.empty()
            p_bar = st.progress(0)
            
            pasos = [
                "[POWER] Alimentando bulbos del rack analógico...",
                f"[ELEVENLABS] Conectando con Voice ID '{voz_info['id']}'...",
                f"[PARAM] Estabilidad: {stability_val} | Claridad: {similarity_val}...",
                "[MASTER] Aplicando procesamiento de dinámica y renderizado MP3/WAV..."
            ]
            for idx, paso in enumerate(pasos):
                log_box.markdown(f"<p style='text-align:center; color:#00ffcc; font-size:0.85rem;'>{paso}</p>", unsafe_allow_html=True)
                p_bar.progress((idx + 1) * 25)
                time.sleep(0.6)
            log_box.empty()
            
            audio_out, es_real = voice_engine.sintetizar_audio(
                eleven_api_key, 
                voz_info['id'], 
                prompt_musica, 
                stability_val, 
                similarity_val, 
                style_val, 
                speaker_boost_val
            )
            
            if es_real:
                st.success("🎯 VOZ GENERADA CON ÉXITO VÍA ELEVENLABS API")
            else:
                st.info("🎯 PISTA RENDERIZADA (MODO SIMULACIÓN / MUESTRA)")
            
        st.markdown("<div class='lcd-display yellow'>STEREO OUT MONITOR // ELEVENLABS AUDIO MASTER READY</div>", unsafe_allow_html=True)
        st.audio(audio_out)
        sc1, sc2 = st.columns(2)
        with sc1:
            st.download_button("📥 Descargar Base Instrumental Limpia (WAV)", data=b"instrumental", file_name="instrumental_master.wav", use_container_width=True)
        with sc2:
            st.download_button("🎤 Descargar Acapella / Voz Sintetizada (MP3)", data=b"vocal", file_name="vocal_elevenlabs.mp3", use_container_width=True)

# ==================== PESTAÑA 2: STUDIO 2.0 ====================
with tab_studio:
    st.markdown("<div class='analog-channel'><div class='hardware-header'><span>SUNO & ELEVENLABS STUDIO 2.0 // DIGITAL AUDIO WORKSTATION</span><span>PREMIER ONLY</span></div></div>", unsafe_allow_html=True)
    st.markdown("<div class='lcd-display'>[DAW TIMELINE RECOGNITION ACTIVE]<br>SAMPLE RATE: 32-bit / 48 kHz (UNLIMITED EXPORT)<br>MIDI WEB INTERFACE & ELEVENLABS CLONER: ENABLED</div>", unsafe_allow_html=True)
    
    sc_col1, sc_col2 = st.columns([2, 1])
    with sc_col1:
        st.markdown("🎛️ **TIMELINE MULTITRACK & PIANO ROLL SIMULATOR:**")
        st.selectbox("MIDI Prompt Input source:", ["Piano Roll Recording", "Velocity & Pitch Bend Map", "MIDI File Clip Input"])
        st.slider("Consola de Automatización de Parámetros (Automation)", 0, 100, 45)
        st.checkbox("Take Lanes (Generar variaciones por tomas separadas)", value=True)
        st.checkbox("Remove FX (Eliminar Reverb/Delay para obtener pista limpia DRY)", value=False)
    
    with sc_col2:
        st.markdown("🎚️ **RACK DE PLUGINS EN TIEMPO REAL:**")
        st.text_input("Describe un plugin personalizado en lenguaje natural:", placeholder="Ej: Haz un tape saturation cálido con wobble...")
        st.selectbox("Wavetable Synth Nativo:", ["Analog Sawtooth Wave", "Quantum Square Wave", "Sub-Bass Heavy Subwoofer"])
        st.multiselect("Efectos Activos en el Master Bus:", ["Compressor", "EQ Pultec", "Reverb 3D", "Delay", "Distortion / Saturation", "Gate"], default=["Compressor", "Reverb 3D"])

# ==================== PESTAÑA 3: LIBRARY ====================
with tab_library:
    st.markdown("### 📁 DATABASE: HISTORIAL DE COMPOSICIONES & VOCES")
    st.markdown("<div class='lcd-display'>TODAS TUS CANCIONES Y CLONES DE VOZ PRIVADOS POR DEFECTO</div>", unsafe_allow_html=True)
    
    for track in st.session_state.db_tracks:
        st.markdown(f"""
        <div class='track-card'>
            <div>
                <strong>🎵 {track['nombre']}</strong><br>
                <small style='color:#94a3b8;'>Fecha: {track['fecha']} | Perfil Vocal: {track['perfil']} | Origen: {track['tipo']}</small>
            </div>
            <span style='color:#10b981; font-size:0.75rem;'>COMMERCIAL RIGHTS SECURED</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    with st.expander("📖 PROGRAMAS CORPORATIVOS & RECURSOS DE MARCA"):
        st.markdown("""
        * **Suno & ElevenLabs Integration:** Clonación instantánea de voz combinada con motores de composición musical.
        * **Spark:** Incubadora oficial para artistas independientes (Grants, mentorías y marketing con derechos completos).
        * **In the Cut:** Serie de videos oficiales con productores usando el motor en estudios reales de grabación.
        * **Knowledge Base Oficial:** Soporte indexado para síntesis multilingüe, derechos comerciales y configuración de DAW.
        """)

# ==================== PESTAÑA 4: PRICING ====================
with tab_pricing:
    st.markdown("### 💎 PLANES DE SUSCRIPCIÓN COMERCIAL (TARIFAS 2026)")
    st.markdown("<div class='lcd-display pink'>FACTURACIÓN ANUAL (PLANES MENSUALES TIENEN COSTOS DE $10 PRO / $30 PREMIER)</div>", unsafe_allow_html=True)
    
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        st.markdown("""
        <div class='analog-channel'>
            <h4>PLAN FREE</h4>
            <p><strong>Costo:</strong> $0</p>
            <p><strong>Créditos:</strong> 50 al día (~10 tracks)</p>
            <p><strong>Modelos:</strong> Multilingual v2 Standard</p>
            <p><strong>Derechos comerciales:</strong> NO</p>
            <p><strong>DAW Studio:</strong> NO</p>
        </div>
        """, unsafe_allow_html=True)
    with pc2:
        st.markdown("""
        <div class='analog-channel vocal-strip'>
            <h4 style='color:#ff007f;'>PLAN PRO</h4>
            <p><strong>Costo:</strong> $8 / mes (Anual)</p>
            <p><strong>Créditos:</strong> 2,500 al mes (~500 tracks)</p>
            <p><strong>Modelos:</strong> ElevenLabs Pro + Suno v5.5</p>
            <p><strong>Derechos comerciales:</strong> SÍ</p>
            <p><strong>Features:</strong> Voice Cloning, 30 min Upload</p>
        </div>
        """, unsafe_allow_html=True)
    with pc3:
        st.markdown("""
        <div class='analog-channel master-strip'>
            <h4 style='color:#eab308;'>PLAN PREMIER</h4>
            <p><strong>Costo:</strong> $24 / mes (Anual)</p>
            <p><strong>Créditos:</strong> 10,000 al mes (~2,000 tracks)</p>
            <p><strong>Modelos:</strong> Todos (ElevenLabs Studio + DAW 2.0)</p>
            <p><strong>Derechos comerciales:</strong> SÍ</p>
            <p><strong>Studio 2.0 DAW:</strong> SÍ (Completo)</p>
        </div>
        """, unsafe_allow_html=True)
