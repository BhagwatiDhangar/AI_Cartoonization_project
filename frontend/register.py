import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from backend.auth import register_user

st.set_page_config(page_title="Register", layout="centered")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #141e30, #243b55);
}

header {visibility: hidden;}

.block-container {
    max-width: 420px;
    padding-top: 40px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## 📝 Create Account")
st.write("Join AI Cartoonization Studio")

username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")
terms = st.checkbox("I agree to the Terms & Conditions")

if st.button("REGISTER"):

    if not username or not email or not password:
        st.error("All fields are required.")

    elif password != confirm_password:
        st.error("Passwords do not match.")

    elif not terms:
        st.error("You must accept the Terms & Conditions.")

    else:
        success, message = register_user(username, email, password)

        if success:
            st.success("Registration successful 🎉")
            st.info("Now run login.py to login.")
        else:
            st.error(message)

st.divider()

st.info("Already have account? Run login.py file.")
st.divider()

st.markdown(
    """
    <a href="http://localhost:8501/?page=login" target="_self">
        <button style="
            width:100%;
            padding:10px;
            border-radius:8px;
            background:#444;
            color:white;
            border:none;">
            Go to Login
        </button>
    </a>
    """,
    unsafe_allow_html=True
)