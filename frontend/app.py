import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import time
from datetime import datetime

from backend.auth import register_user, login_user
from backend.database.models import create_tables

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Cartoonization Studio", layout="wide")
create_tables()

# ---------------- SESSION INIT ----------------
if "page" not in st.session_state:
    st.session_state.page = "landing"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "image_count" not in st.session_state:
    st.session_state.image_count = 0

if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0

if "account_locked" not in st.session_state:
    st.session_state.account_locked = False


# ---------------- PREMIUM CSS ----------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #667eea, #764ba2);
}
.hero {
    text-align: center;
    padding: 80px 20px;
    color: white;
}
.feature-card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    text-align: center;
}
.feature-card h3 { color: #333; }
.feature-card p { color: #555; }
.card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)


# ---------------- IMAGE EFFECTS ----------------
def cartoon_effect(image):
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray,255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY,9,9)
    color = cv2.bilateralFilter(img,9,250,250)
    cartoon = cv2.bitwise_and(color,color,mask=edges)
    cartoon = cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
    return cartoon

def pencil_sketch_effect(image):
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv,(21,21),0)
    inv_blur = 255 - blur
    sketch = cv2.divide(gray, inv_blur, scale=256.0)
    return cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)

def black_white_effect(image):
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)


# ---------------- LANDING ----------------
def landing_page():
    st.markdown("""
    <div class="hero">
        <h1>🎨 AI Cartoonization Studio</h1>
        <p>Transform your images with AI-powered effects.</p>
    </div>
    """, unsafe_allow_html=True)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.markdown('<div class="feature-card"><h3>⚡ Fast</h3><p>Instant processing</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="feature-card"><h3>🎨 3 Effects</h3><p>Cartoon, Sketch, B/W</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="feature-card"><h3>🔐 Secure</h3><p>Login protected</p></div>', unsafe_allow_html=True)

    if st.button("🚀 Get Started"):
        st.session_state.page = "login"


# ---------------- REGISTER ----------------
def register_page():
    st.subheader("📝 Register")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        success, message = register_user(username,email,password)
        if success:
            st.success(message)
            st.session_state.page = "login"
        else:
            st.error(message)

    if st.button("Already have an account? Login"):
        st.session_state.page = "login"


# ---------------- LOGIN ----------------
def login_page():
    st.subheader("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    st.checkbox("Remember Me")

    if st.session_state.account_locked:
        st.error("🚫 Account locked after 5 failed attempts.")
        return

    if st.button("Login"):

        success, user = login_user(email,password)

        if success:
            st.session_state.logged_in = True
            st.session_state.username = user["username"]
            st.session_state.email = user["email"]
            st.session_state.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            st.session_state.login_attempts = 0
            st.session_state.account_locked = False
            st.session_state.page = "dashboard"

        else:
            st.session_state.login_attempts += 1
            remaining = 5 - st.session_state.login_attempts

            if st.session_state.login_attempts >= 5:
                st.session_state.account_locked = True
                st.error("🚫 Account locked after 5 failed attempts.")
            else:
                st.error(f"Invalid credentials. Attempts left: {remaining}")

    if st.button("Forgot Password?"):
        st.info("Password reset feature coming soon.")

    if st.button("New user? Register"):
        st.session_state.page = "register"


# ---------------- DASHBOARD ----------------
def dashboard_page():

    st.success(f"Welcome, {st.session_state.username} 🎉")

    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("👤 Account Info")
        st.write("Username:", st.session_state.username)
        st.write("Email:", st.session_state.email)
        st.write("Last Login:", st.session_state.last_login)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📊 Quick Stats")
        st.write("Images Processed:", st.session_state.image_count)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    menu = st.radio("Navigation",
        ["🎨 Image Processing","💳 Payment History","⚙ Profile Settings"])

    # -------- IMAGE PROCESSING --------
    if menu == "🎨 Image Processing":

        uploaded_file = st.file_uploader("Upload Image", type=["jpg","jpeg","png"])

        if uploaded_file is not None:
            image = Image.open(uploaded_file)

            effect = st.selectbox("Choose Effect",
                                  ["Cartoon","Pencil Sketch","Black & White"])

            col1,col2 = st.columns(2)
            with col1:
                st.image(image, caption="Original", use_column_width=True)

            start = time.time()

            if effect == "Cartoon":
                result = cartoon_effect(image)
            elif effect == "Pencil Sketch":
                result = pencil_sketch_effect(image)
            else:
                result = black_white_effect(image)

            end = time.time()
            st.session_state.image_count += 1

            with col2:
                st.image(result, caption=effect, use_column_width=True)

            st.success(f"Processing Time: {round(end-start,2)} sec")

            result_img = Image.fromarray(result)
            st.download_button("📥 Download",
                               data=result_img.tobytes(),
                               file_name="processed.png",
                               mime="image/png")

    elif menu == "💳 Payment History":
        st.info("No payments yet.")

    elif menu == "⚙ Profile Settings":
        st.subheader("Update Profile")
        new_username = st.text_input("Change Username")
        if st.button("Update"):
            st.success("Profile updated (demo only).")

    if st.button("Logout"):
        st.session_state.clear()
        st.session_state.page = "landing"


# ---------------- ROUTING ----------------
if st.session_state.page == "landing":
    landing_page()
elif st.session_state.page == "register":
    register_page()
elif st.session_state.page == "login":
    login_page()
elif st.session_state.page == "dashboard":
    if st.session_state.logged_in:
        dashboard_page()
    else:
        st.session_state.page = "login"