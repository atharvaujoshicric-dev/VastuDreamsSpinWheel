import streamlit as st
import streamlit.components.v1 as components
import base64
import os
from pathlib import Path

# Setup
st.set_page_config(page_title="Vaastu Dreams Spin Wheel", layout="centered")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

try:
    current_dir = Path(__file__).parent.absolute()
except NameError:
    current_dir = Path.cwd()

image_target = current_dir / "wheel.jpg"
img_base64 = get_image_base64(str(image_target))

if img_base64 is None:
    st.error("🚨 'wheel.jpg' not found. Please ensure the file is in the same folder as app.py")
else:
    wheel_html = f"""
    <div id="wrapper" style="text-align: center; background-color: #0f1116; padding: 40px; border-radius: 20px;">
        <div style="position: relative; display: inline-block;">
            <div id="pointer" style="
                position: absolute; top: -15px; left: 50%; transform: translateX(-50%);
                width: 0; height: 0; border-left: 20px solid transparent;
                border-right: 20px solid transparent; border-top: 40px solid #FFD700;
                z-index: 100; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.5));
            "></div>
            
            <img id="wheel" src="data:image/jpeg;base64,{img_base64}" style="
                width: 450px; height: 450px;
                transition: transform 5s cubic-bezier(0.15, 0, 0.15, 1);
                border-radius: 50%;
                border: 8px solid #333;
            ">
        </div>
        <br><br>
        <button onclick="spinWheel()" style="
            padding: 15px 60px; font-size: 24px; cursor: pointer;
            background: #e31b23; color: white; border: none; border-radius: 10px;
            font-weight: bold; text-transform: uppercase; letter-spacing: 1px;
            box-shadow: 0 6px #9e1217; transition: 0.1s;
        " onmousedown="this.style.transform='translateY(3px)';this.style.boxShadow='0 3px #9e1217'" 
           onmouseup="this.style.transform='translateY(0px)';this.style.boxShadow='0 6px #9e1217'">
            SPIN WHEEL
        </button>
    </div>

    <script>
        let currentRotation = 0;

        function spinWheel() {{
            const wheel = document.getElementById('wheel');
            
            // Random degree for the landing
            const randomDegree = Math.floor(Math.random() * 360);
            
            // 8 full rotations + the random landing
            const totalRotation = currentRotation + (360 * 8) + randomDegree;
            currentRotation = totalRotation;

            wheel.style.transform = "rotate(" + totalRotation + "deg)";
        }}
    </script>
    """
    components.html(wheel_html, height=650)
