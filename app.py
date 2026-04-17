import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# Page configuration
st.set_page_config(page_title="Vaastu Dreams Spin Wheel", layout="centered")

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# Path resolution
current_dir = os.path.dirname(__file__)
image_target = os.path.join(current_dir, "wheel.jpg")
img_base64 = get_image_base64(image_target)

if img_base64 is None:
    st.error("🚨 'wheel.jpg' not found! Please upload it to your GitHub repo in the same folder as this script.")
else:
    st.title("🎡 Vaastu Dreams III - Lucky Spin")
    
    segments = ["₹ 50,000 Off", "₹ 1 Lacs Off", "Better luck next time", "₹ 1.5 Lacs Off", "₹ 2 Lacs Off", "₹ 75,000 Off"]

    wheel_html = f"""
    <div id="wrapper" style="text-align: center;">
        <div style="position: relative; display: inline-block;">
            <div id="pointer" style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); width: 0; height: 0; border-left: 15px solid transparent; border-right: 15px solid transparent; border-top: 30px solid #FFD700; z-index: 10;"></div>
            <img id="wheel" src="data:image/jpeg;base64,{img_base64}" style="width: 350px; height: 350px; transition: transform 4s cubic-bezier(0.15, 0, 0.15, 1); border-radius: 50%;">
        </div>
        <br><br>
        <button onclick="spinWheel()" style="padding: 12px 30px; font-size: 18px; cursor: pointer; background: #e63946; color: white; border: none; border-radius: 5px;">SPIN NOW</button>
        <h2 id="result" style="margin-top: 20px; font-family: sans-serif; color: #333;"></h2>
    </div>

    <script>
        let currentRotation = 0;
        const segments = {segments};
        function spinWheel() {{
            const wheel = document.getElementById('wheel');
            const resultText = document.getElementById('result');
            resultText.innerHTML = "Spinning...";
            const extraDegree = Math.floor(Math.random() * 360);
            const totalDegree = currentRotation + 1800 + extraDegree;
            currentRotation = totalDegree;
            wheel.style.transform = "rotate(" + totalDegree + "deg)";
            setTimeout(() => {{
                const actualDegree = (360 - (extraDegree % 360)) % 360;
                const index = Math.floor(actualDegree / 60);
                resultText.innerHTML = "Result: " + segments[index];
            }}, 4000);
        }}
    </script>
    """
    components.html(wheel_html, height=550)
