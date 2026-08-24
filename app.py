import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import requests
from datetime import datetime
from streamlit_cropper import st_cropper
from streamlit_lottie import st_lottie
from supabase import create_client, Client

# 1. Page Config
st.set_page_config(page_title="PhotoFix Pro", layout="wide")

# --- SUPABASE CONFIGURATION ---
SUPABASE_URL = "https://bdbitcnhwylezraieqdx.supabase.co"
SUPABASE_KEY = "sb_publishable_CKqrK1o8YZ8ZSiAP2iI3Xg_P_hd8j6U"

supabase: Client = None
if SUPABASE_URL:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.error(f"Failed to connect to Supabase: {e}")

# --- Session State Initialization ---
if 'user' not in st.session_state:
    st.session_state.user = None
if 'is_guest' not in st.session_state:
    st.session_state.is_guest = False


# 2. Lottie Animation Loader
@st.cache_data
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None


lottie_ai = load_lottieurl("https://lottie.host/81b10a27-eb63-4560-b636-6927a4216892/O6p6l1hXDe.json")

# 3. Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    .stApp { background-color: #F0F2F5; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}

    .stButton > button {
        background-color: #1877F2; color: #ffffff; font-weight: 600;
        border-radius: 6px; border: none; padding: 0.5rem 1rem; transition: 0.2s;
    }
    .stButton > button:hover { background-color: #166FE5; color: white; }

    .guest-btn > button {
        background-color: #E4E6EB !important; color: #050505 !important;
    }
    .guest-btn > button:hover { background-color: #D8DADF !important; }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff; border-radius: 8px; border: 1px solid #ced0d4 !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1); padding: 1.5rem !important; margin-bottom: 1rem;
    }

    .top-header {
        background: white; padding: 15px 25px; border-radius: 8px; border: 1px solid #ced0d4;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1); margin-bottom: 25px; display: flex; align-items: center; justify-content: space-between;
    }
    .header-left { display: flex; align-items: center; }
    .header-left h1 { color: #1877F2; margin: 0; font-size: 24px; font-weight: bold; }
    .header-left p { color: #65676B; margin: 0; margin-left: 15px; font-size: 15px; padding-top: 5px; }
    .header-right { font-weight: 600; color: #050505; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# AUTHENTICATION PAGE (LOGIN / SIGN UP)
# ==========================================
if not st.session_state.user and not st.session_state.is_guest:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("<h1 style='text-align:center; color:#1877F2;'>🌐 PhotoFix</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; color:#65676B;'>Professional Image Optimization Studio</p><hr>",
                        unsafe_allow_html=True)

            auth_mode = st.radio("Choose action", ["Log In", "Sign Up"], horizontal=True, label_visibility="collapsed")

            email_input = st.text_input("Email Address")
            password_input = st.text_input("Password", type="password")

            st.markdown("<br>", unsafe_allow_html=True)

            if auth_mode == "Log In":
                if st.button("Log In to Account", use_container_width=True):
                    if supabase and email_input and password_input:
                        try:
                            res = supabase.auth.sign_in_with_password(
                                {"email": email_input, "password": password_input})
                            st.session_state.user = res.user
                            st.rerun()
                        except Exception as e:
                            st.error(f"Login failed: {e}")
                    else:
                        st.warning("Please fill in all fields.")
            else:
                if st.button("Create Account (Sign Up)", use_container_width=True):
                    if supabase and email_input and password_input:
                        try:
                            res = supabase.auth.sign_up({"email": email_input, "password": password_input})
                            st.success("Account created successfully! You can now log in.")
                        except Exception as e:
                            st.error(f"Sign up failed: {e}")
                    else:
                        st.warning("Please fill in all fields.")

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<div class='guest-btn'>", unsafe_allow_html=True)
            if st.button("Continue as Guest", use_container_width=True):
                st.session_state.is_guest = True
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# MAIN APP (LOGGED IN OR GUEST)
# ==========================================
else:
    user_identifier = st.session_state.user.email if st.session_state.user else "Guest User"

    st.markdown(f"""
    <div class="top-header">
        <div class="header-left">
            <h1>🌐 PhotoFix</h1>
            <p>Professional Image Enhancement & Optimization Studio</p>
        </div>
        <div class="header-right">
            Hello, {user_identifier} 👋
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_out1, col_out2 = st.columns([10, 1])
    with col_out2:
        if st.button("Log Out"):
            if supabase and st.session_state.user:
                try:
                    supabase.auth.sign_out()
                except:
                    pass
            st.session_state.user = None
            st.session_state.is_guest = False
            st.rerun()

    # --- Main Workspace Layout ---
    col_settings, col_feed = st.columns([1, 2.5], gap="large")

    # --- Left Column: Settings + Inspiration Gallery ---
    with col_settings:
        with st.container(border=True):
            st.markdown("<h3 style='color:#050505; margin-top:0; font-size:18px;'>⚙️ Tools & Settings</h3>",
                        unsafe_allow_html=True)
            st.markdown("<hr style='margin: 10px 0; border-color: #ced0d4;'>", unsafe_allow_html=True)
            enable_cropping = st.toggle("✂️ Manual Crop Tool", value=False)

        with st.container(border=True):
            st.markdown(
                "<h3 style='text-align:center; color:#050505; font-size:18px; margin-top:0;'>✨ Inspiration Gallery</h3>",
                unsafe_allow_html=True)

            # גלריה מתוקנת שנטענת כהלכה בלי תקלות טקסט
            gallery_html = """
            <style>
            .gallery-wrapper { background: white; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #ced0d4; margin-bottom: 15px; }
            .gallery-wrapper img { width: 100%; border-radius: 4px; margin-bottom: 5px; object-fit: cover; }
            .badge { font-size: 11px; font-weight: bold; padding: 3px 8px; border-radius: 12px; display: inline-block; margin: 5px 0; }
            .b-before { background: #E4E6EB; color: #050505; }
            .b-after { background: #1877F2; color: white; }
            .img-before { filter: brightness(60%) contrast(85%) blur(0.5px); }
            .img-after { filter: brightness(110%) contrast(115%) saturate(120%); }
            </style>
            <div style="height: 400px; overflow: hidden;">
              <marquee direction="up" scrollamount="3" height="400px" onmouseover="this.stop();" onmouseout="this.start();">
            """
            images = ["https://picsum.photos/id/10/400/300", "https://picsum.photos/id/11/400/300",
                      "https://picsum.photos/id/13/400/300"]
            for img in images * 2:
                gallery_html += f"""
                <div class="gallery-wrapper">
                    <span class="badge b-before">Original</span>
                    <img class="img-before" src="{img}" />
                    <span class="badge b-after">PhotoFix Enhanced</span>
                    <img class="img-after" src="{img}" />
                </div>
                """
            gallery_html += "</marquee></div>"
            st.markdown(gallery_html, unsafe_allow_html=True)

    # --- Right Column: Studio / Personal Gallery Tabs ---
    with col_feed:
        if st.session_state.user:
            tab_studio, tab_gallery = st.tabs(["🎨 Edit Studio", "📁 Cloud Personal Gallery"])
        else:
            tab_studio = st.container()
            tab_gallery = None

        # TAB 1: STUDIO
        with tab_studio:
            with st.container(border=True):
                st.markdown("<h3 style='color:#050505; margin-top:0; font-size:18px;'>📸 Upload Workspace</h3>",
                            unsafe_allow_html=True)
                uploaded_file = st.file_uploader("Drag and drop or browse files", type=['jpg', 'jpeg', 'png'])

            if uploaded_file is not None:
                image = Image.open(uploaded_file)

                with st.container(border=True):
                    if enable_cropping:
                        st.markdown("<h4 style='color:#050505; font-size:16px;'>Select the exact area to crop:</h4>",
                                    unsafe_allow_html=True)
                        img_to_process = st_cropper(image, realtime_update=True, box_color='#1877F2')
                    else:
                        img_to_process = image
                        st.markdown("<h4 style='color:#050505; font-size:16px;'>Live Preview:</h4>",
                                    unsafe_allow_html=True)
                        st.image(image, use_container_width=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    process_btn = st.button("🚀 Run Advanced Enhancement", use_container_width=True)

                if process_btn:
                    loading_placeholder = st.empty()
                    with loading_placeholder.container():
                        st.markdown(
                            "<h4 style='text-align:center; color:#1877F2;`>Analyzing and optimizing image...</h4>",
                            unsafe_allow_html=True)
                        if lottie_ai:
                            st_lottie(lottie_ai, height=150, key="loading_anim")

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

                    result_pil = Image.fromarray(final_rgb)

                    # --- SAVE TO SUPABASE CLOUD STORAGE ---
                    if st.session_state.user and supabase:
                        try:
                            buf_temp = io.BytesIO()
                            result_pil.save(buf_temp, format="PNG")
                            byte_data = buf_temp.getvalue()

                            safe_email = st.session_state.user.email.replace("@", "_at_").replace(".", "_")
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            file_path = f"{safe_email}/PhotoFix_{timestamp}.png"

                            supabase.storage.from_("user-images").upload(
                                file=byte_data,
                                path=file_path,
                                file_options={"content-type": "image/png", "upsert": "true"}
                            )
                        except Exception as e:
                            st.error(f"Cloud upload error: {e}")

                    loading_placeholder.empty()

                    with st.container(border=True):
                        st.markdown("<h3 style='color:#050505; font-size:18px; margin-top:0;'>✨ Final Results</h3>",
                                    unsafe_allow_html=True)

                        res_col1, res_col2 = st.columns(2)
                        with res_col1:
                            st.markdown("<p style='text-align:center; font-weight:bold; color:#65676B;'>Original</p>",
                                        unsafe_allow_html=True)
                            st.image(img_to_process, use_container_width=True)
                        with res_col2:
                            st.markdown("<p style='text-align:center; font-weight:bold; color:#1877F2;'>Enhanced</p>",
                                        unsafe_allow_html=True)
                            st.image(final_rgb, use_container_width=True)

                        buf = io.BytesIO()
                        result_pil.save(buf, format="PNG")
                        byte_im = buf.getvalue()

                        st.markdown("<br>", unsafe_allow_html=True)
                        st.download_button(
                            label="📥 Download High-Quality PNG",
                            data=byte_im,
                            file_name="PhotoFix_Premium_Enhanced.png",
                            mime="image/png",
                            use_container_width=True
                        )

        # TAB 2: CLOUD PERSONAL GALLERY
        if tab_gallery:
            with tab_gallery:
                with st.container(border=True):
                    st.markdown("<h3 style='color:#050505; margin-top:0; font-size:18px;'>📁 My Cloud Gallery</h3>",
                                unsafe_allow_html=True)
                    st.markdown("<hr style='margin: 10px 0; border-color: #ced0d4;'>", unsafe_allow_html=True)

                    if supabase and st.session_state.user:
                        try:
                            safe_email = st.session_state.user.email.replace("@", "_at_").replace(".", "_")
                            files = supabase.storage.from_("user-images").list(safe_email)

                            if files and len(files) > 0:
                                cols = st.columns(3)
                                for i, file_info in enumerate(files):
                                    file_name = file_info.get('name')
                                    if file_name and file_name != ".emptyFolderPlaceholder":
                                        public_url = supabase.storage.from_("user-images").get_public_url(
                                            f"{safe_email}/{file_name}")

                                        with cols[i % 3]:
                                            st.image(public_url, use_container_width=True)
                                            st.markdown(
                                                f"<a href='{public_url}' target='_blank'><button style='width:100%; background-color:#1877F2; color:white; border:none; border-radius:6px; padding:6px; font-weight:600; cursor:pointer;'>📥 Open / Download</button></a>",
                                                unsafe_allow_html=True)
                            else:
                                st.info("Your cloud gallery is empty. Enhance your first photo in the studio!")
                        except Exception as e:
                            st.error(f"Could not load gallery from cloud: {e}")
                    else:
                        st.warning("Supabase credentials are not configured yet.")