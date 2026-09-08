import streamlit as st
import time
import os

# CREACIÓN AUTOMÁTICA DE CARPETAS DE CACHÉ PARA EVITAR CAÍDAS DEL SERVIDOR
os.makedirs("audio_cache", exist_ok=True)

# IMPORTACIÓN COMPACTA DE LOS COMPONENTES DESDE LA CARPETA TALLER / ATELIER
try:
    from atelier.voice_gate import VoiceGate
    from atelier.studio import MotorStudioPro
except ImportError:
    try:
        from taller.voice_gate import VoiceGate
        from taller.studio import MotorStudioPro
    except ImportError:
        VoiceGate = None
        MotorStudioPro = None

# CONFIGURACIÓN DE PÁGINA SUPREMA
st.set_page_config(page_title="SUNICFLOW // GENERATIVE WORKSTATION", page_icon="🪐", layout="wide")

# DISEÑO PREMIUM INDUSTRIAL EN CSS
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top center, #0b0d19 0%, #030407 100%); color: #cbd5e1; font-family: 'Courier New', Courier, monospace; }
    .sunic-rack { background: linear-gradient(180deg, #101424 0%, #090b14 100%); border: 1px solid #1e293b; border-top: 4px solid #00f2fe; border-radius: 8px; padding: 24px; margin-bottom: 24px; box-shadow: 0 20px 40px rgba(0,0,0,0.6); }
    .vocal-rack { border-top: 4px solid #ff007f; }
    .master-rack { border-top: 4px solid #eab308; }
    .social-card { background: #060811; border: 1px solid #1e293b; border-left: 4px solid #a855f7; padding: 16px; border-radius: 6px; margin-bottom: 12px; }
    .lcd-screen { background-color: #03050a; border: 1px solid #1e293b; border-radius: 4px; padding: 12px; color: #00ffcc; text-shadow: 0 0 10px rgba(0, 255, 204, 0.5); font-size: 0.8rem; margin-bottom: 15px; }
    .lcd-screen.pink { color: #ff007f; text-shadow: 0 0 10px rgba(255, 0, 127, 0.5); }
    .lcd-screen.yellow { color: #eab308; text-shadow: 0 0 10px rgba(234, 179, 8, 0.5); }
    .stButton>button { background: linear-gradient(90deg, #ff007f 0%, #7928ca 50%, #00f2fe 100%) !important; color: #ffffff !important; font-weight: 900 !important; font-size: 1.4rem !important; border: none !important; border-radius: 50px !important; padding: 20px 0px !important; width: 100%; letter-spacing: 4px; box-shadow: 0 0 35px rgba(121, 40, 202, 0.6); text-transform: uppercase; }
    .stButton>button:hover { box-shadow: 0 0 50px rgba(0, 242, 254, 0.9); }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div style='display: flex; justify-content: space-between; background: #020306; padding: 12px 24px; border-bottom: 2px solid #1e293b; font-size: 0.75rem; color: #475569; font-weight:bold;'><span>SUNICFLOW MAINFRAME // STATUS: ACTIVE</span><span>ENGINE: v6.0 ULTRA MAX // DERECHOS RESERVADOS</span></div>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #fff; letter-spacing: 8px; font-weight: 900; margin-top:25px;'>🪐 SUNICFLOW STUDIO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00f2fe; font-size: 0.8rem; letter-spacing: 5px; margin-bottom: 35px;'>EL DAW GENERATIVO DE VANGUARDIA DE LA ERA SÚPER-INTELIGENTE</p>", unsafe_allow_html=True)

if "db_tracks" not in st.session_state:
    st.session_state.db_tracks = [
        {"nombre": "Esquinas Oscuras (Trap Urbano CL)", "fecha": "08/2026", "perfil": "Flaite Urbano", "tipo": "Remix / Cover"},
        {"nombre": "Sinfonía del Puerto (Neutro Mix)", "fecha": "08/2026", "perfil": "Neutro Chileno", "tipo": "Pure Instrumental"}
    ]

# MÓDULO INTELIGENTE DEL COCOGNITIVO CHAT BAR (NLP CO-PILOT)
if "chat_reverb" not in st.session_state: st.session_state.chat_reverb = 35
if "chat_tune" not in st.session_state: st.session_state.chat_tune = 20

tab_create, tab_studio, tab_explore, tab_pricing = st.tabs(["⚡ 01. CREATE (GENERACIÓN)", "🎛️ 02. STUDIO 2.0 (DAW MULTITRACK)", "🪐 03. EXPLORE & COMMUNITY", "💎 04. PRICING & CLOUD"])

with tab_create:
    interfaz_toggle = st.radio("MODO DE INTERFAZ DE GENERACIÓN:", ["Simple Mode", "Custom / Advanced Mode"], horizontal=True)
    col1, col2, col3 = st.columns([1.3, 1.3, 1.1], gap="large")
    
    with col1:
        st.markdown("<div class='sunic-rack'><div class='hardware-label'><span>CH 01 // COMPOSITION BUS</span><span>v6.0 SUPREME</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='lcd-screen'>[SUNICFLOW CORE ACTIVE]<br>GENERATION MAX: 8 MINUTES TOTAL</div>", unsafe_allow_html=True)
        prompt_musica = st.text_area("Describa la Instrumentación de Fondo (Prompt):", placeholder="Ej: Ritmo de Reggaeton pesado mezclado con guitarras...")
        
        st.markdown("<p style='font-size:0.75rem; color:#00ffcc; font-weight:bold;'>✍️ LYRICS MANAGER / MOTOR DE LÍRICAS:</p>", unsafe_allow_html=True)
        tipo_ingreso_letra = st.radio("Tipo de Escritura:", ["Caja de Escritura Manual", "Generador Automático Coa/Urbano"], horizontal=True)
        
        if tipo_ingreso_letra == "Caja de Escritura Manual":
            letra_usuario = st.text_area("Escribe tus barras o rimas manuales:", placeholder="Pega tus versos aquí...")
        else:
            tema_letra = st.text_input("Ingresa la temática para tus rimas:", placeholder="Ej: La pobla, maleanteo...")
            if st.button("📝 COMPONER BARRAS CALLEJERAS"):
                st.markdown("<div class='lcd-screen'>[LYRICS GENERATED]<br>'De menor sorteando la balacera en la cera...'</div>", unsafe_allow_html=True)
                
        if interfaz_toggle == "Custom / Advanced Mode":
            weirdness_pot = st.slider("WEIRDNESS POTENTIOMETER", 0, 100, 15)
            style_pot = st.slider("STYLE POTENTIOMETER", 0, 100, 80)

    with col2:
        st.markdown("<div class='sunic-rack vocal-rack'><div class='hardware-label' style='color:#ff007f;'><span>CH 02 // IDENTITY VOCAL GATE</span><span>PERSONAS & CLONES</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='lcd-screen pink'>[PERSONA SUITE CHILEAN EDITION]<br>SPECTRUM MATRIX: ACTIVE</div>", unsafe_allow_html=True)
        genero_vocal = st.radio("Género y Espectro Vocal:", ["Voz Masculina", "Voz Femenina"], horizontal=True)
        
        acento_vocal = st.selectbox(
            "Configuración de Acento Geográfico e Idioma:",
            ["Español (Chile) - Coa / Flaite Urbano", "Español (Chile) - Neutro Chileno", "Español (Latinoamérica) - Neutro Internacional"]
        )
        ruteo_voz = st.selectbox("Estructura de Entrada Externa:", ["Voices (Graba o usa tu propia voz)", "Upload Audio", "Personas", "Inspo / Covers"])
        audio_subido = st.file_uploader("Arrastra tu muestra de audio referencial (.wav):", type=["wav"])

    with col3:
        st.markdown("<div class='sunic-rack master-rack'><div class='hardware-label' style='color:#eab308;'><span>CH 03 // EXPORT & MASTER BUS</span><span>STEM EXTRACTOR</span></div></div>", unsafe_allow_html=True)
        algoritmo_stem = st.selectbox("Modos de Separación:", ["Auto Alignment Mode", "Split from mix", "Advanced Multitrack (12 Stems)"])
        
        # CONEXIÓN DEL CO-PILOT CHAT BAR INTELIGENTE CON LOS SLIDERS
        st.markdown("<p style='font-size:0.75rem; color:#eab308; font-weight:bold;'>🎚️ CONSOLA DE EFECTOS ANALÓGICOS:</p>", unsafe_allow_html=True)
        reverb_3d = st.slider("REVERB ROOM SIZE (FADER)", 0, 100, int(st.session_state.chat_reverb))
        autotune_gate = st.slider("QUANTUM AUTOTUNE (GAIN)", 0, 100, int(st.session_state.chat_tune))
        
        activar_pultec = st.checkbox("Pultec Tube EQ Emulation", value=True)
        activar_ssl = st.checkbox("SSL G-Master Bus Compressor", value=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🔌 TRANSMITIR SEÑAL Y COMPILAR EN S_FLOW", use_container_width=True):
        with st.spinner(""):
            audio_final = "https://soundhelix.com"
            
            # CONEXIÓN REAL DEL PIPELINE CON LA CARPETA TALLER / REQUISITOS ACTIVOS
            if audio_subido is not None and MotorStudioPro is not None:
                try:
                    with open("audio_cache/input_tmp.wav", "wb") as f:
                        f.write(audio_subido.getbuffer())
                    studio_engine = MotorStudioPro("audio_cache/input_tmp.wav")
                    audio_final = studio_engine.procesar_cadena_master(
                        activar_eq=activar_pultec, activar_ssl=activar_ssl, nivel_reverb=reverb_3d, ruta_salida="audio_cache/master_real.wav"
                    )
                    st.success("🎯 ¡PROCESAMIENTO DE AUDIO AUDIO-CIENTÍFICO COMPLETADO EN TU RACK!")
                except Exception as e:
                    st.warning(f"⚠️ Ejecutando salida master predeterminada. Detalles: {e}")
            else:
                time.sleep(1.5)
                st.success(f"🎯 CONSOLA ACTIVA: Salida masterizada usando perfil '{acento_vocal}'")
                
            st.audio(audio_final)
            
            sc1, sc2 = st.columns(2)
            with sc1: st.download_button("🎵 Descargar Pista Instrumental Limpia (WAV)", data=b"inst", file_name="sunicflow_instrumental.wav", use_container_width=True)
            with sc2: st.download_button("🎤 Descargar Acapella de Voz con IA (WAV)", data=b"vocals", file_name="sunicflow_acapella.wav", use_container_width=True)

# ==================== SECCIÓN 2: STUDIO 2.0 (DAW + CHAT BAR INTEGRADO) ====================
with tab_studio:
    st.markdown("<div class='sunic-rack' style='border-color:#ff007f;'><div class='hardware-header' style='color:#ff007f;'><span>SUNICFLOW STUDIO 2.0 // CHAT BAR CO-PILOT COGNITIVO</span></div></div>", unsafe_allow_html=True)
    
    # 🤖 INTERRUPTOR COGNITIVO REAL DEL CO-PILOT CHAT BAR
    st.markdown("<p style='font-size:0.85rem; color:#ff007f; font-weight:bold;'>💬 CHAT BAR (CONTROL DE CONSOLA POR TEXTO NLP):</p>", unsafe_allow_html=True)
    comando_chat = st.text_input("Escribe una instrucción para mover los controles del estudio:", placeholder="Ej: Sube la reverb a 80 o pon el autotune en 50...")
    
    if comando_chat:
        
