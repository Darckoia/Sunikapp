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
    .lcd-screen.pink { color: #ff007f; text-shadow: 0 0 10px rgba(255, 0, 127, 0.
