import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
from streamlit_cropper import st_cropper

# הגדרת הדף - חובה להיות ראשון
st.set_page_config(page_title="PhotoFix", layout="wide")

# עיצוב בסגנון פייסבוק (כרטיסיות לבנות, רקע אפור, כחול רשמי)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Segoe UI', 'Assistant', Tahoma, Geneva, Verdana, sans-serif !important;
    }

    /* הרקע האפור המוכר של פייסבוק */
    .stApp {
        background-color: #F0F2F5;
    }

    /* הסתרת המיתוג של Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* עיצוב כפתורים לכחול פייסבוק */
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

    /* עיצוב ה"כרטיסיות" (Cards) שנותן את המראה המגודר והמסודר */
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

# ----------------- החלק העליון (סוג של תפריט/Header) -----------------
with st.container(border=True):
    col_icon, col_title = st.columns([1, 20])
    with col_icon:
        # אייקון פשוט ובטוח שלא יישבר
        st.markdown("<h1 style='color:#1877F2; margin:0; font-size: 2.5rem;'>🌐</h1>", unsafe_allow_html=True)
    with col_title:
        st.markdown("<h1 style='color:#1877F2; margin:0; font-weight:700; line-height:1.2;'>PhotoFix</h1>",
                    unsafe_allow_html=True)
        st.markdown(
            "<span style='color:#65676B; font-size:15px;'>מערכת חכמה לשיפור תמונות ואופטימיזציה מבית היוצר שלך</span>",
            unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ----------------- אזור העבודה המרכזי -----------------
# חלוקה ל-2 עמודות: הגדרות בצד שמאל/ימין (בהתאם לכיוון) ופיד עבודה מרכזי
col_settings, col_feed = st.columns([1, 2.5], gap="large")

with col_settings:
    # כרטיסיית הגדרות
    with st.container(border=True):
        st.markdown("<h3 style='color:#050505; margin-top:0; font-size:18px;'>⚙️ הגדרות</h3>", unsafe_allow_html=True)
        st.markdown("<hr style='margin: 10px 0; border-color: #ced0d4;'>", unsafe_allow_html=True)

        enable_cropping = st.toggle("✂️ הפעל כלי חיתוך ידני", value=False)

        st.markdown("<hr style='margin: 10px 0; border-color: #ced0d4;'>", unsafe_allow_html=True)
        st.markdown(
            "<p style='font-size:14px; color:#65676B; line-height:1.6;'><b>הוראות:</b><br>1. העלה תמונה לאזור המרכזי.<br>2. בחר האם לחתוך אותה (כאן למעלה).<br>3. הפעל את מנוע השיפור.</p>",
            unsafe_allow_html=True)

with col_feed:
    # כרטיסיית העלאת תמונה ("פוסט חדש")
    with st.container(border=True):
        st.markdown("<h3 style='color:#050505; margin-top:0; font-size:18px;'>📸 העלאת תמונה</h3>",
                    unsafe_allow_html=True)
        uploaded_file = st.file_uploader("בחר או גרור תמונה לכאן", type=['jpg', 'jpeg', 'png'])

    # אם הועלתה תמונה - פותחים כרטיסייה חדשה להמשך העבודה
    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        with st.container(border=True):
            if enable_cropping:
                st.markdown("<h4 style='color:#050505; font-size:16px;'>סמן את האזור המדויק שתרצה לשמור:</h4>",
                            unsafe_allow_html=True)
                # כלי החיתוך בצבע כחול
                img_to_process = st_cropper(image, realtime_update=True, box_color='#1877F2')
            else:
                img_to_process = image
                st.markdown("<h4 style='color:#050505; font-size:16px;'>תצוגה מקדימה של התמונה:</h4>",
                            unsafe_allow_html=True)
                st.image(image, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # כפתור פעולה ענק וברור
            process_btn = st.button("🚀 הפעל שיפור תמונה איכותי", use_container_width=True)

        # אם המשתמש לחץ על כפתור השיפור - כרטיסיית התוצאות
        if process_btn:
            with st.container(border=True):
                st.markdown("<h3 style='color:#050505; font-size:18px; margin-top:0;'>✨ תוצאות העיבוד</h3>",
                            unsafe_allow_html=True)

                img_array = np.array(img_to_process)
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

                with st.spinner('מנתח את התמונה ומשפר איכות...'):
                    # אופטימיזציית תאורה (CLAHE)
                    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
                    l, a, b = cv2.split(lab)
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                    cl = clahe.apply(l)
                    limg = cv2.merge((cl, a, b))
                    optimized_bgr = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

                    # ניקוי רעשים
                    final_bgr = cv2.fastNlMeansDenoisingColored(optimized_bgr, None, 5, 5, 7, 21)
                    final_rgb = cv2.cvtColor(final_bgr, cv2.COLOR_BGR2RGB)

                # הצגה של לפני ואחרי בתוך הכרטיסייה
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.markdown("<p style='text-align:center; font-weight:bold; color:#65676B;'>לפני (מקור)</p>",
                                unsafe_allow_html=True)
                    st.image(img_to_process, use_container_width=True)
                with res_col2:
                    st.markdown("<p style='text-align:center; font-weight:bold; color:#1877F2;'>אחרי (משופר)</p>",
                                unsafe_allow_html=True)
                    st.image(final_rgb, use_container_width=True)

                # הכנה להורדה
                result_pil = Image.fromarray(final_rgb)
                buf = io.BytesIO()
                result_pil.save(buf, format="PNG")
                byte_im = buf.getvalue()

                st.markdown("<br>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 הורד תמונה למחשב (PNG איכותי)",
                    data=byte_im,
                    file_name="PhotoFix_Enhanced.png",
                    mime="image/png",
                    use_container_width=True
                )