# Suno UI clone para Streamlit Community Cloud
# Deploy: share.streamlit.io -> repo -> Main file path: streamlit_app.py

from __future__ import annotations

from datetime import datetime

import streamlit as st

st.set_page_config(
    page_title="Suno",
    page_icon="S",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
html, body, [class*="css"], .stApp {
  font-family: Inter, Segoe UI, Helvetica, Arial, sans-serif;
}
#MainMenu, footer, header, .stDeployButton {visibility: hidden; height: 0;}
.stApp { background: #121212; color: #f5f5f5; }
.block-container { padding: 0.6rem 1rem 6.5rem 1rem; max-width: 460px; }
section[data-testid="stSidebar"] { background: #0e0e12; }
.logo { font-weight: 800; letter-spacing: .2em; font-size: 1.1rem; }
.bar { display:flex; justify-content:space-between; align-items:center; margin: 4px 0 10px; }
.pill { background:#2a2a2e; border-radius:999px; padding:4px 10px; font-size:12px; }
.take { background:#18181b; border:1px solid #2a2a2e; border-radius:14px; padding:12px; margin:8px 0; }
.muted { color:#a1a1aa; font-size:12px; }
div.stButton > button {
  width: 100%;
  border: 0;
  border-radius: 999px;
  padding: .8rem 1rem;
  font-weight: 700;
  color: #fff;
  background: linear-gradient(90deg,#ec4899,#f97316,#eab308);
}
.stTextArea textarea, .stTextInput input {
  background: #0f0f12;
  color: #eee;
  border-radius: 12px;
}
</style>
""",
    unsafe_allow_html=True,
)

MODELS = {
    "Free": ["v4.5-all"],
    "Pro": ["v4", "v4.5", "v4.5+", "v5", "v5.5"],
    "Premier": ["v4", "v4.5", "v4.5+", "v5", "v5.5"],
}
CREDITS = {"Free": 50, "Pro": 2500, "Premier": 10000}
COST = {"Simple": 10, "Custom": 10, "Sounds": 5, "Extend": 5}

TOOLS = [
    ("Simple", "Create", "Free", "Descripcion unica. 2 takes."),
    ("Custom", "Create", "Free", "Title, lyrics, styles, exclude, sliders."),
    ("Sounds", "Create", "Pro", "One-shot o loop + BPM + key."),
    ("Add Audio", "Create", "Free", "Upload mp3/wav. En Cloud no persiste."),
    ("Voices", "Identidad", "Pro", "Voz propia. Aqui solo selector demo."),
    ("Personas", "Identidad", "Pro", "Reusar vibe de una take."),
    ("Custom Models", "Identidad", "Pro", "Hasta 3. Demo de nombre."),
    ("Inspo", "Create", "Pro", "Referencia de estilo."),
    ("Extend", "Edit", "Free", "Alarga una take de Library."),
    ("Stems", "Edit", "Pro", "Lista de stems demo."),
    ("Studio 2.0", "Studio", "Premier", "Faders + chat. Sin VST ni MIDI hardware."),
]


def boot() -> None:
    s = st.session_state
    s.setdefault("plan", "Free")
    s.setdefault("credits", 50)
    s.setdefault("library", [])
    s.setdefault("chat", [])
    s.setdefault("playing", "Sin pista")


def pay(kind: str) -> bool:
    n = COST[kind]
    if st.session_state.credits < n:
        st.error("Sin creditos. Sidebar > Recargar.")
        return False
    st.session_state.credits -= n
    return True


def push(title: str, style: str, mode: str, model: str) -> None:
    now = datetime.now().strftime("%H:%M:%S")
    for tag in ("A", "B"):
        st.session_state.library.insert(
            0,
            {
                "title": f"{title} ({tag})",
                "style": style,
                "mode": mode,
                "model": model,
                "time": now,
            },
        )
    st.session_state.playing = f"{title} (A)"


boot()

with st.sidebar:
    st.write("**SUNO**")
    page = st.radio(
        "Paginas",
        ["Create", "Library", "Studio", "Explore", "Account"],
        label_visibility="collapsed",
    )
    plan = st.selectbox(
        "Plan",
        ["Free", "Pro", "Premier"],
        index=["Free", "Pro", "Premier"].index(st.session_state.plan),
    )
    if plan != st.session_state.plan:
        st.session_state.plan = plan
        st.session_state.credits = CREDITS[plan]
        st.rerun()
    if st.button("Recargar creditos"):
        st.session_state.credits = CREDITS[st.session_state.plan]
        st.rerun()
    st.caption("Cloud: el estado vive en la sesion. Al recargar el browser se pierde.")

paid = st.session_state.plan != "Free"
premier = st.session_state.plan == "Premier"
models = MODELS[st.session_state.plan]
prefer = "v5.5" if paid else "v4.5-all"

st.markdown(
    f'<div class="bar"><span class="logo">SUNO</span>'
    f'<span class="pill">{st.session_state.plan} · {st.session_state.credits}</span></div>',
    unsafe_allow_html=True,
)

if page == "Create":
    st.title("Create")
    mode = st.radio("Modo", ["Simple", "Custom", "Sounds"], horizontal=True)
    model = st.selectbox("Modelo", models, index=models.index(prefer) if prefer in models else 0)
    instrumental = st.toggle("Instrumental")
    title, style, lyrics = "Untitled", "", ""

    if mode == "Simple":
        style = st.text_area("Styles", placeholder="Resistente, tambores ligeros, rap afro")
        if not instrumental:
            lyrics = st.text_area("Lyrics", placeholder="Letra o vacio")
    elif mode == "Custom":
        title = st.text_input("Title", "Midnight Rain")
        style = st.text_input("Styles", "dark synth pop, analog bass")
        lyrics = st.text_area("Lyrics", "[Verse]\n...\n[Chorus]\n...")
        st.text_input("Exclude styles")
        st.radio("Vocal gender", ["Auto", "Male", "Female"], horizontal=True)
        st.slider("Weirdness", 0, 100, 50)
        st.slider("Style influence", 0, 100, 50)
        st.slider("Audio influence", 0, 100, 25)
        st.file_uploader("Add Audio", type=["mp3", "wav", "m4a"])
        st.selectbox("Voices", ["Ninguna"] + (["Mi voz"] if paid else ["Requiere Pro"]))
        st.selectbox("Inspo", ["Ninguna"] + (["Playlist"] if paid else ["Requiere Pro"]))
    else:
        if not paid:
            st.caption("Sounds es Pro en Suno. Demo abierta.")
        style = st.text_area("Sound", placeholder="whoosh, vinyl loop")
        x, y, z = st.columns(3)
        x.selectbox("Tipo", ["one-shot", "loop"])
        y.text_input("BPM", "92")
        z.text_input("Key", "A minor")

    if st.button("Create"):
        if not (style or lyrics):
            st.error("Escribe styles o lyrics.")
        elif pay(mode):
            push(title, style or lyrics[:60], mode, model)
            st.rerun()

    for t in st.session_state.library[:2]:
        st.markdown(
            f"<div class='take'><b>{t['title']}</b>"
            f"<div class='muted'>{t['model']} · {t['mode']} · {t['time']}</div>"
            f"<div class='muted'>{t['style']}</div></div>",
            unsafe_allow_html=True,
        )

elif page == "Library":
    st.title("Library")
    tabs = st.tabs(["All", "Stems", "Personas", "Uploads"])
    with tabs[0]:
        if not st.session_state.library:
            st.caption("Vacio.")
        for i, t in enumerate(st.session_state.library):
            st.write(f"**{t['title']}**")
            st.caption(f"{t['model']} · {t['mode']} · {t['style']}")
            if st.button("Extend", key=f"ex{i}") and pay("Extend"):
                push(t["title"] + " ext", t["style"], "Extend", t["model"])
                st.rerun()
    with tabs[1]:
        st.caption("Pro: vocals, drums, bass, other. Premier: split avanzado.")
        if paid and st.session_state.library:
            st.write("vocals\ndrums\nbass\nguitar\nkeys\nfx")
    with tabs[2]:
        if paid:
            name = st.text_input("Nombre Persona")
            if st.button("Guardar Persona") and name:
                st.success(f"Persona demo: {name}")
        else:
            st.caption("Requiere Pro.")
    with tabs[3]:
        st.file_uploader("Upload", type=["mp3", "wav"], key="up2")
        st.caption("Cloud no guarda el archivo al recargar.")

elif page == "Studio":
    st.title("Studio 2.0")
    st.caption("Premier en Suno. Cloud: solo faders y chat. Sin MIDI/VST.")
    if not premier:
        st.caption("Plan actual sin Studio real.")
    a, b = st.columns(2)
    a.metric("BPM", 120)
    b.metric("Compas", "4/4")
    for n in ("Vocals", "Drums", "Bass MIDI", "Synth"):
        st.slider(n, 0, 100, 70)
    q = st.chat_input("Chat Studio")
    if q:
        st.session_state.chat.append(q)
    for m in st.session_state.chat:
        st.write("Tu:", m)
        st.write("Studio: demo. En Cloud no se sintetiza audio.")

elif page == "Explore":
    st.title("Explore")
    q = st.text_input("Buscar")
    st.caption("Sin red a suno.com desde Cloud en este clone.")
    if q:
        st.write("Demo:", q)

else:
    st.title("Account")
    st.write("**Free** — $0 — 50 creditos/dia — v4.5-all — no comercial")
    st.write("**Pro** — $8/mes anual — 2500 — v5.5 — Voices, stems, Sounds")
    st.write("**Premier** — $24/mes anual — 10000 — Studio 2.0")
    st.subheader("Herramientas")
    for n, a, p, d in TOOLS:
        st.write(f"**{n}** · {a} · min {p} — {d}")
    st.caption("Precios 2026 suno.com/pricing. Verificar en vivo.")

st.caption(f"Now playing: {st.session_state.playing} · sesion local Cloud")
