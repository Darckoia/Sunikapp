import streamlit as st
import time

# 1. CONFIGURACIÓN DE PÁGINA E INYECTADO DE DISEÑO PREMIUM (CSS)
st.set_page_config(page_title="Atelier Studio AI", page_icon="🎛️", layout="wide")

# Forzar tema oscuro profesional con CSS puro
st.markdown("""
    <style>
    /* Fondo principal y textos */
    .stApp {
        background-color: #0d0e12;
        color: #e2e8f0;
    }
    
    /* Contenedores con estética de Hardware de Estudio */
    .studio-card {
        background: linear-gradient(145deg, #14161d, #1a1d26);
        border: 1px solid #2a2f3d;
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* Título principal estilo Neón */
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(to right, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 5px;
    }
    
    .subtitle {
        text-align: center;
        color: #718096;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    
    /* Botón de generación estilizado */
    .stButton>button {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #0d0e12 !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        letter-spacing: 1px;
        border-radius: 30px !important;
        border: none !important;
        padding: 15px 30px !important;
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(0, 242, 254, 0.7);
    }
    
    /* Headers de secciones */
    h3 {
        color: #00f2fe !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        border-bottom: 1px solid #2a2f3d;
        padding-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado de la App
st.markdown('<p class="main-title">🎛️ ATELIER STUDIO AI</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Estudio de producción musical neural • Next-Gen Engine</p>', unsafe_allow_html=True)

# 2. DISTRIBUCIÓN DEL ESTUDIO EN PANTALLA
col1, col2 = st.columns(2, gap="medium")

with col1:
    # Bloque 1: Motor de Composición
    st.markdown('<div class="studio-card">', unsafe_allow_html=True)
    st.markdown("<h3>🎹 MOTOR DE COMPOSICIÓN (PROMPT MULTI-GÉNERO)</h3>", unsafe_allow_html=True)
    prompt = st.text_area("Describe la instrumentación y ambiente musical:", placeholder="Ej: Fusión Cyberpunk con Flamenco, sintetizadores analógicos y batería pesada de Trap...")
    genero = st.selectbox("Estructura de ritmo base:", ["Fusión Híbrida Inteligente", "Urban Trap / Hip-Hop", "Synthwave / Cyberpunk", "Techno / Club Dance", "Rock Progresivo / Industrial"])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Bloque 2: Clonación y Voces
    st.markdown('<div class="studio-card">', unsafe_allow_html=True)
    st.markdown("<h3>🗣️ SÍNTESIS DE VOZ GLOBAL & ACENTOS</h3>", unsafe_allow_html=True)
    genero_voz = st.radio("Género de la voz neural:", ["Masculino (Barítono/Tenor)", "Femenino (Soprano/Melódica)"], horizontal=True)
    acento = st.selectbox("Región y acento del mundo:", ["Español (Latinoamérica - México/Colombia)", "Español (Castellano - España)", "Inglés (EE.UU. - Urban Studio)", "Inglés (Reino Unido - Deep Accent)"])
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Bloque 3: Ingesta de Audio Propio
    st.markdown('<div class="studio-card">', unsafe_allow_html=True)
    st.markdown("<h3>🎙️ RACK DE GRABACIÓN PRIVADA</h3>", unsafe_allow_html=True)
    st.write("Sube tu toma de voz (acapella) para aplicar el tratamiento de hardware analógico virtual.")
    archivo_voz = st.file_uploader("Arrastra tu archivo aquí (.mp3, .wav)", type=["wav", "mp3"])
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Bloque 4: Consola de Mezcla (Efectos)
    st.markdown('<div class="studio-card">', unsafe_allow_html=True)
    st.markdown("<h3>🎚️ CONSOLA DE EFECTOS (PRODUCTOR PRO)</h3>", unsafe_allow_html=True)
    reverb = st.slider("Espacialidad / Reverb Estéreo", 0, 100, 35, help="Simula el tamaño de la sala de grabación.")
    tuning = st.slider("Corrección de Tono (Autotune)", 0, 100, 15, help="Fuerza la afinación perfecta sobre la escala musical.")
    st.checkbox("Masterización Analógica Virtual (Compresor SSL + Ecualizador Pultec)", value=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 3. ACCIÓN PRINCIPAL DE PRODUCCIÓN
if st.button("🎛️ MASTERIZAR Y GENERAR TRACK", use_container_width=True):
    with st.spinner("🎸 Procesando señales en el rack analógico..."):
        progreso = st.progress(0)
        for i in range(1, 6):
            progreso.progress(i * 20)
            time.sleep(0.8)
        
        st.success("🎯 ¡Producción finalizada con éxito!")
        
        # Tarjeta contenedora del reproductor musical premium
        st.markdown('<div class="studio-card" style="border: 1px solid #00f2fe;">', unsafe_allow_html=True)
        st.markdown("<h3 style='color: #00f2fe !important;'>🎧 MONITOR DE AUDIO EN VIVO (MASTER FINAL)</h3>", unsafe_allow_html=True)
        st.audio("https://soundhelix.com")
        st.markdown('</div>', unsafe_allow_html=True)
