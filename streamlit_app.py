import streamlit as st
import time
import os
import requests
from datetime import datetime

# ==================== MÓDULO SIGHT & VOICE ENGINE (SUNO + ELEVENLABS CORE) ====================
class SunoEngineCore:
    def __init__(self):
        self.voces_preset = {
            "Masculino": {
                "Español (Chile) - Coa / Flaite Urbano": "es_cl_male_urbano",
                "Español (Chile) - Neutro Chileno": "es_cl_male_neutro",
                "Español (Latinoamérica) - Adam (Pro Voice)": "pNInz6obpgDQGcFmaJgB",
                "Español (Castellano) - Arnold": "VR6AewLTigWG4xT1s5nC",
                "Inglés (EE.UU.) - Josh (Studio)": "TxGEqnscrfWFTf81Cj2q"
            },
            "Femenino": {
                "Español (Chile) - Coa / Flaite Urbano": "es_cl_female_urbano",
                "Español (Chile) - Neutro Chileno": "es_cl_female_neutro",
                "Español (Latinoamérica) - Rachel (Pro Voice)": "21m00Tcm4TlvDq8ikWAM",
                "Español (Castellano) - Bella": "EXAVITQu4vr4xnSDxMaL",
                "Inglés (EE.UU.) - Domi": "AZnzlk1XvdvUeBnXmlld"
            }
        }
        os.makedirs("audio_cache", exist_ok=True)

    def obtener_voice_id(self, genero, acento):
        gen_key = "Masculino" if "male" in genero.lower() else "Femenino"
        return self.voces_preset.get(gen_key, {}).get(acento, "21m00Tcm4TlvDq8ikWAM")

# Inicializar motor
suno_core = SunoEngineCore()

# ==================== CONFIGURACIÓN Y ESTILOS UI SUNO DAW ====================
st.set_page_config(page_title="SUNO AI PRO - ATELIER DAW MATRIX", page_icon="🎵", layout="wide")

