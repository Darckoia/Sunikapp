import streamlit as st
import time
import os
import requests
from datetime import datetime

# ==================== SUNO CREATE CORE ENGINE ====================
class SunoCreateEngine:
    def __init__(self):
        self.voces_preset = {
            "Masculino": {
                "Español (Chile) - Coa / Flaite Urbano": "es_cl_male_urbano",
                "Español (Chile) - Neutro Chileno": "es_cl_male_neutro",
                "Español (Latinoamérica) - Adam (Pro)": "pNInz6obpgDQGcFmaJgB",
                "Español (Castellano) - Arnold": "VR6AewLTigWG4xT1s5nC",
                "Inglés (EE.UU.) - Josh (Studio)": "TxGEqnscrfWFTf81Cj2q"
            },
            "Femenino": {
                "Español (Chile) - Coa / Flaite Urbano": "es_cl_female_urbano",
                "Español (Chile) - Neutro Chileno": "es_cl_female_neutro",
                "Español (Latinoamérica) - Rachel (Pro)": "21m00Tcm4TlvDq8ikWAM",
                "Español (Castellano) - Bella": "EXAVITQu4vr4xnSDxMaL",
                "Inglés (EE.UU.) - Domi": "AZnzlk1XvdvUeBnXmlld"
            }
        }
        os.makedirs("audio_cache", exist_ok=True)

    def obtener_voice_id(self, genero, acento):
        gen_key = "Masculino" if "male" in genero.lower() else "Femenino"
        return self.voces_preset.get(gen_key, {}).get(acento, "21m00Tcm4TlvDq8ikWAM")

suno_engine = SunoCreateEngine()

# ==================== ESTILOS UI SUNO.COM/CREATE ====================
st.set_page_config(page_title="Suno - Create & DAW Matrix", page_icon="🎵", layout="wide")

