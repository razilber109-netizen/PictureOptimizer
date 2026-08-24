import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
from streamlit_cropper import st_cropper

# הגדרת פריסה רחבה ופתיחה אוטומטית של סרגל הצד
st.set_page_config(page_title="PhotoFix", layout="wide", initial_sidebar_state="expanded")

# CSS נקי ומתוקן - שומר על היציבות של האתר
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;800&display=swap');

    html, body, [class*="css"] { 
        font-family: 'Assistant', sans-serif; 
    }

    /* עיצוב רקע כהה ונקי לכל האתר */
    .stApp {
        background-color: #0f172a;
    }

    /* מיתוג PhotoFix */
    .brand-title {
        font-size: 4rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #38bdf8, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding-bottom: 10px;
    }

    /* תיקון צבעי טקסט כלליים לרקע כהה */
    p, label, span, div, h1, h2, h3, h4 {
        color: #f8fafc !important;
    }

    /* הסתרת מיתוג של Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ----- סרגל צד (Sidebar) -----
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>⚙️ הגדרות</h2>", unsafe_allow_html=True)
    st.divider()
    # כפתור הבחירה האם לחתוך את התמונה
    enable_cropping = st.toggle("✂️ הפעל כלי חיתוך ידני", value=False)
    st.divider()
    st.markdown("### 🖼️ גלריית השראה")
    st.info("מקום שמור לתמונות לפני/אחרי שיוצגו כדוגמה למשתמשים.")

# ----- תוכן מרכזי -----
st.markdown('<h1 class="brand-title">📸 PhotoFix</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>העלה תמונה לשיפור אוטומטי של תאורה, ניגודיות וניקוי רעשים.</p>",
            unsafe_allow_html=True)
st.markdown("---")

uploaded_file = st.file_uploader("בחר קובץ להתחלה", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    # שלב 1: בדיקה האם המשתמש בחר לחתוך
    if enable_cropping:
        st.markdown("### ✂️ סמן את האזור הרצוי")
        img_to_process = st_cropper(image, realtime_update=True, box_color='#38bdf8')
    else:
        # אם לא נבחר חיתוך, נעבוד על התמונה המלאה
        img_to_process = image
        st.image(image, caption="התמונה המקורית", width=500)

    st.markdown("<br>", unsafe_allow_html=True)

    # כפתור פעולה מרכזי ובולט
    if st.button("✨ הפעל אלגוריתם אופטימיזציה", use_container_width=True):
        img_array = np.array(img_to_process)
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        with st.spinner('מבצע קסמים על התמונה... ⏳'):
            # שיפור תאורה (CLAHE)
            lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            limg = cv2.merge((cl, a, b))
            optimized_bgr = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

            # ניקוי רעשים
            final_bgr = cv2.fastNlMeansDenoisingColored(optimized_bgr, None, 5, 5, 7, 21)
            final_rgb = cv2.cvtColor(final_bgr, cv2.COLOR_BGR2RGB)

        st.success("העיבוד הושלם!")

        # תצוגת השוואה מדויקת
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h3 style='text-align: center;'>המקור</h3>", unsafe_allow_html=True)
            st.image(img_to_process, use_container_width=True)
        with col2:
            st.markdown("<h3 style='text-align: center;'>אחרי עיבוד</h3>", unsafe_allow_html=True)
            st.image(final_rgb, use_container_width=True)

        # הכנה להורדה איכותית
        result_pil = Image.fromarray(final_rgb)
        buf = io.BytesIO()
        result_pil.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="📥 הורד תמונה באיכות מקסימלית",
            data=byte_im,
            file_name="PhotoFix_Enhanced.png",
            mime="image/png",
            use_container_width=True
        )