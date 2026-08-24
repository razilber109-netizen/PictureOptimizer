import streamlit as st
import cv2
import numpy as np
from PIL import Image

# הגדרות עיצוב עמוד - חובה להיות הפקודה הראשונה!
st.set_page_config(page_title="Image Enhancer Pro", layout="wide")

# CSS נקי להסתרת המיתוג של Streamlit
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("✨ משפר התמונות האוטומטי")
st.write("העלה תמונה והמערכת תנקה ממנה רעשים תוך שמירה על חדות מרבית.")

uploaded_file = st.file_uploader("בחר תמונה", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # קריאת התמונה והמרה לפורמט של OpenCV
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    # הצגת אנימציית טעינה מרשימה בזמן העיבוד
    with st.spinner('מנקה רעשים... (זה עשוי לקחת כמה שניות)'):
        # אלגוריתם הניקוי המתקדם - הערכים פה הם הסטנדרט המומלץ
        denoised_bgr = cv2.fastNlMeansDenoisingColored(img_bgr, None, 10, 10, 7, 21)
        denoised_rgb = cv2.cvtColor(denoised_bgr, cv2.COLOR_BGR2RGB)

    st.success("התמונה נוקתה בהצלחה!")

    # תצוגה מקצועית בשתי עמודות
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("לפני")
        st.image(image, use_column_width=True)
    with col2:
        st.subheader("אחרי")
        st.image(denoised_rgb, use_column_width=True)