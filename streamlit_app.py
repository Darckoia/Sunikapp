import streamlit as st
import os

os.makedirs("audio_cache", exist_ok=True)

st.set_page_config(
    page_title="SUNICFLOW // GENERATIVE MULTI-CHANNEL DAW",
    page_icon="🪐",
    layout="wide"
)

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
    .social-card {
        background: #060811;
        border: 1px solid #1e293b;
        border-left: 4px solid #a855f7;
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
        font-size: 1.1rem !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 16px 0px !important;
        width: 100%;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .led-bar { display: flex; gap: 6px; margin-bottom: 12px; }
    .led-dot { width: 8px; height: 8px; border-radius: 50%; background: #111422; }
    .led-dot.green { background: #22c55e; box-shadow: 0 0 10px #22c55e; }
    .led-dot.yellow { background: #eab308; box-shadow: 0 0 10px #eab308; }
    .led-dot.red { background: #ef4444; box-shadow: 0 0 10px #ef4444; }
    .hardware-label {
        font-size: 0.8rem;
        font-weight: 800;
        color: #475569;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 15px;
        display: flex;
        justify-content: space-between;
        border-bottom: 1px solid #1e293b;
        padding-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    "<div style='display:flex;justify-content:space-between;background:#020306;padding:12px 24px;border-bottom:2px solid #1e293b;font-size:0.75rem;color:#475569;font-weight:bold;'>"
    "<span>SUNICFLOW MAINFRAME // STATUS: ACTIVE</span>"
    "<span>ENGINE: v6.0</span></div>",
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align:center;color:#fff;letter-spacing:6px;font-weight:900;margin-top:20px;'>🪐 SUNICFLOW STUDIO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#00f2fe;font-size:0.8rem;letter-spacing:3px;margin-bottom:25px;'>GENERATIVE DAW • MODO AUTOMÁTICO + CONSOLA</p>", unsafe_allow_html=True)

if "db_tracks" not in st.session_state:
    st.session_state.db_tracks = [
        {"nombre": "Esquinas Oscuras (Trap Urbano CL)", "fecha": "08/09/2026", "perfil": "Flaite Urbano", "tipo": "Remix / Cover"},
        {"nombre": "Sinfonía del Puerto (Neutro Mix)", "fecha": "08/09/2026", "perfil": "Neutro Chileno", "tipo": "Pure Instrumental"}
    ]

if "chat_reverb" not in st.session_state:
    st.session_state.chat_reverb = 35
if "chat_tune" not in st.session_state:
    st.session_state.chat_tune = 20

tab_create, tab_studio, tab_explore, tab_pricing = st.tabs([
    "⚡ CREATE",
    "🎛️ STUDIO",
    "🪐 EXPLORE",
    "💎 PLANES"
])

with tab_create:
    interfaz_toggle = st.radio(
        "Modo de generación:",
        ["Simple Mode", "Custom / Advanced Mode"],
        horizontal=True
    )

    col1, col2, col3 = st.columns([1.3, 1.3, 1.1], gap="large")

    with col1:
        st.markdown("<div class='sunic-rack'><div class='hardware-label'><span>CH 01 // COMPOSITION</span><span>v6.0</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='lcd-screen'>[SUNICFLOW CORE ACTIVE]<br>STATUS: ONLINE</div>", unsafe_allow_html=True)
        prompt_musica = st.text_area(
            "Describe la canción:",
            placeholder="Ej: Trap chileno oscuro, voz masculina, 2:30...",
            key="txt_prompt"
        )

        st.markdown("<p style='font-size:0.75rem;color:#00ffcc;font-weight:bold;'>✍️ LETRAS</p>", unsafe_allow_html=True)
        tipo_ingreso_letra = st.radio(
            "Tipo de escritura:",
            ["Caja de Escritura Manual", "Generador Automático"],
            horizontal=True
        )

        letra_usuario = ""
        tema_letra = ""
        if tipo_ingreso_letra == "Caja de Escritura Manual":
            letra_usuario = st.text_area("Escribe tus letras:", placeholder="Pega tus versos aquí...")
        else:
            tema_letra = st.text_input("Temática para las rimas:", placeholder="Ej: La pobla, superación...")
            if st.button("📝 COMPONER BARRAS"):
                st.markdown(
                    "<div class='lcd-screen'>[LYRICS GENERATED]<br>"
                    "De menor sorteando la balacera en la cera,<br>"
                    "voh sai hermano que andamos a nuestra manera.</div>",
                    unsafe_allow_html=True
                )

        if interfaz_toggle == "Custom / Advanced Mode":
            st.markdown("---")
            exclusiones = st.text_input("Excluir:", placeholder="Ej: No heavy bass...")
            weirdness_pot = st.slider("WEIRDNESS", 0, 100, 15)
            style_pot = st.slider("STYLE", 0, 100, 80)

        st.markdown("<div class='led-bar'><div class='led-dot green'></div><div class='led-dot green'></div><div class='led-dot green'></div><div class='led-dot yellow'></div><div class='led-dot'></div></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='sunic-rack vocal-rack'><div class='hardware-label' style='color:#ff007f;'><span>CH 02 // VOZ</span><span>PERSONAS</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='lcd-screen pink'>[PERSONA SUITE]<br>IDENTITY SECURED</div>", unsafe_allow_html=True)
        genero_vocal = st.radio(
            "Género vocal:",
            ["Voz Masculina (Barítono)", "Voz Femenina (Soprano)"],
            horizontal=True
        )
        acento_vocal = st.selectbox(
            "Acento / idioma:",
            [
                "Español (Chile) - Coa / Flaite Urbano",
                "Español (Chile) - Neutro Chileno",
                "Español (Latinoamérica) - Neutro Internacional",
                "Español (Castellano - España)",
                "Inglés (EE.UU. - Hip-Hop Studio)",
                "Inglés (Reino Unido - London Drill)"
            ]
        )
        ruteo_voz = st.selectbox(
            "Entrada:",
            ["Voices (Usa tu propia voz)", "Upload Audio", "Personas", "Inspo / Covers / Remix"]
        )
        audio_subido = st.file_uploader("Sube audio de referencia (.wav / .mp3):", type=["wav", "mp3"])

    with col3:
        st.markdown("<div class='sunic-rack master-rack'><div class='hardware-label' style='color:#eab308;'><span>CH 03 // MASTER</span><span>STEMS</span></div></div>", unsafe_allow_html=True)
        st.markdown("<div class='led-bar'><div class='led-dot green'></div><div class='led-dot green'></div><div class='led-dot green'></div><div class='led-dot yellow'></div><div class='led-dot red'></div></div>", unsafe_allow_html=True)
        algoritmo_stem = st.selectbox(
            "Separación:",
            ["Auto Alignment Mode", "Split from mix", "Advanced Multitrack"]
        )
        reverb_3d = st.slider("REVERB", 0, 100, int(st.session_state.chat_reverb))
        autotune_gate = st.slider("AUTOTUNE", 0, 100, int(st.session_state.chat_tune))
        activar_pultec = st.checkbox("Pultec Tube EQ", value=True)
        activar_ssl = st.checkbox("SSL G-Master Compressor", value=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔌 TRANSMITIR SEÑAL Y COMPILAR", use_container_width=True):
        st.success("Composición registrada en la biblioteca.")
        nuevo_nombre = prompt_musica.strip() if prompt_musica else "Nueva Mezcla Generada"
        nombre_corto = (nuevo_nombre[:30] + "...") if len(nuevo_nombre) > 30 else nuevo_nombre
        st.session_state.db_tracks.insert(0, {
            "nombre": nombre_corto,
            "fecha": "08/09/2026",
            "perfil": acento_vocal,
            "tipo": ruteo_voz
        })
        st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
        st.caption("Audio de prueba. La generación real se conecta después.")

with tab_studio:
    st.subheader("Studio 2.0")
    st.info("Editor básico. Aquí se listan las pistas generadas.")
    if st.session_state.db_tracks:
        for track in st.session_state.db_tracks:
            st.markdown(f"**{track['nombre']}**  \n{track['perfil']} · {track['tipo']} · {track['fecha']}")
            st.divider()
    else:
        st.caption("Aún no hay pistas.")

with tab_explore:
    st.subheader("Explore & Community")
    st.write("Trending now on Sunicflow")
    for track in st.session_state.db_tracks:
        st.markdown(
            f"<div class='social-card'><b>{track['nombre']}</b><br>{track['perfil']} · {track['tipo']}</div>",
            unsafe_allow_html=True
        )

with tab_pricing:
    st.subheader("Planes")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### Free\n- 10 canciones/día\n- Sin uso comercial")
    with c2:
        st.markdown("### Pro\n- Más créditos\n- Derechos comerciales")
    with c3:
        st.markdown("### Premier\n- Studio completo\n- Stems avanzados")
