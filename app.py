import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
from streamlit_cropper import st_cropper

# הגדרת פריסה רחבה
st.set_page_config(page_title="PhotoFix Pro", layout="wide")

# עיצוב פרימיום נקי - פונט יוקרתי, צלליות רכות וצבעים טבעיים
st.markdown("""
<style>
    /* ייבוא פונט Rubik - מודרני, נקי ומשדר יוקרה */
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;700&display=swap');

    html, body, [class*="css"] { 
        font-family: 'Rubik', sans-serif !important; 
    }

    /* רקע בהיר ונקי לאתר */
    .stApp {
        background-color: #f8fafc;
    }

    /* עיצוב הפאנל הצדדי (הכרטיסייה) */
    .control-panel {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }

    /* עיצוב הלוגו */
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        margin-top: 10px;
    }

    .brand-text {
        font-size: 3.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        line-height: 1.2;
    }

    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        font-weight: 300;
        margin-top: -5px;
        margin-bottom: 40px;
    }

    /* הסתרת מיתוג Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ----- לוגו מבוסס SVG מותאם לעיצוב הבהיר -----
svg_logo = """
<svg width="45" height="45" viewBox="0 0 24 24" fill="none" stroke="url(#grad1)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#2563eb;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#7c3aed;stop-opacity:1" />
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
<div class="subtitle">מערכת חכמה לשיפור תמונות, ניקוי רעשים ואופטימיזציית תאורה</div>
""", unsafe_allow_html=True)

# ----- חלוקת המסך לעמודות -----
control_col, workspace_col = st.columns([1, 3], gap="large")

# עמודת ההגדרות (צד ימין)
with control_col:
    st.markdown('<div class="control-panel">', unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:#1e293b; margin-top:0;'>הגדרות עבודה</h3>", unsafe_allow_html=True)
    st.divider()

    enable_cropping = st.toggle("✂️ הפעל כלי חיתוך", value=False)

    st.divider()
    st.markdown(
        "<p style='font-size: 0.95rem; color: #64748b; line-height:1.5;'>העלה תמונה באזור העבודה, בחר האם לחתוך אותה, ולאחר מכן הפעל את אלגוריתם השיפור.</p>",
        unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# עמודת אזור העבודה (צד שמאל)
with workspace_col:
    uploaded_file = st.file_uploader("גרור קובץ או לחץ לבחירה", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        st.markdown("<br>", unsafe_allow_html=True)
        if enable_cropping:
            st.markdown("<h4 style='color:#1e293b;'>סמן את האזור הרצוי לחיתוך:</h4>", unsafe_allow_html=True)
            img_to_process = st_cropper(image, realtime_update=True, box_color='#2563eb')
        else:
            img_to_process = image
            st.markdown("<h4 style='color:#1e293b;'>תצוגה מקדימה:</h4>", unsafe_allow_html=True)
            st.image(image, width=600)

        st.markdown("<br>", unsafe_allow_html=True)

        # כפתור עיבוד
        if st.button("✨ החל שיפור תמונה מתקדם", use_container_width=True):
            img_array = np.array(img_to_process)
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

            with st.spinner('מנתח את התמונה ומשפר איכות...'):
                lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
                l, a, b = cv2.split(lab)
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                cl = clahe.apply(l)
                limg = cv2.merge((cl, a, b))
                optimized_bgr = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

                final_bgr = cv2.fastNlMeansDenoisingColored(optimized_bgr, None, 5, 5, 7, 21)
                final_rgb = cv2.cvtColor(final_bgr, cv2.COLOR_BGR2RGB)

            st.success("העיבוד הושלם בהצלחה!")

            # תצוגת התוצאות
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.markdown("<h4 style='text-align: center; color:#1e293b;'>תמונת מקור</h4>", unsafe_allow_html=True)
                st.image(img_to_process, use_container_width=True)
            with res_col2:
                st.markdown("<h4 style='text-align: center; color:#1e293b;'>לאחר עיבוד</h4>", unsafe_allow_html=True)
                st.image(final_rgb, use_container_width=True)

            # המרה לשמירה והורדה
            result_pil = Image.fromarray(final_rgb)
            buf = io.BytesIO()
            result_pil.save(buf, format="PNG")
            byte_im = buf.getvalue()

            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="📥 הורד תמונה משופרת (Lossless PNG)",
                data=byte_im,
                file_name="PhotoFix_Pro_Enhanced.png",
                mime="image/png",
                use_container_width=True
            )