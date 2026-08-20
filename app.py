import streamlit as st
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
from streamlit_cropper import st_cropper
import io

st.set_page_config(page_title="Pro Image Editor", layout="wide")

st.markdown("""
    <style>
    h1 { font-family: 'Helvetica Neue', sans-serif; color: #1f2937; text-align: center; margin-bottom: 5px; }
    .subtitle { text-align: center; color: #6b7280; font-size: 1.1rem; margin-bottom: 30px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# זיכרון הסליידרים
if 'bright' not in st.session_state: st.session_state.bright = 1.0
if 'cont' not in st.session_state: st.session_state.cont = 1.0
if 'sat' not in st.session_state: st.session_state.sat = 1.0
if 'sharp' not in st.session_state: st.session_state.sharp = 1.0


def set_optimal():
    st.session_state.bright = 1.05
    st.session_state.cont = 1.15
    st.session_state.sat = 1.20
    st.session_state.sharp = 1.20


def reset_all():
    st.session_state.bright = 1.0
    st.session_state.cont = 1.0
    st.session_state.sat = 1.0
    st.session_state.sharp = 1.0


st.markdown("<h1>Pro Image Editor</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Interactive cropping & stylish frames</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload an Image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    original = Image.open(uploaded_file)
    img_format = original.format if original.format else "JPEG"

    # תפריט צדדי (כלים)
    st.sidebar.markdown("### ✨ Magic Tools")
    col_a, col_b = st.sidebar.columns(2)
    with col_a:
        st.button("Auto Optimize", on_click=set_optimal, use_container_width=True)
    with col_b:
        st.button("Reset All", on_click=reset_all, use_container_width=True)

    st.sidebar.divider()

    st.sidebar.markdown("### 🛠️ Manual Tools")

    with st.sidebar.expander("🎨 Color & Light", expanded=True):
        brightness = st.slider("Brightness", 0.5, 2.0, key='bright')
        contrast = st.slider("Contrast", 0.5, 2.0, key='cont')
        saturation = st.slider("Saturation", 0.0, 2.0, key='sat')

    with st.sidebar.expander("🔍 Details"):
        sharpness = st.slider("Sharpness", 0.0, 3.0, key='sharp')
        noise_reduction = st.checkbox("Smooth Noise")

    with st.sidebar.expander("🖼️ Frames"):
        frame_style = st.selectbox("Choose Style:", ["None", "Classic Solid", "Polaroid", "Double Elegant"])
        frame_color = st.color_picker("Frame Color (if applicable)", "#FFFFFF")

    # חלוקה ל-2 עמודות מרכזיות
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<p style='text-align:center; font-weight:bold;'>1. Crop (Drag the box)</p>",
                    unsafe_allow_html=True)
        # החיתוך האינטראקטיבי!
        cropped_img = st_cropper(original, realtime_update=True, box_color='#007AFF', aspect_ratio=None)

    # החלת העריכות על התמונה החתוכה
    edited = cropped_img.copy()

    if noise_reduction:
        edited = edited.filter(ImageFilter.SMOOTH_MORE)

    edited = ImageEnhance.Brightness(edited).enhance(brightness)
    edited = ImageEnhance.Contrast(edited).enhance(contrast)
    edited = ImageEnhance.Color(edited).enhance(saturation)
    edited = ImageEnhance.Sharpness(edited).enhance(sharpness)

    # החלת המסגרות
    if frame_style == "Classic Solid":
        edited = ImageOps.expand(edited, border=30, fill=frame_color)
    elif frame_style == "Polaroid":
        # פולארויד: שוליים רחבים למטה
        edited = ImageOps.expand(edited, border=(25, 25, 25, 100), fill=frame_color)
        # הוספת מסגרת אפורה דקיקה מסביב לפולארויד
        edited = ImageOps.expand(edited, border=2, fill='#E5E7EB')
    elif frame_style == "Double Elegant":
        # מסגרת כפולה: לבן, שחור דק, ולבן רחב
        edited = ImageOps.expand(edited, border=8, fill=frame_color)
        edited = ImageOps.expand(edited, border=3, fill='#1f2937')
        edited = ImageOps.expand(edited, border=25, fill=frame_color)

    with col2:
        st.markdown("<p style='text-align:center; font-weight:bold;'>2. Final Result</p>", unsafe_allow_html=True)
        st.image(edited, use_container_width=True)

        buf = io.BytesIO()
        if img_format == "JPEG":
            edited.save(buf, format=img_format, quality=100, subsampling=0)
        else:
            edited.save(buf, format=img_format)

        st.download_button(
            label="⬇️ Download Masterpiece",
            data=buf.getvalue(),
            file_name=f"final_edit.{img_format.lower()}",
            mime=f"image/{img_format.lower()}",
            use_container_width=True
        )