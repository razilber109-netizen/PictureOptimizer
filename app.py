import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import requests
from streamlit_cropper import st_cropper
from streamlit_lottie import st_lottie

# 1. הגדרת הדף - חובה לשים פריסה רחבה וסרגל צד פתוח תמיד!
st.set_page_config(page_title="PhotoFix", layout="wide", initial_sidebar_state="expanded")


# 2. פונקציה לטעינת אנימציות רשת
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

# 3. עיצוב CSS מתקדם (פייסבוק + גלריה רצה)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Segoe UI', 'Assistant', Tahoma, Geneva, Verdana, sans-serif !important;
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

    /* כותרת עליונה חדשה ומקצועית */
    .top-header {
        background: white; padding: 15px 25px; border-radius: 8px; border: 1px solid #ced0d4;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1); margin-bottom: 25px; display: flex; align-items: center;
    }
    .top-header h1 { color: #1877F2; margin: 0; font-size: 24px; font-weight: bold; }
    .top-header p { color: #65676B; margin: 0; margin-right: 15px; font-size: 15px; padding-top: 5px; }
</style>
""", unsafe_allow_html=True)

# 4. כותרת עליונה אמיתית
st.markdown("""
<div class="top-header">
    <h1>🌐 PhotoFix</h1>
    <p>מערכת הסטודיו המרכזית - ניקוי, שיפור ואופטימיזציה</p>
</div>
""", unsafe_allow_html=True)

# 5. --- בניית הגלריה הרצה בסרגל הצד (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center; color:#050505; font-size:20px;'>✨ גלריית השראה</h2>",
                unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#65676B; font-size:14px;'>דוגמאות ליכולות המערכת שלנו</p>",
                unsafe_allow_html=True)

    # CSS ו-HTML עבור האנימציה של הגלריה
    gallery_html = """
    <style>
    .slider-container {
        height: 75vh; overflow: hidden; position: relative; padding: 5px;
    }
    .slider-track {
        animation: scrollVertical 25s linear infinite; display: flex; flex-direction: column; gap: 20px;
    }
    .slider-track:hover { animation-play-state: paused; }
    @keyframes scrollVertical { 0% { transform: translateY(0); } 100% { transform: translateY(-50%); } }
    .gallery-card {
        background: white; padding: 12px; border-radius: 8px; text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #ced0d4;
    }
    .gallery-card img { width: 100%; border-radius: 4px; margin-bottom: 5px; }

    /* שימוש בפילטרים כדי לזייף לפני ואחרי מתמונות רשת איכותיות */
    .img-before { filter: brightness(55%) contrast(85%) sepia(20%) blur(0.5px); }
    .img-after { filter: brightness(110%) contrast(115%) saturate(120%); }

    .badge { font-size: 12px; font-weight: bold; padding: 4px 10px; border-radius: 12px; display: inline-block; margin-bottom: 8px; }
    .badge-before { background: #E4E6EB; color: #050505; }
    .badge-after { background: #1877F2; color: white; margin-top: 15px; }
    </style>
    <div class="slider-container">
        <div class="slider-track">
    """

    # מאגר תמונות מהאינטרנט
    images = [
        "https://images.unsplash.com/photo-1506744626753-eba7bc3623ea?w=400&q=80",
        "https://images.unsplash.com/photo-1495111316679-43c5e3144a2c?w=400&q=80",
        "https://images.unsplash.com/photo-1516214104703-d2507f62742a?w=400&q=80"
    ]

    # מכפילים את התמונות כדי שהגלילה לא תעצור לעולם
    for img in images * 3:
        gallery_html += f"""
        <div class="gallery-card">
            <span class="badge badge-before">לפני עיבוד</span>
            <img class="img-before" src="{img}">
            <span class="badge badge-after">אחרי PhotoFix</span>
            <img class="img-after" src="{img}">
        </div>
        """
    gallery_html += "</div></div>"

    st.markdown(gallery_html, unsafe_allow_html=True)

# 6. --- אזור העבודה המרכזי ---
col_settings, col_feed = st.columns([1, 2.5], gap="large")

with col_settings:
    with st.container(border=True):
        st.markdown("<h3 style='color:#050505; margin-top:0; font-size:18px;'>⚙️ כלי עבודה</h3>",
                    unsafe_allow_html=True)
        st.markdown("<hr style='margin: 10px 0; border-color: #ced0d4;'>", unsafe_allow_html=True)
        enable_cropping = st.toggle("✂️ כלי חיתוך ידני", value=False)
        st.markdown(
            "<p style='font-size:14px; color:#65676B; line-height:1.6; margin-top:15px;'>בחר האם לחתוך את התמונה לפני תחילת תהליך האופטימיזציה.</p>",
            unsafe_allow_html=True)

with col_feed:
    with st.container(border=True):
        st.markdown("<h3 style='color:#050505; margin-top:0; font-size:18px;'>📸 אזור העלאת תמונות</h3>",
                    unsafe_allow_html=True)
        uploaded_file = st.file_uploader("בחר או גרור קובץ לכאן", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        with st.container(border=True):
            if enable_cropping:
                st.markdown("<h4 style='color:#050505; font-size:16px;'>סמן את האזור המדויק:</h4>",
                            unsafe_allow_html=True)
                img_to_process = st_cropper(image, realtime_update=True, box_color='#1877F2')
            else:
                img_to_process = image
                st.markdown("<h4 style='color:#050505; font-size:16px;'>תצוגה מקדימה:</h4>", unsafe_allow_html=True)
                st.image(image, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)
            process_btn = st.button("🚀 הפעל מנוע שיפור מתקדם", use_container_width=True)

        if process_btn:
            loading_placeholder = st.empty()
            with loading_placeholder.container():
                st.markdown("<h4 style='text-align:center; color:#1877F2;'>מנתח ומנקה את התמונה...</h4>",
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
                st.markdown("<h3 style='color:#050505; font-size:18px; margin-top:0;'>✨ תוצאות סופיות</h3>",
                            unsafe_allow_html=True)

                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.markdown("<p style='text-align:center; font-weight:bold; color:#65676B;'>מקור</p>",
                                unsafe_allow_html=True)
                    st.image(img_to_process, use_container_width=True)
                with res_col2:
                    st.markdown("<p style='text-align:center; font-weight:bold; color:#1877F2;'>אחרי שיפור</p>",
                                unsafe_allow_html=True)
                    st.image(final_rgb, use_container_width=True)

                result_pil = Image.fromarray(final_rgb)
                buf = io.BytesIO()
                result_pil.save(buf, format="PNG")
                byte_im = buf.getvalue()

                st.markdown("<br>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 שמור למחשב (PNG איכותי)",
                    data=byte_im,
                    file_name="PhotoFix_Premium_Enhanced.png",
                    mime="image/png",
                    use_container_width=True
                )