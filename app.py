import streamlit as st
import cv2
import numpy as np
from PIL import Image

# הגדרות עמוד - פריסה ממורכזת ונקייה
st.set_page_config(page_title="Image Enhancement Tool", layout="centered")

# עיצוב מוקפד ומינימליסטי בסגנון Google Material
clean_google_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Assistant', sans-serif;
    }

    /* הסתרת אלמנטים מיותרים של סטרים-ליט */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* רקע לבן ונקי לכל האתר */
    .stApp {
        background-color: #ffffff;
    }

    /* טיפוגרפיה מקצועית לכותרות */
    h1 {
        color: #202124;
        font-weight: 500;
        font-size: 2.2rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    p {
        color: #5f6368;
        font-size: 1rem;
        text-align: center;
        margin-bottom: 2rem;
    }

    h3 {
        color: #3c4043;
        font-size: 1.1rem;
        font-weight: 500;
        text-align: center;
        margin-bottom: 1rem;
    }

    /* עיצוב עדין ונקי לאזור העלאת הקבצים */
    [data-testid="stFileUploadDropzone"] {
        border: 1px solid #dadce0 !important;
        border-radius: 8px !important;
        background-color: #ffffff !important;
        padding: 2rem !important;
        transition: all 0.2s ease;
    }
    [data-testid="stFileUploadDropzone"]:hover {
        border: 1px solid #1a73e8 !important;
        background-color: #f8f9fa !important;
    }

    /* מסגרת עדינה לתמונות המוצגות */
    [data-testid="stImage"] img {
        border: 1px solid #e8eaed;
        border-radius: 4px;
    }
</style>
"""
st.markdown(clean_google_css, unsafe_allow_html=True)

# ----- תוכן האתר -----

st.markdown("<h1>כלי לשיפור איכות תמונה</h1>", unsafe_allow_html=True)
st.markdown("<p>מערכת אוטומטית לניקוי רעשים ואופטימיזציה של תאורה וצבע.</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("בחר או גרור קובץ תמונה לכאן", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # קריאת התמונה
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    with st.spinner('מעבד את התמונה...'):
        # 1. שלב האופטימיזציה (CLAHE) לשיפור ניגודיות
        lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        optimized_bgr = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

        # 2. שלב ניקוי הרעשים
        final_bgr = cv2.fastNlMeansDenoisingColored(optimized_bgr, None, 5, 5, 7, 21)

        # המרה חזרה להצגה במסך
        final_rgb = cv2.cvtColor(final_bgr, cv2.COLOR_BGR2RGB)

    st.markdown("<br>", unsafe_allow_html=True)

    # תצוגה זה לצד זה
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h3>תמונת מקור</h3>", unsafe_allow_html=True)
        st.image(image, use_container_width=True)
    with col2:
        st.markdown("<h3>לאחר עיבוד</h3>", unsafe_allow_html=True)
        st.image(final_rgb, use_container_width=True)