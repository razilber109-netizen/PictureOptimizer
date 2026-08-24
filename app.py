import streamlit as st
import cv2
import numpy as np
from PIL import Image

# הגדרות עמוד - פריסה ממורכזת ונקייה
st.set_page_config(page_title="Image Optimizer Pro", layout="centered")

# עיצוב מתקדם (CSS) לאתר - צבעים, פינות מעוגלות והסתרת מיתוג
st.markdown("""
    <style>
    /* הסתרת התפריט של Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* עיצוב רקע האפליקציה והכותרות */
    .stApp {background-color: #f4f7f6;}
    h1 {color: #1e3d59; text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}

    /* עיצוב כפתור העלאת הקובץ */
    .stFileUploader > div > div > div > button {
        background-color: #ff6e40;
        color: white;
        border-radius: 10px;
        font-weight: bold;
    }

    /* עיצוב הקופסאות של התמונות */
    .css-1v0mbdj {border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);}
    </style>
""", unsafe_allow_html=True)

st.title("📸 שדרוג וניקוי תמונות אוטומטי")
st.write(
    "<p style='text-align: center; color: #555;'>העלה תמונה והמערכת תשפר את הניגודיות, תדגיש צבעים ותנקה רעשי רקע באופן אוטומטי.</p>",
    unsafe_allow_html=True)

st.markdown("---")

uploaded_file = st.file_uploader("בחר תמונה לשיפור", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # קריאת התמונה
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    with st.spinner('מבצע קסמים על התמונה... ⏳'):
        # 1. שלב האופטימיזציה (CLAHE) לשיפור ניגודיות
        lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        optimized_bgr = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

        # 2. שלב ניקוי הרעשים (בעוצמה עדינה של 5 במקום 10)
        final_bgr = cv2.fastNlMeansDenoisingColored(optimized_bgr, None, 5, 5, 7, 21)

        # המרה חזרה להצגה במסך
        final_rgb = cv2.cvtColor(final_bgr, cv2.COLOR_BGR2RGB)

    st.success("✨ התמונה שודרגה בהצלחה!")

    # תצוגה זה לצד זה
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h3 style='text-align: center;'>המקור</h3>", unsafe_allow_html=True)
        st.image(image, use_column_width=True)
    with col2:
        st.markdown("<h3 style='text-align: center;'>אחרי שיפור</h3>", unsafe_allow_html=True)
        st.image(final_rgb, use_column_width=True)