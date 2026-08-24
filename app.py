import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
from streamlit_cropper import st_cropper

# הגדרת פריסה רחבה
st.set_page_config(page_title="PhotoFix Pro", layout="wide")

# CSS עכשווי, נקי ומקצועי (בלי אימוג'ים)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;800&display=swap');

    html, body, [class*="css"] { 
        font-family: 'Assistant', sans-serif; 
    }

    /* רקע כהה מודרני עם תאורה גיאומטרית עדינה */
    .stApp {
        background-color: #0b1120;
        background-image: radial-gradient(circle at 10% 20%, rgba(56, 189, 248, 0.05), transparent 30%), 
                          radial-gradient(circle at 90% 80%, rgba(139, 92, 246, 0.08), transparent 30%);
    }

    /* תיקון צבעי טקסט */
    p, label, span, div, h1, h2, h3, h4 {
        color: #e2e8f0 !important;
    }

    /* עיצוב הפאנל הימני (תחליף לסרגל הצד) */
    .control-panel {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }

    /* עיצוב הלוגו המקצועי */
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin-bottom: 30px;
        margin-top: 10px;
    }

    .brand-text {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #38bdf8, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1;
    }

    /* הסתרת מיתוג Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ----- לוגו מקצועי מבוסס SVG (בלי אימוג'י!) -----
svg_logo = """
<svg width="50" height="50" viewBox="0 0 24 24" fill="none" stroke="url(#grad1)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#38bdf8;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#8b5cf6;stop-opacity:1" />
    </linearGradient>
  </defs>
  <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
  <circle cx="12" cy="13" r="4"></circle>
</svg>
"""

st.markdown(f"""
<div class="logo-container">
    {svg_logo}
    <h1 class="brand-text">PhotoFix</h1>
</div>
<p style='text-align: center; color: #94a3b8 !important; margin-bottom: 40px;'>מערכת חכמה לשיפור תמונות, ניקוי רעשים ואופטימיזציית תאורה</p>
""", unsafe_allow_html=True)

# ----- חלוקת המסך: פאנל שליטה בימין (1), אזור עבודה בשמאל (3) -----
control_col, workspace_col = st.columns([1, 3], gap="large")

with control_col:
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>הגדרות עבודה</h3>", unsafe_allow_html=True)
    st.divider()

    enable_cropping = st.toggle("הפעל כלי חיתוך (Crop)", value=False)

    st.divider()
    st.markdown(
        "<p style='font-size: 0.9rem; color: #94a3b8 !important;'>העלה תמונה, בחר האם לחתוך אותה, ולחץ על כפתור העיבוד שיופיע באזור העבודה.</p>",
        unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with workspace_col:
    uploaded_file = st.file_uploader("גרור קובץ או לחץ לבחירה", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        # אזור התצוגה והחיתוך
        st.markdown("<br>", unsafe_allow_html=True)
        if enable_cropping:
            st.markdown("#### סמן את האזור הרצוי לחיתוך:")
            img_to_process = st_cropper(image, realtime_update=True, box_color='#38bdf8')
        else:
            img_to_process = image
            st.markdown("#### תצוגה מקדימה:")
            st.image(image, width=600)

        st.markdown("<br>", unsafe_allow_html=True)

        # כפתור העיבוד המרכזי
        if st.button("החל שיפור תמונה מתקדם", use_container_width=True):
            img_array = np.array(img_to_process)
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

            with st.spinner('מנתח את התמונה ומשפר איכות...'):
                # שיפור ניגודיות
                lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
                l, a, b = cv2.split(lab)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                cl = clahe.apply(l)
                limg = cv2.merge((cl, a, b))
                optimized_bgr = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

                # ניקוי רעשים
                final_bgr = cv2.fastNlMeansDenoisingColored(optimized_bgr, None, 5, 5, 7, 21)
                final_rgb = cv2.cvtColor(final_bgr, cv2.COLOR_BGR2RGB)

            st.success("העיבוד הושלם בהצלחה!")

            # תצוגת התוצאות
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.markdown("<h4 style='text-align: center;'>תמונת מקור</h4>", unsafe_allow_html=True)
                st.image(img_to_process, use_container_width=True)
            with res_col2:
                st.markdown("<h4 style='text-align: center;'>לאחר עיבוד</h4>", unsafe_allow_html=True)
                st.image(final_rgb, use_container_width=True)

            # הורדה
            result_pil = Image.fromarray(final_rgb)
            buf = io.BytesIO()
            result_pil.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="הורד תמונה משופרת (Lossless PNG)",
                data=byte_im,
                file_name="PhotoFix_Pro_Enhanced.png",
                mime="image/png",
                use_container_width=True
            )