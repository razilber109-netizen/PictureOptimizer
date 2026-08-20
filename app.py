import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import io

st.set_page_config(page_title="Pro Image Editor", layout="wide")

st.markdown("""
    <style>
    h1 { font-family: 'Helvetica Neue', sans-serif; color: #1f2937; text-align: center; }
    .subtitle { text-align: center; color: #6b7280; font-size: 1.2rem; margin-bottom: 20px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- זיכרון האתר (Session State) ---
# מגדיר את הערכים ההתחלתיים של הסליידרים
if 'bright' not in st.session_state: st.session_state.bright = 1.0
if 'cont' not in st.session_state: st.session_state.cont = 1.0
if 'sat' not in st.session_state: st.session_state.sat = 1.0
if 'sharp' not in st.session_state: st.session_state.sharp = 1.0
if 'auto_fix' not in st.session_state: st.session_state.auto_fix = False

# פונקציה: החלה של המצב האופטימלי (הקסם)
def set_optimal():
    st.session_state.bright = 1.05
    st.session_state.cont = 1.15
    st.session_state.sat = 1.20
    st.session_state.sharp = 1.20
    st.session_state.auto_fix = True

# פונקציה: איפוס הכל למצב המקורי
def reset_all():
    st.session_state.bright = 1.0
    st.session_state.cont = 1.0
    st.session_state.sat = 1.0
    st.session_state.sharp = 1.0
    st.session_state.auto_fix = False

# --- תצוגת האתר ---
st.markdown("<h1>Pro Image Editor</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Professional editing with one-click magic optimization.</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload an Image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    original = Image.open(uploaded_file)
    img_format = original.format if original.format else "JPEG"
    edited = original.copy()
    
    st.sidebar.markdown("### ✨ Magic Tools")
    
    # כפתורי הקסם והאיפוס
    col_a, col_b = st.sidebar.columns(2)
    with col_a:
        st.button("Auto Optimize", on_click=set_optimal, use_container_width=True)
    with col_b:
        st.button("Reset All", on_click=reset_all, use_container_width=True)
        
    st.sidebar.divider()
    
    st.sidebar.markdown("### 🛠️ Manual Tools")
    
    # כלי תיקון תאורה חכם לתמונות בעייתיות
    auto_fix_checkbox = st.sidebar.checkbox("Auto-Fix Lighting", key='auto_fix')
    if auto_fix_checkbox:
        edited = ImageOps.autocontrast(edited, cutoff=1)
    
    # סליידרים שמחוברים לזיכרון של האתר
    with st.sidebar.expander("🎨 Color & Light", expanded=True):
        brightness = st.slider("Brightness", 0.5, 2.0, key='bright')
        contrast = st.slider("Contrast", 0.5, 2.0, key='cont')
        saturation = st.slider("Saturation", 0.0, 2.0, key='sat')
        
    with st.sidebar.expander("🔍 Details"):
        sharpness = st.slider("Sharpness", 0.0, 3.0, key='sharp')
        if st.checkbox("Apply Noise Reduction"):
            edited = edited.filter(ImageFilter.SMOOTH_MORE)
            
    with st.sidebar.expander("✂️ Crop & Frame"):
        # חיתוך
        left = st.slider("Crop Left %", 0, 49, 0)
        right = st.slider("Crop Right %", 0, 49, 0)
        top = st.slider("Crop Top %", 0, 49, 0)
        bottom = st.slider("Crop Bottom %", 0, 49, 0)
        
        width, height = edited.size
        if left > 0 or right > 0 or top > 0 or bottom > 0:
            l_px = int(width * (left / 100))
            r_px = width - int(width * (right / 100))
            t_px = int(height * (top / 100))
            b_px = height - int(height * (bottom / 100))
            if l_px < r_px and t_px < b_px:
                edited = edited.crop((l_px, t_px, r_px, b_px))
        
        # מסגרת
        frame_width = st.slider("Frame Width (px)", 0, 100, 0)
        if frame_width > 0:
            frame_color = st.color_picker("Frame Color", "#FFFFFF")
            edited = ImageOps.expand(edited, border=frame_width, fill=frame_color)

    # החלת השינויים מהסליידרים על התמונה
    edited = ImageEnhance.Brightness(edited).enhance(brightness)
    edited = ImageEnhance.Contrast(edited).enhance(contrast)
    edited = ImageEnhance.Color(edited).enhance(saturation)
    edited = ImageEnhance.Sharpness(edited).enhance(sharpness)

    # תצוגה מרכזית
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p style='text-align:center; font-weight:bold;'>Original</p>", unsafe_allow_html=True)
        st.image(original, use_container_width=True)
        
    with col2:
        st.markdown("<p style='text-align:center; font-weight:bold;'>Edited Result</p>", unsafe_allow_html=True)
        st.image(edited, use_container_width=True)
        
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