st.markdown("""
<style> 
.stApp { background: radial-gradient(circle at top center, #06070d 0%, #010204 100%); color: #e2e8f0; font-family: 'Courier New', Courier, monospace; } 
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

# BARRA DE ENCABEZADO SUNO GLOBAL
st.markdown("<div style='display: flex; justify-content: space-between; background: #020306; padding: 10px 24px; border-bottom: 2px solid #1e293b; font-size: 0.75rem; color: #475569; letter-spacing:1px;'><span>SUNO ENGINE: ONLINE // MODEL: v5.5 PREMIER & STUDIO 2.0</span><span>HELP CENTER INTEGRATED</span></div>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #fff; letter-spacing: 6px; font-weight: 900; margin-top:20px; font-size:2.2rem;'>🪐 SUNO AI MATRIX DAW</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #38bdf8; font-size: 0.8rem; letter-spacing: 4px; margin-bottom: 30px;'>CREA MÚSICA COMPLETA, SEPARA STEMS Y GENERA VOCES IA</p>", unsafe_allow_html=True)

# BASE DE DATOS LOCAL
if "db_tracks" not in st.session_state:
    st.session_state.db_tracks = [
        {"nombre": "Esquinas Oscuras (Trap Urbano CL)", "fecha": "08/2026", "perfil": "Flaite Urbano", "tipo": "Suno v5.5 Remix"},
        {"nombre": "Sinfonía del Puerto (Neutro Mix)", "fecha": "08/2026", "perfil": "Neutro Chileno", "tipo": "Instrumental Pure"}
    ]

# BARRA LATERAL
with st.sidebar:
    st.markdown("### 🎛️ SUNO MODEL SETTINGS")
    modelo_suno = st.selectbox("Versión del Motor Suno:", ["v5.5 Premier (Recomendado)", "v4.5 Standard", "v3.5 Legacy"])
    st.markdown("---")
    st.markdown("### 🔑 API KEYS & INTEGRACIONES")
    api_key_input = st.text_input("Suno / ElevenLabs API Key:", type="password", placeholder="Clave de API...")
    st.caption("Si no ingresas clave, la app operará en modo simulación de DAW.")

# ==================== PESTAÑAS PRINCIPALES DE SUNO ====================
tab_create, tab_studio, tab_library, tab_help, tab_about = st.tabs([
    "🎵 CREATE (GENERADOR)", 
    "🎛️ STUDIO 2.0 (DAW)", 
    "📁 BIBLIOTECA & STEMS", 
    "❓ HELP CENTER (AYUDA)", 
    "ℹ️ SOBRE SUNO"
])

# ==================== PESTAÑA 1: CREATE ====================
with tab_create:
    modo_creacion = st.radio("MODO DE INTERFAZ:", ["Simple Mode (Solo estilo)", "Custom / Advanced Mode (Letra + Estilo)"], horizontal=True)
    
    col1, col2, col3 = st.columns([1.3, 1.3, 1.1], gap="large")
    
    with col1:
        st.markdown("<div class='analog-channel'><div class='hardware-header'><span>CH 01 // COMPOSITION BUS</span><span>SUNO COMPILER</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='lcd-display'>[PROMPT MATRIX ACTIVE]<br>GENERACIÓN DE MÚSICA DE HASTA 8 MINS<br>ESTRUCTURA: INTRO/VERSO/CORO/OUTRO</div>", unsafe_allow_html=True)
        
        prompt_estilo = st.text_area("Estilo Musical / Prompt:", placeholder="Ej: Reggaeton chileno con guitarras acústicas, ritmo pesado de club, tempo 95 BPM...")
        
        if modo_creacion == "Custom / Advanced Mode (Letra + Estilo)":
            st.markdown("<p style='font-size:0.75rem; color:#00ffcc; font-weight:bold; margin-top:15px;'>✍️ COMPOSITOR DE LETRA:</p>", unsafe_allow_html=True)
            tipo_letra = st.radio("Modo de Letra:", ["Letra Manual / Estrofas", "Generar Letra con IA"], horizontal=True)
            if tipo_letra == "Letra Manual / Estrofas":
                letra_texto = st.text_area("Escribe la letra de tu canción:", placeholder="[Verse 1]\nDe menor en la calle buscando el destino...\n\n[Chorus]\nY ahora andamos coronando...")
            else:
                tema_generar = st.text_input("Concepto de la canción:", placeholder="Ej: Superación personal, noche urbana...")
                if st.button("📝 GENERAR LETRA AUTOMÁTICA"):
                    st.markdown("<div class='lcd-display'>[SUNO LYRICIST]<br>'De menor en el barrio soñando despierto...<br>Hoy salimos a la calle con el combo completo.'</div>", unsafe_allow_html=True)
            
            exclusiones = st.text_input("Excluir instrumentos/estilos:", placeholder="Ej: No piano, no edm synth...")
        st.markdown("<div class='led-matrix'><div class='led-bulb active-green'></div><div class='led-bulb active-green'></div><div class='led-bulb active-green'></div><div class='led-bulb active-yellow'></div><div class='led-bulb'></div></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='analog-channel vocal-strip'><div class='hardware-header' style='color:#ff007f;'><span>CH 02 // REPERTORIO VOCAL</span><span>PERSONAS & VOICES</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='lcd-display pink'>[VOCAL ENGINE READY]<br>SELECCIÓN DE ACENTO Y GÉNERO NEURAL</div>", unsafe_allow_html=True)
        
        genero_vocal = st.radio("Género de Voz:", ["Male (Masculino)", "Female (Femenino)"], horizontal=True)
        
        acento_geografico = st.selectbox(
            "Perfil e Idioma Vocal:", 
            [
                "Español (Chile) - Coa / Flaite Urbano",
                "Español (Chile) - Neutro Chileno",
                "Español (Latinoamérica) - Adam (Pro Voice)",
                "Español (Castellano) - Arnold",
                "Inglés (EE.UU.) - Josh (Studio)"
            ]
        )
        
        voice_id_sel = suno_core.obtener_voice_id(genero_vocal, acento_geografico)
        st.caption(f"🎙️ Voice Profile ID: `{voice_id_sel}`")
        
        opcion_origen = st.selectbox("Audio Base u Origen:", ["Solo Prompt / Texto", "Upload Audio (Sube muestra de 30 seg)", "Cover / Remix de Track Existente"])
        archivo_ref = st.file_uploader("Sube audio de muestra (.wav, .mp3):", type=["wav", "mp3"])

    with col3:
        st.markdown("<div class='analog-channel master-strip'><div class='hardware-header' style='color:#eab308;'><span>CH 03 // MASTERING & STEMS</span><span>EXPORT CONTROL</span></div></div>", unsafe_allow_html=True)
        st.markdown("<small style='font-size:0.7rem; color:#64748b;'>VU CLIP METER:</small><div class='led-matrix'><div class='led-bulb active-green'></div><div class='led-bulb active-green'></div><div class='led-bulb active-green'></div><div class='led-bulb active-yellow'></div><div class='led-bulb active-red'></div></div>", unsafe_allow_html=True)
        
        st.markdown("<p style='font-size:0.75rem; color:#eab308; font-weight:bold;'>SEPARACIÓN DE PISTAS (STEMS):</p>", unsafe_allow_html=True)
        modo_stem = st.selectbox("Formato de Exportación:", ["Full Mix (Canción Completa)", "Separate Vocals + Instrumental", "Multi-Track Stems (Drums, Bass, Vocals, Synths)"])
        
        st.checkbox("Suno Audio Isolation (Eliminar Ruido de Fondo)", value=True)
        st.checkbox("Create Hooks (Versión corta para TikTok/Reels)", value=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 GENERAR CANCIÓN COMPLETA CON SUNO AI", use_container_width=True):
        with st.spinner(""):
            log_box = st.empty()
            p_bar = st.progress(0)
            
            pasos = [
                "[SUNO CORE] Analizando estructura del prompt y armonías...",
                f"[MODEL] Invocando motor Suno '{modelo_suno}'...",
                f"[VOICE GATE] Asignando perfil de voz '{acento_geografico}'...",
                "[MASTERING] Renderizando audio estéreo a 32-bit / 48kHz..."
            ]
            for idx, paso in enumerate(pasos):
                log_box.markdown(f"<p style='text-align:center; color:#00ffcc; font-size:0.85rem;'>{paso}</p>", unsafe_allow_html=True)
                p_bar.progress((idx + 1) * 25)
                time.sleep(0.6)
            log_box.empty()
            
            st.success("🎯 PISTA COMPUESTA Y MASTERIZADA EXITOSAMENTE")
            
        st.markdown("<div class='lcd-display yellow'>STEREO MONITOR // MASTER AUDIO GENERATED</div>", unsafe_allow_html=True)
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        sc1, sc2 = st.columns(2)
        with sc1:
            st.download_button("📥 Descargar Base Instrumental (WAV)", data=b"instrumental", file_name="suno_instrumental.wav", use_container_width=True)
        with sc2:
            st.download_button("🎤 Descargar Voz / Acapella (WAV)", data=b"vocal", file_name="suno_vocal.wav", use_container_width=True)

# ==================== PESTAÑA 2: STUDIO 2.0 ====================
with tab_studio:
    st.markdown("<div class='analog-channel'><div class='hardware-header'><span>SUNO STUDIO 2.0 // WORKSTATION MULTITRACK</span><span>PREMIER EDITION</span></div></div>", unsafe_allow_html=True)
    st.markdown("<div class='lcd-display'>[DAW TIMELINE DIGITAL ACTIVE]<br>EDICIÓN DE CANCIONES POR SECCIONES / CORTES / EXTENSIONES</div>", unsafe_allow_html=True)
    
    sc1, sc2 = st.columns([2, 1])
    with sc1:
        st.markdown("🎛️ **CONTROLES DE EDICIÓN Y LÍNEA DE TIEMPO:**")
        st.slider("Extend Track (Ampliar duración en minutos)", 1, 8, 4)
        st.slider("Crop Section (Recortar inicio/fin)", 0, 240, (0, 180))
        st.text_input("Replace Section Prompt (Reemplazar un verso o solo):", placeholder="Ej: Cambia el solo de guitarra por un sintetizador synthwave...")
        st.checkbox("Infill Loop (Generar loop infinito transparente)", value=False)
    
    with sc2:
        st.markdown("🎚️ **MEZCLADOR DE PISTAS (STEMS):**")
        st.slider("Volumen Voces", 0, 100, 85)
        st.slider("Volumen Batería / Drums", 0, 100, 90)
        st.slider("Volumen Bajo / Bass", 0, 100, 80)
        st.slider("Volumen Instrumentos / Synths", 0, 100, 75)

# ==================== PESTAÑA 3: LIBRARY ====================
with tab_library:
    st.markdown("### 📁 MIS CANCIONES Y PROYECTOS PRIVADOS")
    st.markdown("<div class='lcd-display'>TODAS LAS CREACIONES GUARDADAS CON DERECHOS COMERCIALES</div>", unsafe_allow_html=True)
    
    for track in st.session_state.db_tracks:
        st.markdown(f"""
        <div class='track-card'>
            <div>
                <strong>🎵 {track['nombre']}</strong><br>
                <small style='color:#94a3b8;'>Fecha: {track['fecha']} | Perfil: {track['perfil']} | Tipo: {track['tipo']}</small>
            </div>
            <span style='color:#10b981; font-size:0.75rem;'>DERECHOS COMERCIALES RESERVADOS</span>
        </div>
        """, unsafe_allow_html=True)

# ==================== PESTAÑA 4: HELP CENTER ====================
with tab_help:
    st.markdown("### ❓ CENTRO DE AYUDA Y PREGUNTAS FRECUENTES (HELP.SUNO.COM)")
    st.markdown("<div class='lcd-display pink'>GUÍA DE USO COMPLETA DE SUNO AI</div>", unsafe_allow_html=True)
    
    with st.expander("🎵 ¿Cómo crear una canción desde cero?"):
        st.write("Ve a la pestaña **CREATE**, escribe la descripción del estilo musical en la casilla de Prompt o activa el modo avanzado para añadir tus propias letras organizadas por estrofas como `[Verse]` y `[Chorus]`.")
        
    with st.expander("⚖️ ¿Tengo los derechos comerciales de las canciones?"):
        st.write("Sí. Si utilizas un plan Pro o Premier, posees el 100% de los derechos comerciales de la música que generes para subirla a Spotify, Apple Music, YouTube o monetize en plataformas.")

    with st.expander("🎤 ¿Cómo separar la voz de la música (Stems)?"):
        st.write("En la columna derecha de la pestaña **CREATE**, en la sección *Separación de pistas*, selecciona 'Separate Vocals + Instrumental'. Al terminar la compilación tendrás botones de descarga independientes.")

    with st.expander("🛠️ ¿Cómo extender o recortar una canción existente?"):
        st.write("Entra a la pestaña **STUDIO 2.0 (DAW)** para ajustar la línea de tiempo, agregar minutos extra a una composición o reemplazar un fragmento específico.")

# ==================== PESTAÑA 5: ABOUT SUNO ====================
with tab_about:
    st.markdown("### ℹ️ SOBRE SUNO AI (SUNO.COM/ABOUT)")
    st.markdown("""
    <div class='analog-channel'>
        <h4>Misión de Suno</h4>
        <p>Suno está construyendo un futuro donde cualquiera puede hacer gran música. Diseñado para democratizar la producción musical mediante inteligencia artificial, permitiendo a artistas, productores y mentes creativas componer temas completos a partir de ideas simples o letras complejas.</p>
        <hr style='border-color:#1e293b;'>
        <h4>Ecosistema de Herramientas Integradas:</h4>
        <ul>
            <li><strong>Suno Studio DAW:</strong> Edición multipista profesional en el navegador.</li>
            <li><strong>Personas & Voices:</strong> Asignación y clonación de perfiles de voz neurales.</li>
            <li><strong>Audio-to-Audio / Covers:</strong> Modificación de pistas de audio de referencia.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