st.markdown("""
<style> 
.stApp { background: radial-gradient(circle at top center, #07090e 0%, #010204 100%); color: #e2e8f0; font-family: 'Courier New', Courier, monospace; } 
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

# BARRA DE CRÉDITOS Y TELEMETRÍA SUNO
st.markdown("<div style='display: flex; justify-content: space-between; background: #020306; padding: 10px 24px; border-bottom: 2px solid #1e293b; font-size: 0.75rem; color: #475569; letter-spacing:1px;'><span>SUNO.COM/CREATE // ENGINE ACTIVE</span><span>CREDITS REMAINING: 2,500 / 2,500 PRO PLAN</span></div>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #fff; letter-spacing: 6px; font-weight: 900; margin-top:20px; font-size:2.2rem;'>🪐 SUNO CREATE STUDIO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #38bdf8; font-size: 0.8rem; letter-spacing: 4px; margin-bottom: 30px;'>ESTUDIO OFICIAL DE GENERACIÓN Y COMPOSICIÓN MUSICAL</p>", unsafe_allow_html=True)

# BASE DE DATOS Y FEED EN TIEMPO REAL
if "db_tracks" not in st.session_state:
    st.session_state.db_tracks = [
        {"nombre": "Esquinas Oscuras (Trap CL v5.5)", "fecha": "08/2026", "perfil": "Flaite Urbano", "tipo": "Custom Mode"},
        {"nombre": "Sinfonía del Puerto (Neutro Mix)", "fecha": "08/2026", "perfil": "Neutro Chileno", "tipo": "Instrumental"}
    ]

# BARRA LATERAL (PANEL DE CONTROL DE PROMPTS Y RECURSOS)
with st.sidebar:
    st.markdown("### 🎛️ SUNO CREATE SETTINGS")
    modelo_suno = st.selectbox("Versión de Motor:", ["v5.5 Premier", "v4.5 Standard", "v3.5 Legacy"])
    solo_instrumental = st.checkbox("Solo Instrumental (Sin Voces)", value=False)
    st.markdown("---")
    st.markdown("### 🔑 API KEY & SERVICIOS")
    api_key_input = st.text_input("Suno API Key:", type="password", placeholder="Clave de API...")
    st.caption("Modo demostración integrado si no ingresas clave.")

# ==================== PESTAÑAS DE SUNO.COM ====================
tab_create, tab_studio, tab_library, tab_help, tab_about = st.tabs([
    "🎵 CREATE (SUNO.COM/CREATE)", 
    "🎛️ STUDIO 2.0 (DAW)", 
    "📁 MY LIBRARY & FEED", 
    "❓ HELP CENTER", 
    "ℹ️ ABOUT SUNO"
])

# ==================== PESTAÑA 1: CREATE ====================
with tab_create:
    custom_toggle = st.toggle("Custom Mode (Activar control de letras y estrofas)", value=True)
    
    col1, col2, col3 = st.columns([1.3, 1.3, 1.1], gap="large")
    
    with col1:
        st.markdown("<div class='analog-channel'><div class='hardware-header'><span>CH 01 // SONG DESCRIPTION</span><span>PROMPT BUS</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='lcd-display'>[STYLE & LYRICS MATRIX]<br>INSERTA TU CONCEPTO O LETRA COMPLETA</div>", unsafe_allow_html=True)
        
        if custom_toggle:
            st.markdown("<p style='font-size:0.75rem; color:#00ffcc; font-weight:bold;'>✍️ LYRICS (LETRA DE LA CANCIÓN):</p>", unsafe_allow_html=True)
            letra_input = st.text_area("Escribe tus versos marcados con etiquetas [Verse], [Chorus], [Bridge]:", placeholder="[Verse 1]\nCamino de noche por la ciudad...\n\n[Chorus]\nY no miro atrás...")
            
            if st.button("📝 GENERAR LETRA CON IA"):
                st.markdown("<div class='lcd-display'>[AUTO LYRICS GENERATED]<br>'De menor en la pobla buscando el destino...<br>Marcando la diferencia en el camino.'</div>", unsafe_allow_html=True)
            
            prompt_estilo = st.text_input("Style of Music (Estilo de Música):", placeholder="Ej: Reggaeton Chileno, Trap Urbano, tempo 95 BPM, bajo pesado...")
            titulo_song = st.text_input("Title (Título de la canción):", placeholder="Ej: Esquinas Oscuras")
        else:
            prompt_estilo = st.text_area("Song Description (Describe la canción que quieres crear):", placeholder="Ej: Una canción de Trap Urbano chileno sobre la superación con ritmo lento y melodía melancólica...")
            titulo_song = "Suno Track Generado"
            
        st.markdown("<div class='led-matrix'><div class='led-bulb active-green'></div><div class='led-bulb active-green'></div><div class='led-bulb active-green'></div><div class='led-bulb active-yellow'></div><div class='led-bulb'></div></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='analog-channel vocal-strip'><div class='hardware-header' style='color:#ff007f;'><span>CH 02 // VOCAL IDENTITY</span><span>PERSONA SELECTOR</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='lcd-display pink'>[VOICE ENGINE SUNO v5.5]<br>CONFIGURACIÓN DE PERSONA Y ACENTO</div>", unsafe_allow_html=True)
        
        genero_vocal = st.radio("Género Vocal:", ["Male (Masculino)", "Female (Femenino)"], horizontal=True)
        
        acento_geografico = st.selectbox(
            "Selección de Acento:", 
            [
                "Español (Chile) - Coa / Flaite Urbano",
                "Español (Chile) - Neutro Chileno",
                "Español (Latinoamérica) - Adam (Pro)",
                "Español (Castellano) - Arnold",
                "Inglés (EE.UU.) - Josh (Studio)"
            ]
        )
        
        voice_id_sel = suno_engine.obtener_voice_id(genero_vocal, acento_geografico)
        st.caption(f"🎙️ Profile Voice ID: `{voice_id_sel}`")
        
        opcion_source = st.selectbox("Audio Input / Cover Mode:", ["Sin Audio de Base", "Upload Audio (Sube muestra para transformar)", "Reuse Persona"])
        archivo_ref = st.file_uploader("Subir referencia audio (.wav, .mp3):", type=["wav", "mp3"])

    with col3:
        st.markdown("<div class='analog-channel master-strip'><div class='hardware-header' style='color:#eab308;'><span>CH 03 // GENERATION OUT</span><span>VARIATIONS & EXPORT</span></div></div>", unsafe_allow_html=True)
        st.markdown("<small style='font-size:0.7rem; color:#64748b;'>VU CLIP METER:</small><div class='led-matrix'><div class='led-bulb active-green'></div><div class='led-bulb active-green'></div><div class='led-bulb active-green'></div><div class='led-bulb active-yellow'></div><div class='led-bulb active-red'></div></div>", unsafe_allow_html=True)
        
        st.markdown("<p style='font-size:0.75rem; color:#eab308; font-weight:bold;'>GENERACIÓN EN PARALELO:</p>", unsafe_allow_html=True)
        st.caption("Suno genera 2 variaciones automáticas por cada intento (Part 1 y Part 2).")
        
        modo_stem = st.selectbox("Exportación de Pistas:", ["Full Stereo Audio", "Get Stems (Separar Voz e Instrumental)"])
        st.checkbox("Create Video Hooks (Formato TikTok/Reels)", value=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🔥 CREATE (GENERAR 2 VARIACIONES DE CANCIÓN)", use_container_width=True):
        with st.spinner(""):
            log_box = st.empty()
            p_bar = st.progress(0)
            
            pasos = [
                "[SUNO ENGINE] Conectando con servidor de composición...",
                f"[MODEL] Invocando modelo '{modelo_suno}'...",
                f"[VOICE] Inyectando perfil '{acento_geografico}'...",
                "[MASTER] Generando Pista v1 y Pista v2 en paralelo..."
            ]
            for idx, paso in enumerate(pasos):
                log_box.markdown(f"<p style='text-align:center; color:#00ffcc; font-size:0.85rem;'>{paso}</p>", unsafe_allow_html=True)
                p_bar.progress((idx + 1) * 25)
                time.sleep(0.6)
            log_box.empty()
            
            # Agregar a la biblioteca local
            st.session_state.db_tracks.insert(0, {"nombre": f"{titulo_song} (Part 1)", "fecha": "09/2026", "perfil": acento_geografico, "tipo": "Suno v5.5"})
            st.session_state.db_tracks.insert(0, {"nombre": f"{titulo_song} (Part 2)", "fecha": "09/2026", "perfil": acento_geografico, "tipo": "Suno v5.5"})
            
            st.success("🎯 2 VARIACIONES GENERADAS Y GUARDADAS EN TU BIBLIOTECA")
            
        st.markdown("### 🎵 VARIACIONES GENERADAS (SUNO FEED):")
        var_col1, var_col2 = st.columns(2)
        with var_col1:
            st.markdown(f"<div class='lcd-display yellow'><b>{titulo_song} (Part 1)</b><br>Duration: 3:42 | Model: {modelo_suno}</div>", unsafe_allow_html=True)
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
            st.download_button("📥 Descargar Part 1 (MP3/WAV)", data=b"part1", file_name=f"{titulo_song}_part1.mp3", use_container_width=True)
        with var_col2:
            st.markdown(f"<div class='lcd-display yellow'><b>{titulo_song} (Part 2)</b><br>Duration: 3:15 | Model: {modelo_suno}</div>", unsafe_allow_html=True)
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3")
            st.download_button("📥 Descargar Part 2 (MP3/WAV)", data=b"part2", file_name=f"{titulo_song}_part2.mp3", use_container_width=True)

# ==================== PESTAÑA 2: STUDIO 2.0 ====================
with tab_studio:
    st.markdown("<div class='analog-channel'><div class='hardware-header'><span>SUNO STUDIO 2.0 // MULTITRACK DAW EDITOR</span><span>PREMIER EDITION</span></div></div>", unsafe_allow_html=True)
    st.markdown("<div class='lcd-display'>[DAW TIMELINE ACTIVE]<br>EDICIÓN DE PISTAS GENERADAS // EXTENSIONES Y REEMPLAZO DE SECCIONES</div>", unsafe_allow_html=True)
    
    sc1, sc2 = st.columns([2, 1])
    with sc1:
        st.markdown("🎛️ **HERRAMIENTAS DE EDICIÓN DE TIEMPO:**")
        st.slider("Extend Track From (Extender desde segundo)", 0, 240, 120)
        st.text_input("Replace Section Lyrics (Cambiar letra de un verso):", placeholder="Escribe el nuevo verso para reemplazar...")
        st.slider("Automation Parameter (Filtro de Frecuencia)", 0, 100, 50)
    
    with sc2:
        st.markdown("🎚️ **MEZCLADOR DE STEMS DE LA CANCIÓN:**")
        st.slider("Vocal Level", 0, 100, 85)
        st.slider("Drums Level", 0, 100, 90)
        st.slider("Bass Level", 0, 100, 80)
        st.slider("Synths / Instruments", 0, 100, 75)

# ==================== PESTAÑA 3: LIBRARY ====================
with tab_library:
    st.markdown("### 📁 MY LIBRARY & GENERATION FEED")
    st.markdown("<div class='lcd-display'>TODAS LAS CREACIONES GUARDADAS // DERECHOS COMERCIALES RESERVADOS</div>", unsafe_allow_html=True)
    
    for track in st.session_state.db_tracks:
        st.markdown(f"""
        <div class='track-card'>
            <div>
                <strong>🎵 {track['nombre']}</strong><br>
                <small style='color:#94a3b8;'>Fecha: {track['fecha']} | Perfil: {track['perfil']} | Tipo: {track['tipo']}</small>
            </div>
            <span style='color:#10b981; font-size:0.75rem;'>COMMERCIAL RIGHTS SECURED</span>
        </div>
        """, unsafe_allow_html=True)

# ==================== PESTAÑA 4: HELP CENTER ====================
with tab_help:
    st.markdown("### ❓ HELP CENTER (HELP.SUNO.COM)")
    with st.expander("🎵 ¿Cómo funciona el Custom Mode en Suno Create?"):
        st.write("El Custom Mode te permite escribir tus propias letras y dividirlas mediante corchetes como `[Verse]`, `[Chorus]`, y `[Bridge]`, además de controlar de forma independiente el estilo de música.")

# ==================== PESTAÑA 5: ABOUT SUNO ====================
with tab_about:
    st.markdown("### ℹ️ ABOUT SUNO AI (SUNO.COM/ABOUT)")
    st.markdown("Suno está diseñado para permitir a cualquier persona crear música de calidad profesional a partir de texto o ideas líricas.")
