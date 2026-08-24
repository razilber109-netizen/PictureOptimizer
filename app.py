import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
from streamlit_cropper import st_cropper

# הגדרת הפריסה לרחבה כדי שסרגל הצד ייראה טוב
st.set_page_config(page_title="PhotoFix", layout="wide")

# עיצוב CSS מתקדם: רקע גיאומטרי, מיתוג וטקסט רץ
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Assistant', sans-serif; }

    /* הוספת רקע גיאומטרי עכשווי (עיגולי תאורה על רקע כהה) */
    .stApp {
        background-color: #0f172a;
        background-image: radial-gradient(circle at 15% 50%, rgba(56, 189, 248, 0.1), transparent 25%), 
                          radial-gradient(circle at 85% 30%, rgba(139, 92, 246, 0.15), transparent 25%);
        color: white;
    }

    /* מיתוג PhotoFix */
    .brand-title {
        font-size: 4rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #38bdf8, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }

    /* אנימציה לגלריה הרצה בצד */
    .marquee {
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        background: rgba(255,255,255,0.05);
        padding: 15px 0;
        border-radius: 10px;
    }
    .marquee p {
        display: inline-block;
        animation: scroll 15s linear infinite;
        color: #38bdf8;
        font-weight: bold;
        margin: 0;
    }
    @keyframes scroll {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# אזור סרגל הצד (Sidebar) לגלריה רצה
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>גלריית השראה</h2>", unsafe_allow_html=True)
    st.markdown('<div class="marquee"><p>📸 תמונה 1: מקור ➡️ עיבוד | 📸 תמונה 2: מקור ➡️ עיבוד </p></div>',
                unsafe_allow_html=True)
    st.write("כאן ניתן לקשר בהמשך תיקיית תמונות אמיתית שתרוץ בצד.")

# כותרת ראשית במרכז המסך
st.markdown('<h1 class="brand-title">📸 PhotoFix</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>פלטפורמה מקצועית לחיתוך, ניקוי ושיפור תאורת תמונות.</p>",
            unsafe_allow_html=True)
st.markdown("---")

uploaded_file = st.file_uploader("העלה תמונה להתחלת עבודה", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.markdown("### ✂️ 1. חיתוך התמונה")
    # הצגת ממשק החיתוך
    cropped_img = st_cropper(image, realtime_update=True, box_color='#38bdf8')

    st.markdown("### 🪄 2. עיבוד והורדה")
    if st.button("החל אופטימיזציה על האזור החתוך"):
        img_array = np.array(cropped_img)
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        with st.spinner('משפר ניגודיות ומנקה רעשים...'):
            # שיפור תאורה מקומי
            lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            limg = cv2.merge((cl, a, b))
            optimized_bgr = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

            # החלקת רעשים עדינה
            final_bgr = cv2.fastNlMeansDenoisingColored(optimized_bgr, None, 5, 5, 7, 21)
            final_rgb = cv2.cvtColor(final_bgr, cv2.COLOR_BGR2RGB)

        st.image(final_rgb, caption="התמונה המוכנה", use_container_width=True)

        # המרה חזרה לפורמט PNG שאינו מאבד מידע (Lossless)
        result_pil = Image.fromarray(final_rgb)
        buf = io.BytesIO()
        result_pil.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(
            label="📥 הורד תמונה מלאה באיכות מקסימלית",
            data=byte_im,
            file_name="PhotoFix_Enhanced.png",
            mime="image/png"
        )