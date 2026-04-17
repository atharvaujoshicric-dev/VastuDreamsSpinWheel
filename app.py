import streamlit as st
import random
import time
import base64
import json
from datetime import datetime
import streamlit.components.v1 as components

# Prize data matching the image clockwise starting from the segment at 0-60 degrees
# According to your image, the yellow segment is now at the top-right (0 to 60 deg)
prizes = [
    {"label": "75,000 OFF", "icon": "💰"},          # 0-60 deg (Yellow)
    {"label": "50,000 OFF", "icon": "💵"},          # 60-120 deg (Pink)
    {"label": "1 LACS OFF", "icon": "💰"},           # 120-180 deg (Orange)
    {"label": "BETTER LUCK NEXT TIME", "icon": "❌"}, # 180-240 deg (White)
    {"label": "1.5 LACS OFF", "icon": "💵"},         # 240-300 deg (Pink)
    {"label": "2 LACS OFF", "icon": "💎"}            # 300-360 deg (Orange)
]

st.set_page_config(page_title="VASTU DREAMS III — Wheel of Fortune", layout="centered")

# --- PREMIUM LUXURY CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Raleway:wght@300;400;500&display=swap');

    :root {
        --gold: #C9A84C;
        --dark: #0B0C0F;
    }

    html, body, .stApp {
        background-color: var(--dark) !important;
        font-family: 'Raleway', sans-serif;
        overflow: hidden;
    }

    .block-container {
        padding-top: 1rem !important;
        max-width: 450px !important;
    }

    #MainMenu, footer, header {visibility: hidden;}
    
    .stButton > button {
        background: linear-gradient(135deg, #C9A84C, #8B6914) !important;
        color: var(--dark) !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 700 !important;
        width: 100%;
        border-radius: 2px !important;
    }
    </style>
""", unsafe_allow_html=True)

def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except:
        return ""

wheel_base64 = get_image_base64("wheel.png")

if 'winner_name' not in st.session_state:
    st.session_state.winner_name = ""

# =====================
# 1. LEAD GENERATION
# =====================
if not st.session_state.winner_name:
    st.markdown("""
    <div style="text-align: center; padding: 30px 0 10px;">
        <h1 style="font-family: 'Cinzel'; color: #E8C97A; letter-spacing: 0.1em; margin: 0; font-size: 1.8rem;">VASTU DREAMS III</h1>
        <p style="font-size: 0.7rem; color: rgba(255,255,255,0.4); letter-spacing: 0.2em; margin: 5px 0 0; text-transform: uppercase;">Premium Residences</p>
    </div>
    """, unsafe_allow_html=True)
    
    name = st.text_input("Full Name", placeholder="Your Name")
    phone = st.text_input("Phone Number", placeholder="Your Phone")
    agree = st.checkbox("I agree to terms")

    if st.button("REGISTER & SPIN"):
        if name and phone and agree:
            st.session_state.winner_name = name
            st.rerun()
        else:
            st.error("Please fill all fields.")

# =====================
# 2. GAME PHASE
# =====================
else:
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <h2 style="font-family: 'Cinzel'; color: #E8C97A; font-size: 1.4rem; margin:0;">VASTU DREAMS III</h2>
        <p style="color: grey; font-size: 0.8rem;">Welcome, {st.session_state.winner_name.upper()}</p>
    </div>
    """, unsafe_allow_html=True)

    wheel_html = f"""
    <div id="wrapper" style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <div id="pointer" style="width: 0; height: 0; border-left: 12px solid transparent; border-right: 12px solid transparent; border-top: 24px solid #C9A84C; z-index: 100; margin-bottom: -15px;"></div>

        <div id="wheel-container" style="position: relative; width: 330px; height: 330px; border-radius: 50%; border: 7px solid #C9A84C; background: #000; overflow: hidden; display: flex; align-items: center; justify-content: center;">
            <img id="wheel-img" src="data:image/png;base64,{wheel_base64}" style="width: 100%; height: 100%; object-fit: cover; transition: transform 6s cubic-bezier(0.1, 0, 0, 1); transform: rotate(0deg);">
        </div>

        <button id="spin-button" style="margin-top: 25px; padding: 12px 50px; font-size: 1rem; font-weight: bold; background: linear-gradient(135deg, #C9A84C, #8B6914); color: #0B0C0F; border: none; cursor: pointer; font-family: 'Cinzel'; letter-spacing: 2px;">SPIN TO WIN</button>

        <h2 id="winner-display" style="margin-top: 20px; color: #E8C97A; font-family: 'Cinzel'; text-align: center; font-size: 1.2rem; min-height: 40px;"></h2>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <script>
    const prizes = {json.dumps(prizes)};
    const img = document.getElementById('wheel-img');
    const btn = document.getElementById('spin-button');
    const display = document.getElementById('winner-display');
    let currentRotation = 0;

    btn.addEventListener('click', () => {{
        if(btn.disabled) return;
        btn.disabled = true;
        display.innerText = "DETERMINING YOUR LUCK...";
        
        const randomDegree = Math.floor(Math.random() * 360);
        currentRotation += 1800 + randomDegree; 
        img.style.transform = `rotate(${{currentRotation}}deg)`;

        setTimeout(() => {{
            const numSlices = 6;
            const sliceDeg = 360 / numSlices;
            
            // MATH ADJUSTMENT FOR YOUR IMAGE:
            // The boundary is at the top, so index 0 starts at 0 degrees.
            const netRotation = (currentRotation % 360);
            const winningIndex = Math.floor(((360 - netRotation) % 360) / sliceDeg);
            
            const winner = prizes[winningIndex];
            display.innerText = "🎉 " + winner.label + " 🎉";
            
            if (winner.label !== "BETTER LUCK NEXT TIME") {{
                btn.style.display = 'none';
                display.innerHTML += '<div style="font-size: 0.7rem; color: #8E8E93; margin-top: 10px;">SCREENSHOT TO CLAIM YOUR PRIZE</div>';
                confetti({{ particleCount: 150, spread: 70, origin: {{ y: 0.6 }}, colors: ['#C9A84C', '#E8C97A'] }});
            }} else {{
                btn.disabled = false;
                display.innerText = "BETTER LUCK NEXT TIME! TRY AGAIN?";
            }}
        }}, 6100);
    }});
    </script>
    """
    components.html(wheel_html, height=500)
