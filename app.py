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
    st.error("🚨 'wheel.jpg' not found in the repository root.")
else:
    # The Array below matches the image CLOCKWISE
    # Index 0 is the segment immediately to the right of the top-center line
    segments = [
        "₹ 1 Lacs Off",          # Orange (Top Right)
        "Better luck next time", # White (Right)
        "₹ 1.5 Lacs Off",        # Pink (Bottom Right)
        "₹ 2 Lacs Off",          # Orange (Bottom Left)
        "₹ 75,000 Off",         # Yellow (Left)
        "₹ 50,000 Off"           # Pink (Top Left)
    ]

    wheel_html = f"""
    <div id="wrapper" style="text-align: center; font-family: sans-serif;">
        <div style="position: relative; display: inline-block;">
            <div id="pointer" style="
                position: absolute; top: -10px; left: 50%; transform: translateX(-50%);
                width: 0; height: 0; border-left: 20px solid transparent;
                border-right: 20px solid transparent; border-top: 40px solid #FFD700;
                z-index: 10; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));
            "></div>
            
            <img id="wheel" src="data:image/jpeg;base64,{img_base64}" style="
                width: 450px; height: 450px;
                transition: transform 5s cubic-bezier(0.1, 0, 0.1, 1);
                border-radius: 50%;
            ">
        </div>
        <br><br>
        <button onclick="spinWheel()" style="
            padding: 15px 50px; font-size: 22px; cursor: pointer;
            background: #d90429; color: white; border: none; border-radius: 8px;
            font-weight: bold; box-shadow: 0 4px #8d021f;
        ">SPIN WHEEL</button>
        <h2 id="result" style="margin-top: 30px; height: 50px; color: #2b2d42;"></h2>
    </div>

    <script>
        let currentRotation = 0;
        const prizeList = {segments};

        function spinWheel() {{
            const wheel = document.getElementById('wheel');
            const resultText = document.getElementById('result');
            
            resultText.innerHTML = "Wishing you luck...";
            
            // Generate a random degree (0-359)
            const randomDegree = Math.floor(Math.random() * 360);
            // Spin at least 6 full circles + the random stop
            const totalRotation = currentRotation + (360 * 6) + randomDegree;
            currentRotation = totalRotation;

            wheel.style.transform = "rotate(" + totalRotation + "deg)";

            setTimeout(() => {{
                // Calculate position: 
                // Because wheel spins clockwise, we calculate 'distance' from the top pointer.
                // 360 - (totalRotation % 360) gives us the degree that ended at the top.
                const finalDegree = (360 - (totalRotation % 360)) % 360;
                
                // Since a divider line is at the top, index 0 starts immediately.
                // Each slice is 60 degrees.
                const index = Math.floor(finalDegree / 60);
                
                resultText.innerHTML = "WINNER: <span style='color:#d90429'>" + prizeList[index] + "</span>";
            }}, 5000);
        }}
    </script>
    """
    components.html(wheel_html, height=700)
