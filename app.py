import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import requests
from streamlit_cropper import st_cropper
from streamlit_lottie import st_lottie

# 1. Page Config
st.set_page_config(page_title="PhotoFix Pro", layout="wide")


# 2. Lottie Animation Loader
@st.cache_data
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None


lottie_ai = load_lottieurl("https://lottie.host/81b10a27-eb63-4560-b636-6927a4216892/O6p6l1hXDe.json")

# 3. Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    .stApp { background-color: #F0F2F5; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}

    .stButton > button {
        background-color: #1877F2; color: #ffffff; font-weight: 600;
        border-radius: 6px; border: none; padding: 0.5rem 1rem; transition: 0.2s;
    }
    .stButton > button:hover { background-color: #166FE5; color: white; }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff; border-radius: 8px; border: 1px solid #ced0d4 !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1); padding: 1.5rem !important; margin-bottom: 1rem;
    }

    .top-header {
        background: white; padding: 15px 25px; border-radius: 8px; border: 1px solid #ced0d4;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1); margin-bottom: 25px; display: flex; align-items: center;
    }
    .top-header h1 { color: #1877F2; margin: 0; font-size: 24px; font-weight: bold; }
    .top-header p { color: #65676B; margin: 0; margin-left: 15px; font-size: 15px; padding-top: 5px; }
</style>
""", unsafe_allow_html=True)

# 4. Header Render
st.markdown("""
<div class="top-header">
    <h1>🌐 PhotoFix</h1>
    <p>Professional Image Enhancement & Optimization Studio</p>
</div>
""", unsafe_allow_html=True)

# 5. Main Workspace Layout
col_settings, col_feed = st.columns([1, 2.5], gap="large")

# --- Left Column: Settings + Inspiration Gallery ---
with col_settings:
    with st.container(border=True):
        st.markdown("<h3 style='color:#050505; margin-top:0; font-size:18px;'>⚙️ Tools & Settings</h3>",
                    unsafe_allow_html=True)
        st.markdown("<hr style='margin: 10px 0; border-color: #ced0d4;'>", unsafe_allow_html=True)
        enable_cropping = st.toggle("✂️ Manual Crop Tool", value=False)

    with st.container(border=True):
        st.markdown(
            "<h3 style='text-align:center; color:#050505; font-size:18px; margin-top:0;'>✨ Inspiration Gallery</h3>",
            unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#65676B; font-size:13px;'>Real capabilities of our engine</p>",
                    unsafe_allow_html=True)

        gallery_html = """<style>
.gallery-wrapper {
    background: white; padding: 10px; border-radius: 8px; text-align: center;
    border: 1px solid #ced0d4; margin-bottom: 15px;
}
.gallery-wrapper img { width: 100%; border-radius: 4px; margin-bottom: 5px; object-fit: cover; }
.badge { font-size: 11px; font-weight: bold; padding: 3px 8px; border-radius: 12px; display: inline-block; margin: 5px 0; }
.b-before { background: #E4E6EB; color: #050505; }
.b-after { background: #1877F2; color: white; }
.img-before { filter: brightness(60%) contrast(85%) blur(0.5px); }
.img-after { filter: brightness(110%) contrast(115%) saturate(120%); }
</style>
<marquee direction="up" scrollamount="3" height="400px" onmouseover="this.stop();" onmouseout="this.start();">"""

        # תמונות ממקור אמין שלא נשבר
        images = [
            "https://picsum.photos/id/10/400/300",
            "https://picsum.photos/id/11/400/300",
            "https://picsum.photos/id/13/400/300"
        ]

        for img in images * 2:
            gallery_html += f"""
<div class="gallery-wrapper">
<span class="badge b-before">Original</span>
<img class="img-before" src="{img}" alt="before image" />
<span class="badge b-after">PhotoFix Enhanced</span>
<img class="img-after" src="{img}" alt="after image" />
</div>"""

        gallery_html += "</marquee>"
        st.markdown(gallery_html, unsafe_allow_html=True)

# --- Right Column: Main Upload & Process Workspace ---
with col_feed:
    with st.container(border=True):
        st.markdown("<h3 style='color:#050505; margin-top:0; font-size:18px;'>📸 Upload Workspace</h3>",
                    unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Drag and drop or browse files", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        with st.container(border=True):
            if enable_cropping:
                st.markdown("<h4 style='color:#050505; font-size:16px;'>Select the exact area to crop:</h4>",
                            unsafe_allow_html=True)
                img_to_process = st_cropper(image, realtime_update=True, box_color='#1877F2')
            else:
                img_to_process = image
                st.markdown("<h4 style='color:#050505; font-size:16px;'>Live Preview:</h4>", unsafe_allow_html=True)
                st.image(image, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)
            process_btn = st.button("🚀 Run Advanced Enhancement", use_container_width=True)

        if process_btn:
            loading_placeholder = st.empty()
            with loading_placeholder.container():
                st.markdown("<h4 style='text-align:center; color:#1877F2;'>Analyzing and optimizing image...</h4>",
                            unsafe_allow_html=True)
                if lottie_ai:
                    st_lottie(lottie_ai, height=150, key="loading_anim")

            img_array = np.array(img_to_process)
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

            lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            limg = cv2.merge((cl, a, b))
            optimized_bgr = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

            final_bgr = cv2.fastNlMeansDenoisingColored(optimized_bgr, None, 5, 5, 7, 21)
            final_rgb = cv2.cvtColor(final_bgr, cv2.COLOR_BGR2RGB)

            loading_placeholder.empty()

            with st.container(border=True):
                st.markdown("<h3 style='color:#050505; font-size:18px; margin-top:0;'>✨ Final Results</h3>",
                            unsafe_allow_html=True)

                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.markdown("<p style='text-align:center; font-weight:bold; color:#65676B;'>Original</p>",
                                unsafe_allow_html=True)
                    st.image(img_to_process, use_container_width=True)
                with res_col2:
                    st.markdown("<p style='text-align:center; font-weight:bold; color:#1877F2;'>Enhanced</p>",
                                unsafe_allow_html=True)
                    st.image(final_rgb, use_container_width=True)

                result_pil = Image.fromarray(final_rgb)
                buf = io.BytesIO()
                result_pil.save(buf, format="PNG")
                byte_im = buf.getvalue()

                st.markdown("<br>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download High-Quality PNG",
                    data=byte_im,
                    file_name="PhotoFix_Premium_Enhanced.png",
                    mime="image/png",
                    use_container_width=True
                )