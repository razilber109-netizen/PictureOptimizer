import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import requests
from streamlit_cropper import st_cropper
from streamlit_lottie import st_lottie
import hydralit_components as hc

# 1. הגדרת הדף - חובה להיות ראשון
st.set_page_config(page_title="PhotoFix", layout="wide", initial_sidebar_state="collapsed")


# 2. פונקציה לטעינת אנימציות רשת (Lottie)
@st.cache_data
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None


# טעינת אנימציית הטעינה
lottie_ai = load_lottieurl("https://lottie.host/81b10a27-eb63-4560-b636-6927a4216892/O6p6l1hXDe.json")

# 3. עיצוב CSS מתקדם (שילוב עם ה-Navbar)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Segoe UI', 'Assistant', Tahoma, Geneva, Verdana, sans-serif !important;
    }

    /* רקע אפור פייסבוק */
    .stApp { background-color: #F0F2F5; }

    /* הסתרת מיתוג Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* עיצוב כפתורים */
    .stButton > button {
        background-color: #1877F2;
        color: #ffffff;
        font-weight: 600;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1rem;
        transition: 0.2s;
    }
    .stButton > button:hover {
        background-color: #166FE5;
        color: white;
    }

    /* עיצוב הכרטיסיות המגודרות */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #ced0d4 !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        padding: 1.5rem !important;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 4. יצירת סרגל ניווט עליון מקצועי (Hydralit)
menu_data = [
    {'icon': "fas fa-image", 'label': "סטודיו לעריכה"},
    {'icon': "far fa-clone", 'label': "גלריית השראה"},
    {'icon': "fas fa-sliders-h", 'label': "הגדרות פרו"}
]

# צבעי התפריט בסגנון פייסבוק
over_theme = {'txc_inactive': '#65676B', 'menu_background': 'white', 'txc_active': '#1877F2',
              'option_active': '#F0F2F5'}

menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='🌐 PhotoFix',
    login_name=None,
    hide_streamlit_markers=False,
    sticky_nav=True,
    sticky_mode='pinned',
)

st.markdown("<br>", unsafe_allow_html=True)

# 5. חלוקת אזור העבודה
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
        st.markdown("<h3 style='color:#050505; margin-top:0; font-size:18px;'>📸 צור פוסט / העלה תמונה</h3>",
                    unsafe_allow_html=True)
        uploaded_file = st.file_uploader("בחר תמונה לעיבוד", type=['jpg', 'jpeg', 'png'])

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
            # מקום שומר לאנימציית הטעינה
            loading_placeholder = st.empty()

            with loading_placeholder.container():
                st.markdown("<h4 style='text-align:center; color:#1877F2;'>מנתח ומנקה את התמונה...</h4>",
                            unsafe_allow_html=True)
                if lottie_ai:
                    st_lottie(lottie_ai, height=150, key="loading_anim")

            # --- תהליך העיבוד ---
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

            # מחיקת אנימציית הטעינה לאחר סיום העיבוד
            loading_placeholder.empty()

            # --- הצגת התוצאות ---
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