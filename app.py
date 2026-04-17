import streamlit as st
import streamlit.components.v1 as components
import base64
import os
from pathlib import Path

st.set_page_config(page_title="Vaastu Dreams Spin Wheel", layout="centered")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# Resolve path safely for Streamlit Cloud
try:
    current_dir = Path(__file__).parent.absolute()
except NameError:
    current_dir = Path.cwd()

image_target = current_dir / "wheel.jpg"
img_base64 = get_image_base64(str(image_target))

if img_base64 is None:
    st.error(f"🚨 'wheel.jpg' not found at {image_target}")
else:
    st.title("🎡 Vaastu Dreams III - Lucky Spin")
    
    # EXACT order from the image starting from the top-right segment (0-60 degrees)
    segments = [
        "₹ 1 Lacs Off",          # 0° to 60°
        "Better luck next time", # 60° to 120°
        "₹ 1.5 Lacs Off",        # 120° to 180°
        "₹ 2 Lacs Off",          # 180° to 240°
        "₹ 75,000 Off",         # 240° to 300°
        "₹ 50,000 Off"           # 300° to 360°
    ]

    wheel_html = f"""
    <div id="wrapper" style="text-align: center; font-family: sans-serif;">
        <div style="position: relative; display: inline-block;">
            <div id="pointer" style="
                position: absolute; 
                top: -15px; 
                left: 50%; 
                transform: translateX(-50%); 
                width: 0; 
                height: 0; 
                border-left: 15px solid transparent; 
                border-right: 15px solid transparent; 
                border-top: 30px solid #FFD700; 
                z-index: 10;
                filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
            "></div>
            
            <img id="wheel" src="data:image/jpeg;base64,{img_base64}" style="
                width: 400px; 
                height: 400px; 
                transition: transform 5s cubic-bezier(0.1, 0, 0.1, 1); 
                border-radius: 50%;
            ">
        </div>
        <br><br>
        <button onclick="spinWheel()" style="
            padding: 15px 40px; 
            font-size: 20px; 
            background: #e63946; 
            color: white; 
            border: none; 
            border-radius: 5px; 
            cursor: pointer;
            font-weight: bold;
        ">SPIN TO WIN</button>
        <h2 id="result" style="margin-top: 25px; color: #333;"></h2>
    </div>

    <script>
        let currentRotation = 0;
        const segments = {segments};
        
        function spinWheel() {{
            const wheel = document.getElementById('wheel');
            const resultText = document.getElementById('result');
            resultText.innerHTML = "Spinning...";
            
            // Generate a random degree
            const extraDegree = Math.floor(Math.random() * 360);
            // Spin at least 5 times (1800 deg) + the extra landing spot
            const totalDegree = currentRotation + 1800 + extraDegree;
            currentRotation = totalDegree;
            
            wheel.style.transform = "rotate(" + totalDegree + "deg)";
            
            setTimeout(() => {{
                // The pointer is at 0 degrees (top).
                // To find what is under the pointer, we look at the remainder of the rotation.
                // We use (360 - (rotation % 360)) because the wheel moves clockwise.
                const landingDegree = (360 - (extraDegree % 360)) % 360;
                const index = Math.floor(landingDegree / 60);
                
                resultText.innerHTML = "You Won: <strong>" + segments[index] + "</strong>";
            }}, 5000);
        }}
    </script>
    """
    components.html(wheel_html, height=600)
