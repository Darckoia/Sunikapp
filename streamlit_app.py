# Suno-like Create para Streamlit Cloud
# requirements.txt -> streamlit>=1.36.0

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
#MainMenu, footer, header, .stDeployButton, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"] {display:none !important;}
.stApp { background:#121212 !important; color:#f4f4f5 !important; }
.block-container { padding:12px 16px 88px 16px !important; max-width:430px !important; }
section[data-testid="stSidebar"] { background:#0b0b0d !important; }

h1 { font-size:2.05rem !important; font-weight:800 !important; letter-spacing:-0.03em; margin:8px 0 14px !important; }
p, label, .stMarkdown { color:#d4d4d8 !important; }

div[data-testid="stTextArea"] textarea,
div[data-testid="stTextInput"] input {
  background:#18181b !important;
  color:#f4f4f5 !important;
  border:1px solid #3f3f46 !important;
  border-radius:14px !important;
  font-size:0.95rem !important;
}
div[data-testid="stTextArea"] textarea { min-height:84px !important; }

div[data-baseweb="select"] > div {
  background:#18181b !important;
  border:1px solid #3f3f46 !important;
  border-radius:14px !important;
  color:#f4f4f5 !important;
  box-shadow:none !important;
}
div[data-baseweb="select"] { border-color:#3f3f46 !important; }

[data-testid="stWidgetLabel"] { color:#a1a1aa !important; font-size:13px !important; }

div.stButton > button {
  border-radius:999px !important;
  font-weight:650 !important;
  border:1px solid #3f3f46 !important;
  background:#18181b !important;
  color:#e4e4e7 !important;
}
div.stButton > button[kind="primary"],
div.stButton > button[data-testid="baseButton-primary"] {
  background: linear-gradient(90deg,#ec4899,#f97316,#eab308) !important;
  color:#fff !important;
  border:0 !important;
  font-weight:800 !important;
  padding:0.8rem 1rem !important;
}

.hdr { display:flex; justify-content:space-between; align-items:center; margin:2px 0 6px; }
.logo { font-weight:800; letter-spacing:.28em; font-size:15px; }
.chip { background:#27272a; color:#e4e4e7; border-radius:999px; padding:6px 10px; font-size:12px; }
.card { background:#18181b; border:1px solid #27272a; border-radius:16px; padding:12px; margin:8px 0; }
.muted { color:#a1a1aa; font-size:12px; }
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


def boot() -> None:
    s = st.session_state
    s.setdefault("plan", "Free")
    s.setdefault("credits", 50)
    s.setdefault("library", [])
    s.setdefault("mode", "Simple")
    s.setdefault("page", "Create")
    s.setdefault("chat", [])


boot()

with st.sidebar:
    st.write("SUNO")
    st.session_state.page = st.radio(
        "Pagina",
        ["Create", "Library", "Studio", "Account"],
        index=["Create", "Library", "Studio", "Account"].index(st.session_state.page),
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

paid = st.session_state.plan != "Free"
models = MODELS[st.session_state.plan]
prefer = "v5.5" if paid else "v4.5-all"

st.markdown(
    f'<div class="hdr"><div class="logo">SUNO</div>'
    f'<div class="chip">{st.session_state.plan} · {st.session_state.credits}</div></div>',
    unsafe_allow_html=True,
)

page = st.session_state.page

if page == "Create":
    st.title("Create")

    b1, b2, b3 = st.columns(3)
    if b1.button("Simple", use_container_width=True):
        st.session_state.mode = "Simple"
        st.rerun()
    if b2.button("Custom", use_container_width=True):
        st.session_state.mode = "Custom"
        st.rerun()
    if b3.button("Sounds", use_container_width=True):
        st.session_state.mode = "Sounds"
        st.rerun()
    st.caption("Modo: " + st.session_state.mode)

    model = st.selectbox(
        "Modelo",
        models,
        index=models.index(prefer) if prefer in models else 0,
    )
    instrumental = st.toggle("Instrumental")
    title, style, lyrics = "Untitled", "", ""
    mode = st.session_state.mode

    if mode == "Simple":
        style = st.text_area("Styles", placeholder="Resistente, tambores ligeros, rap afro")
        if not instrumental:
            lyrics = st.text_area("Lyrics", placeholder="Letra o vacio")
    elif mode == "Custom":
        title = st.text_input("Title", "Midnight Rain")
        style = st.text_input("Styles", "dark synth pop, analog bass")
        lyrics = st.text_area("Lyrics", "[Verse]\n...\n[Chorus]\n...")
        st.text_input("Exclude styles")
        st.radio("Vocal gender", ["Auto", "Male", "Female"], horizontal=True, label_visibility="collapsed")
        st.slider("Weirdness", 0, 100, 50)
        st.slider("Style influence", 0, 100, 70)
        st.file_uploader("Add Audio", type=["mp3", "wav", "m4a"])
    else:
        style = st.text_area("Sound", placeholder="whoosh, vinyl loop")
        c1, c2, c3 = st.columns(3)
        c1.selectbox("Tipo", ["one-shot", "loop"])
        c2.text_input("BPM", "92")
        c3.text_input("Key", "A minor")

    if st.button("Create", type="primary"):
        if not (style or lyrics):
            st.error("Escribe styles o lyrics.")
        elif st.session_state.credits < 10:
            st.error("Sin creditos.")
        else:
            st.session_state.credits -= 10
            now = datetime.now().strftime("%H:%M")
            for tag in ("A", "B"):
                st.session_state.library.insert(
                    0,
                    {
                        "title": f"{title} ({tag})",
                        "style": style or lyrics[:50],
                        "mode": mode,
                        "model": model,
                        "time": now,
                    },
                )
            st.rerun()

    for t in st.session_state.library[:2]:
        st.markdown(
            f"<div class='card'><b>{t['title']}</b>"
            f"<div class='muted'>{t['model']} · {t['mode']} · {t['time']}</div>"
            f"<div class='muted'>{t['style']}</div></div>",
            unsafe_allow_html=True,
        )

elif page == "Library":
    st.title("Library")
    if not st.session_state.library:
        st.caption("Vacio.")
    for t in st.session_state.library:
        st.markdown(
            f"<div class='card'><b>{t['title']}</b><div class='muted'>{t['style']}</div></div>",
            unsafe_allow_html=True,
        )

elif page == "Studio":
    st.title("Studio 2.0")
    st.caption("En Cloud: faders y chat. Sin MIDI/VST.")
    a, b = st.columns(2)
    a.metric("BPM", 120)
    b.metric("Compas", "4/4")
    for n in ("Vocals", "Drums", "Bass", "Synth"):
        st.slider(n, 0, 100, 70)
    q = st.chat_input("Chat Studio")
    if q:
        st.session_state.chat.append(q)
    for m in st.session_state.chat:
        st.write(m)

else:
    st.title("Account")
    st.write("Free $0 · Pro $8/mes anual · Premier $24/mes anual")
    st.caption("Suno 2026. Verificar en suno.com/pricing.")
