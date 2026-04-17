import streamlit as st
import random
import time

# --- Page Config ---
st.set_page_config(page_title="Vaastu Dreams Spin Wheel", layout="centered")

# --- Custom CSS for Animation ---
def local_css():
    st.markdown("""
        <style>
        .wheel-container {
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            height: 500px;
        }
        .spin-wheel {
            width: 450px;
            transition: transform 4s cubic-bezier(0.15, 0, 0.15, 1);
            border-radius: 50%;
        }
        .pointer {
            position: absolute;
            top: 10px;
            z-index: 10;
            width: 0; 
            height: 0; 
            border-left: 20px solid transparent;
            border-right: 20px solid transparent;
            border-top: 40px solid #FFD700;
            filter: drop-shadow(0px 4px 4px rgba(0,0,0,0.5));
        }
        </style>
    """, unsafe_allow_html=True)

local_css()

st.title("🎡 Vaastu Dreams III Lucky Spin")

# --- State Management ---
if 'rotation' not in st.session_state:
    st.session_state.rotation = 0
if 'winner' not in st.session_state:
    st.session_state.winner = None

# --- Spin Logic ---
def spin():
    # Add a large random rotation (at least 5 full circles + random offset)
    extra_spin = random.randint(1800, 3600)
    st.session_state.rotation += extra_spin
    
    # Calculate winner based on final angle
    # The wheel has 6 segments (60 degrees each)
    final_angle = st.session_state.rotation % 360
    
    # Map angles to segments (Adjust these based on image alignment)
    # 0 deg is top, segments go clockwise
    if 0 <= final_angle < 60:
        st.session_state.winner = "₹ 1 Lacs Off"
    elif 60 <= final_angle < 120:
        st.session_state.winner = "Better luck next time"
    elif 120 <= final_angle < 180:
        st.session_state.winner = "₹ 1.5 Lacs Off"
    elif 180 <= final_angle < 240:
        st.session_state.winner = "₹ 2 Lacs Off"
    elif 240 <= final_angle < 300:
        st.session_state.winner = "₹ 75,000 Off"
    else:
        st.session_state.winner = "₹ 50,000 Off"

# --- UI Components ---
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Display the wheel with dynamic rotation
    st.markdown(f"""
        <div class="wheel-container">
            <div class="pointer"></div>
            <img src="wheel.png" 
                 class="spin-wheel" 
                 style="transform: rotate({st.session_state.rotation}deg);">
        </div>
    """, unsafe_allow_html=True)

    st.button("SPIN THE WHEEL", on_click=spin, use_container_width=True)

# --- Result Display ---
if st.session_state.winner:
    # Wait for animation to finish visually
    time.sleep(0.5) 
    st.balloons()
    st.success(f"### Congratulations! You won: {st.session_state.winner}")
