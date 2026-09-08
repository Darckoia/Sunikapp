"""Suno Interface Clone — Streamlit
Pega este archivo como streamlit_app.py
Ejecuta: streamlit run streamlit_app.py
No llama a la API oficial de Suno. Generacion demo local.
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st

st.set_page_config(
    page_title="Suno Interface Clone",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """
<style>
#MainMenu, footer, header {visibility: hidden;}
.stApp { background: #121212; color: #f4f4f5; }
section[data-testid="stSidebar"] { background: #0e0e12; }
div[data-testid="stSidebar"] * { color: #e4e4e7; }
.block-container { padding-top: 1.2rem; max-width: 1100px; }
.suno-brand { font-weight: 800; letter-spacing: 0.18em; font-size: 1.15rem; }
.credits { background: #27272a; border-radius: 999px; padding: 4px 12px; font-size: 0.8rem; display: inline-block; }
.take-card { background: #18181b; border: 1px solid #27272a; border-radius: 14px; padding: 14px; margin-bottom: 10px; }
.muted { color: #a1a1aa; font-size: 0.85rem; }
hr { border-color: #27272a; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

MODELS_FREE = ["v4.5-all"]
MODELS_PAID = ["v4", "v4.5", "v4.5+", "v5", "v5.5"]
LYRIC_TAGS = "[Verse] [Pre-Chorus] [Chorus] [Bridge] [Intro] [Outro] [Hook]"

PLANS = {
    "Free": {
        "precio": "$0",
        "creditos": "50 / dia (~10 canciones)",
        "modelos": "v4.5-all",
        "comercial": "No",
        "studio": "No",
        "stems": "No",
        "extras": "My Taste, Create Simple/Custom basico",
    },
    "Pro": {
        "precio": "$8/mes anual ($10 mensual)",
        "creditos": "2.500 / mes (~500 canciones)",
        "modelos": "v4 a v5.5",
        "comercial": "Si",
        "studio": "No",
        "stems": "Auto + Split from mix (hasta 12)",
        "extras": "Voices, Personas, Custom Models (3), Crop, Replace, Sounds, Inspo",
    },
    "Premier": {
        "precio": "$24/mes anual ($30 mensual)",
        "creditos": "10.000 / mes (~2.000 canciones)",
        "modelos": "v4 a v5.5",
        "comercial": "Si",
        "studio": "Si (Studio 2.0)",
        "stems": "Auto + Split + Advanced split",
        "extras": "Todo Pro + MIDI, FX, synth, chat, export 32-bit/48 kHz",
    },
}

FEATURES = [
    ("Simple Mode", "Create", "Free", "Un campo de descripcion. Devuelve 2 takes."),
    ("Custom Mode", "Create", "Free", "Letra, estilo, exclude, titulo, instrumental."),
    ("Sounds", "Create", "Pro", "One-shots y loops con BPM y tonalidad."),
    ("Add Audio", "Create", "Free", "Subir o grabar referencia / tarareo."),
    ("Voices", "Identidad", "Pro", "Tu voz verificada. Privada."),
    ("Personas", "Identidad", "Pro", "Esencia de una cancion reutilizable."),
    ("Custom Models", "Identidad", "Pro", "Hasta 3 modelos afinados con tu catalogo."),
    ("My Taste", "Identidad", "Free", "Personaliza por lo que escuchas."),
    ("Inspo", "Create", "Pro", "Canciones o playlist como referencia."),
    ("Extend", "Edicion", "Free", "Alarga o cambia el final. Puede pasar 8 min."),
    ("Crop", "Edicion", "Pro", "Recorta inicio o final."),
    ("Replace Section", "Edicion", "Pro", "Sustituye un tramo."),
    ("Remaster", "Edicion", "Pago", "Pasa temas viejos a un modelo nuevo."),
    ("Cover / Remix", "Edicion", "Free", "Reinterpreta estilo sobre material existente."),
    ("Stems", "Edicion", "Pro", "Hasta ~12 pistas. Premier: split avanzado."),
    ("Workspaces", "Org", "Free", "Carpetas aparte de Library."),
    ("Studio 2.0", "Studio", "Premier", "DAW web: MIDI, FX, synth, chat. Chrome. Sin VST."),
]

STUDIO_TOOLS = [
    ("Chat Bar", "Pide clips, MIDI, plugins y arreglos en texto."),
    ("Transport", "Play, loop, metronomo, tempo, compas."),
    ("Timeline", "Pistas audio/MIDI, clips, take lanes."),
    ("MIDI", "Piano roll, grabacion, audio a MIDI, teclado PC."),
    ("Wavetable synth", "Osciladores, filtros, envelopes, LFOs. Sin VST."),
    ("Efectos", "Comp, convolution, delay, distortion, EQ, gate, reverb + plugins por chat."),
    ("Automatizacion", "Volumen, paneo y parametros en el tiempo."),
    ("Grabacion", "Audio/MIDI, count-in, pre-roll, latencia."),
    ("Library dock", "Atajo 4. Arrastra al timeline o al chat."),
    ("Export", "Multitrack 32-bit/48 kHz sin tope (Premier)."),
]


def init_state() -> None:
    ss = st.session_state
    ss.setdefault("credits", 50)
    ss.setdefault("plan", "Free")
    ss.setdefault("library", [])
    ss.setdefault("studio_chat", [])
    ss.setdefault("page", "Create")


def spend_credits(n: int = 10) -> bool:
    if st.session_state.credits < n:
        return False
    st.session_state.credits -= n
    return True


def add_takes(title: str, style: str, mode: str, model: str) -> None:
    now = datetime.now().strftime("%H:%M")
    for label in ("Take A", "Take B"):
        st.session_state.library.insert(
            0,
            {
                "title": f"{title} ({label})",
                "style": style,
                "mode": mode,
                "model": model,
                "time": now,
                "plan": st.session_state.plan,
            },
        )


init_state()

with st.sidebar:
    st.markdown('<div class="suno-brand">SUNO CLONE</div>', unsafe_allow_html=True)
    st.caption("Replica local 2026. No es el producto oficial.")
    page = st.radio(
        "Navegacion",
        ["Home", "Explore", "Create", "Studio", "Library", "Account"],
        index=2,
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.session_state.plan = st.selectbox(
        "Plan",
        ["Free", "Pro", "Premier"],
        index=["Free", "Pro", "Premier"].index(st.session_state.plan),
    )
    st.markdown(
        f'<div class="credits">Creditos {st.session_state.credits}</div>',
        unsafe_allow_html=True,
    )
    if st.button("Recargar creditos demo"):
        st.session_state.credits = (
            50 if st.session_state.plan == "Free"
            else 2500 if st.session_state.plan == "Pro"
            else 10000
        )
        st.rerun()

paid = st.session_state.plan in ("Pro", "Premier")
premier = st.session_state.plan == "Premier"
models = MODELS_PAID if paid else MODELS_FREE
default_model = "v5.5" if paid else "v4.5-all"

if page == "Home":
    st.title("Home")
    st.write("Haz que la musica que tienes en la cabeza sea real.")
    st.write("100M+ personas han creado musica en Suno. Funding reportado: 775M USD. Web, iOS y Android.")
    st.info("Usa Create para generar. Studio es Premier. Voices y Custom Models son Pro/Premier.")

elif page == "Explore":
    st.title("Explore")
    q = st.text_input("Buscar canciones, creadores, playlists, generos")
    st.caption("En el producto real: trending, staff picks y perfiles publicos.")
    if q:
        st.write(f"Demo: resultados para `{q}` no conectados a Suno.")

elif page == "Create":
    st.title("Create")
    c1, c2, c3 = st.columns([2, 2, 2])
    with c1:
        mode = st.radio("Modo", ["Simple", "Custom", "Sounds"], horizontal=True)
    with c2:
        model = st.selectbox(
            "Modelo",
            models,
            index=models.index(default_model) if default_model in models else 0,
        )
    with c3:
        instrumental = st.toggle("Instrumental", value=False)

    title = "Untitled"
    style = ""
    lyrics = ""

    if mode == "Simple":
        style = st.text_area(
            "Song description",
            placeholder="A moody late-night synth pop song about leaving the city",
            height=140,
        )
    elif mode == "Custom":
        title = st.text_input("Title", "Midnight Rain")
        st.caption(f"Tags utiles: {LYRIC_TAGS}")
        lyrics = st.text_area(
            "Lyrics",
            "[Verse]\nEmpty streets, neon on the glass\n\n[Chorus]\nMidnight rain, I call your name",
            height=160,
        )
        style = st.text_input(
            "Style of music",
            "dark synth pop, analog bass, intimate female vocal",
        )
        exclude = st.text_input("Exclude styles", placeholder="country, metal screams")
        g1, g2 = st.columns(2)
        with g1:
            vocal = st.radio("Vocal gender", ["Auto", "Male", "Female"], horizontal=True)
        with g2:
            weird = st.slider("Weirdness", 0, 100, 30)
        inf = st.slider("Style influence", 0, 100, 70)
        a1, a2, a3 = st.columns(3)
        with a1:
            st.file_uploader("Add Audio", type=["mp3", "wav", "m4a"])
        with a2:
            st.selectbox("Voices", ["Ninguna"] + (["Mi voz"] if paid else ["Requiere Pro"]))
        with a3:
            st.selectbox("Inspo", ["Ninguna"] + (["Playlist ref"] if paid else ["Requiere Pro"]))
        _ = exclude, vocal, weird, inf
    else:
        if not paid:
            st.warning("Sounds es Pro/Premier en el producto real. Demo desbloqueada aqui.")
        style = st.text_area(
            "Sound description",
            placeholder="cinematic whoosh, vinyl crackle loop in A minor",
            height=100,
        )
        s1, s2, s3 = st.columns(3)
        with s1:
            st.selectbox("Tipo", ["one-shot", "loop"])
        with s2:
            st.text_input("BPM", "92")
        with s3:
            st.text_input("Key", "A minor")

    cost = 5 if mode == "Sounds" else 10
    if st.button("Create", type="primary", use_container_width=True):
        if not (style or lyrics):
            st.error("Escribe una descripcion o letra.")
        elif not spend_credits(cost):
            st.error("Sin creditos. Recarga en la barra o cambia de plan.")
        else:
            add_takes(title if title else "Untitled", style or "(instrumental / lyrics)", mode, model)
            st.success(f"2 takes demo. -{cost} creditos. Mira Library.")
            st.rerun()

    if st.session_state.library:
        st.subheader("Ultimas takes")
        for track in st.session_state.library[:4]:
            st.markdown(
                f"<div class='take-card'><b>{track['title']}</b>"
                f"<div class='muted'>{track['model']} · {track['mode']} · {track['time']}</div>"
                f"<div class='muted'>{track['style']}</div></div>",
                unsafe_allow_html=True,
            )

elif page == "Studio":
    st.title("Studio 2.0")
    if not premier:
        st.warning("Studio es Premier. Puedes explorar la maqueta.")
    st.caption("Chrome recomendado. Web MIDI no va en Safari. Sin VST/AU de terceros.")
    t1, t2, t3, t4 = st.columns(4)
    t1.metric("BPM", "120")
    t2.metric("Compas", "4/4")
    t3.button("Rec")
    t4.button("Play")
    st.progress(0.35, text="Playhead demo")
    st.write("Pistas")
    for name in ("Vocals", "Drums", "Bass MIDI", "Synth"):
        st.slider(name, 0, 100, 75 if name != "Synth" else 60)
    prompt = st.chat_input("Chat: make a warm tape saturation and a MIDI bassline")
    if prompt:
        st.session_state.studio_chat.append(prompt)
    for msg in st.session_state.studio_chat:
        st.chat_message("user").write(msg)
        st.chat_message("assistant").write("Demo: en Studio real esto genera clip, MIDI o plugin.")
    st.subheader("Herramientas")
    for name, desc in STUDIO_TOOLS:
        st.write(f"**{name}** — {desc}")

elif page == "Library":
    st.title("Library")
    tabs = st.tabs(["All", "Liked", "Stems", "Uploads", "Personas", "Workspaces", "Studio Projects"])
    with tabs[0]:
        if not st.session_state.library:
            st.caption("Vacio. Genera en Create.")
        for track in st.session_state.library:
            c1, c2, c3 = st.columns([4, 2, 2])
            c1.write(f"**{track['title']}**")
            c1.caption(track["style"])
            c2.caption(f"{track['model']} · {track['mode']}")
            if c3.button("Extend", key=f"ex-{track['title']}-{track['time']}"):
                if spend_credits(5):
                    add_takes(track["title"] + " ext", track["style"], "Extend", track["model"])
                    st.rerun()
                else:
                    st.error("Sin creditos")
    with tabs[4]:
        st.caption("Personas: guarda voz + vibe de una cancion. En Create viven dentro de Voices.")
        if paid:
            st.text_input("Nombre de Persona")
            st.button("Crear Persona demo")
        else:
            st.info("Requiere Pro/Premier.")

elif page == "Account":
    st.title("Account / Planes")
    st.caption("Precios segun suno.com/pricing 2026. Verifica en vivo antes de cotizar.")
    cols = st.columns(3)
    for col, (name, p) in zip(cols, PLANS.items()):
        with col:
            st.subheader(name)
            st.write(p["precio"])
            st.write(p["creditos"])
            st.write(f"Modelos: {p['modelos']}")
            st.write(f"Comercial: {p['comercial']}")
            st.write(f"Studio: {p['studio']}")
            st.write(f"Stems: {p['stems']}")
            st.caption(p["extras"])
    st.subheader("Herramientas")
    for name, area, plan, desc in FEATURES:
        st.write(f"**{name}** · {area} · min {plan} — {desc}")
    st.caption("Fuentes: suno.com, help.suno.com, blog v5.5 (mar 2026), Studio 2.0 (ago 2026).")
