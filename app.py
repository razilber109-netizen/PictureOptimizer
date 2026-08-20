import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import io

# 1. Page Configuration
st.set_page_config(page_title="Pro Image Editor", layout="wide")

# 2. Custom CSS
st.markdown("""
    <style>
    h1 { font-family: 'Helvetica Neue', sans-serif; color: #1f2937; text-align: center; }
    .subtitle { text-align: center; color: #6b7280; font-size: 1.2rem; margin-bottom: 20px; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. Header
st.markdown("<h1>Pro Image Editor</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Professional editing tools for perfect results.</p>", unsafe_allow_html=True)

# 4. Upload Section
uploaded_file = st.file_uploader("Upload an Image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    original = Image.open(uploaded_file)
    img_format = original.format if original.format else "JPEG"
    
    # Initialize edited image variable
    edited = original.copy()
    
    # --- SIDEBAR: Professional Tools ---
    st.sidebar.markdown("### 🛠️ Editing Tools")
    
    # Tool 1: Crop
    with st.sidebar.expander("✂️ Crop"):
        st.write("Adjust margins to crop:")
        left = st.slider("Left %", 0, 49, 0)
        right = st.slider("Right %", 0, 49, 0)
        top = st.slider("Top %", 0, 49, 0)
        bottom = st.slider("Bottom %", 0, 49, 0)
        
        width, height = edited.size
        left_px = int(width * (left / 100))
        right_px = width - int(width * (right / 100))
        top_px = int(height * (top / 100))
        bottom_px = height - int(height * (bottom / 100))
        
        if left_px < right_px and top_px < bottom_px:
            edited = edited.crop((left_px, top_px, right_px, bottom_px))
            
    # Tool 2: Color & Light
    with st.sidebar.expander("🎨 Color & Light"):
        brightness = st.slider("Brightness", 0.5, 2.0, 1.0, 0.05)
        contrast = st.slider("Contrast", 0.5, 2.0, 1.0, 0.05)
        saturation = st.slider("Saturation", 0.0, 2.0, 1.0, 0.05)
        
        edited = ImageEnhance.Brightness(edited).enhance(brightness)
        edited = ImageEnhance.Contrast(edited).enhance(contrast)
        edited = ImageEnhance.Color(edited).enhance(saturation)
        
    # Tool 3: Detail & Noise Reduction
    with st.sidebar.expander("🔍 Details"):
        sharpness = st.slider("Sharpness", 0.0, 3.0, 1.0, 0.1)
        edited = ImageEnhance.Sharpness(edited).enhance(sharpness)
        
        noise_reduction = st.checkbox("Apply Noise Reduction")
        if noise_reduction:
            # Uses a smoothing filter to reduce grain/noise
            edited = edited.filter(ImageFilter.SMOOTH_MORE)
            
    # Tool 4: Frame / Border
    with st.sidebar.expander("🖼️ Frame"):
        frame_width = st.slider("Frame Width (px)", 0, 150, 0)
        frame_color = st.color_picker("Frame Color", "#FFFFFF")
        
        if frame_width > 0:
            edited = ImageOps.expand(edited, border=frame_width, fill=frame_color)

    # --- MAIN AREA: Display Results ---
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<p style='text-align:center; font-weight:bold;'>Original</p>", unsafe_allow_html=True)
        st.image(original, use_container_width=True)
        
    with col2:
        st.markdown("<p style='text-align:center; font-weight:bold;'>Edited Result</p>", unsafe_allow_html=True)
        st.image(edited, use_container_width=True)
        
        # Prepare High-Quality Download
        buf = io.BytesIO()
        if img_format == "JPEG":
            edited.save(buf, format=img_format, quality=100, subsampling=0)
        else:
            edited.save(buf, format=img_format)
        
        st.download_button(
            label="⬇️ Download High-Res Image",
            data=buf.getvalue(),
            file_name=f"edited_image.{img_format.lower()}",
            mime=f"image/{img_format.lower()}",
            use_container_width=True
        )
