import streamlit as st
import streamlit.components.v1 as components
import random

# Page configuration
st.set_page_config(page_title="Vaastu Dreams Spin Wheel", layout="centered")

st.title("🎡 Vaastu Dreams III - Lucky Spin")

# Define the segments based on your image (clockwise starting from top)
segments = [
    "₹ 50,000 Off",
    "₹ 1 Lacs Off",
    "Better luck next time",
    "₹ 1.5 Lacs Off",
    "₹ 2 Lacs Off",
    "₹ 75,000 Off"
]

# JavaScript/CSS for the wheel logic
# We use a CSS transform to rotate the image
wheel_html = f"""
<div id="wrapper" style="text-align: center; font-family: sans-serif;">
    <div class="container" style="position: relative; display: inline-block;">
        <div id="pointer" style="
            position: absolute;
            top: -20px;
            left: 50%;
            transform: translateX(-50%);
            width: 0; 
            height: 0; 
            border-left: 20px solid transparent;
            border-right: 20px solid transparent;
            border-top: 40px solid #FFD700;
            z-index: 10;
            filter: drop-shadow(0 2px 5px rgba(0,0,0,0.5));
        "></div>
        
        <img id="wheel" src="app/static/wheel.jpg" style="
            width: 400px;
            height: 400px;
            transition: transform 4s cubic-bezier(0.15, 0, 0.15, 1);
            border-radius: 50%;
        ">
    </div>
    
    <br><br>
    <button onclick="spinWheel()" style="
        padding: 15px 40px;
        font-size: 20px;
        cursor: pointer;
        background-color: #e63946;
        color: white;
        border: none;
        border-radius: 50px;
        box-shadow: 0 4px #9b2226;
    ">SPIN NOW</button>
    
    <h2 id="result" style="margin-top: 30px; color: #333;"></h2>
</div>

<script>
    let currentRotation = 0;
    const segments = {segments};
    
    function spinWheel() {{
        const wheel = document.getElementById('wheel');
        const resultText = document.getElementById('result');
        
        // Reset result text
        resultText.innerHTML = "Spinning...";
        
        // Calculate a random rotation (at least 5 full spins + random angle)
        const extraDegree = Math.floor(Math.random() * 360);
        const totalDegree = currentRotation + 1800 + extraDegree;
        currentRotation = totalDegree;
        
        wheel.style.transform = "rotate(" + totalDegree + "deg)";
        
        // Calculate which segment it landed on
        // 360 / 6 segments = 60 degrees per segment
        // We subtract the rotation from 360 because the wheel spins clockwise
        setTimeout(() => {{
            const actualDegree = extraDegree % 360;
            // Offset calculation: The pointer is at the top (0 deg). 
            // We need to account for the image orientation.
            const index = Math.floor(((360 - actualDegree) % 360) / 60);
            resultText.innerHTML = "Congratulations! You won: <br><strong>" + segments[index] + "</strong>";
        }}, 4000);
    }}
</script>
"""

# Crucial: Streamlit needs to be able to serve the local image.
# We map the local image to a static path.
current_dir = os.path.dirname(__file__)
img_path = os.path.join(current_dir, "wheel.jpg")

def get_image_base64(path):
    # Check if file exists to avoid the crash you just saw
    if not os.path.isfile(path):
        st.error(f"Error: {path} not found. Please ensure wheel.jpg is in the same folder as app.py")
        return ""
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Use the absolute path
img_base64 = get_image_base64(img_path)
final_html = wheel_html.replace("app/static/wheel.jpg", f"data:image/jpeg;base64,{img_base64}")

# Render the component
components.html(final_html, height=600)
