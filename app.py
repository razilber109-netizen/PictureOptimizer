import streamlit as st
from PIL import Image, ImageEnhance, ImageOps
import io

# 1. Page Configuration (Must be first)
st.set_page_config(page_title="AI Image Enhancer", layout="wide")

# 2. Custom CSS for Professional UI
st.markdown("""
    <style>
    /* Clean fonts and text colors */
    h1 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #1f2937;
        text-align: center;
        font-weight: 700;
        margin-top: 20px;
    }
    h3 {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #374151;
        font-weight: 500;
    }
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 1.2rem;
        margin-bottom: 40px;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    /* Hide Streamlit default hamburger menu and footer for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. Header Section
st.markdown("<h1>AI Image Enhancer</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Instantly optimize lighting, contrast, and color balance with professional accuracy.</p>",
    unsafe_allow_html=True)

# 4. Example Gallery (Before & After Catalog)
st.markdown("<h3 style='text-align: center;'>See the Difference</h3>", unsafe_allow_html=True)
st.write("")  # Small spacing

gal_col1, gal_col2 = st.columns(2)
with gal_col1:
    st.markdown("<p style='text-align:center; color:#6b7280; font-size: 0.9rem;'>Original</p>", unsafe_allow_html=True)
    # Placeholder image for "Before"
    st.image("https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=600&auto=format&fit=crop",
             use_container_width=True)

with gal_col2:
    st.markdown("<p style='text-align:center; color:#6b7280; font-size: 0.9rem;'>Enhanced</p>", unsafe_allow_html=True)
    # Placeholder image for "After" (slightly different lighting/edit from unsplash)
    st.image(
        "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=100&w=600&auto=format&fit=crop&sat=30&con=20",
        use_container_width=True)

st.divider()

# 5. Upload Section
st.markdown("<h3 style='text-align: center;'>Upload Your Image</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

# 6. Processing Section
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_format = image.format if image.format else "JPEG"

    # AI/Math Optimization
    auto_image = ImageOps.autocontrast(image, cutoff=1)
    auto_image = ImageEnhance.Color(auto_image).enhance(1.15)
    auto_image = ImageEnhance.Sharpness(auto_image).enhance(1.2)

    st.markdown("<h3 style='margin-top: 40px; text-align: center;'>Optimization Results</h3>", unsafe_allow_html=True)
    st.write("")

    # Displaying results Left to Right
    res_col1, res_col2 = st.columns(2)

    with res_col1:
        st.markdown("<p style='text-align:center; font-weight:bold;'>Original Image</p>", unsafe_allow_html=True)
        st.image(image, use_container_width=True)

    with res_col2:
        st.markdown("<p style='text-align:center; font-weight:bold;'>Enhanced Image</p>", unsafe_allow_html=True)
        st.image(auto_image, use_container_width=True)

        # Prepare High-Quality Download
        buf = io.BytesIO()
        if img_format == "JPEG":
            auto_image.save(buf, format=img_format, quality=100, subsampling=0)
        else:
            auto_image.save(buf, format=img_format)

        byte_im = buf.getvalue()

        # Professional looking download button
        st.download_button(
            label="Download Enhanced Image",
            data=byte_im,
            file_name=f"enhanced_image.{img_format.lower()}",
            mime=f"image/{img_format.lower()}",
            use_container_width=True
        )