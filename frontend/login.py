import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from backend.auth import login_user
from datetime import datetime

st.set_page_config(page_title="Login", layout="centered")

# -------- SESSION INIT --------
if "login_attempts" not in st.session_state:
    st.session_state.login_attempts = 0

if "account_locked" not in st.session_state:
    st.session_state.account_locked = False

# -------- CSS --------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

header {visibility: hidden;}

.block-container {
    max-width: 420px;
    padding-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# -------- UI --------
st.markdown("## 🔐 Sign In")
st.write("Access your creative workspace")

email = st.text_input("Email or Username")
password = st.text_input("Password", type="password")
remember = st.checkbox("Remember Me")

if st.session_state.account_locked:
    st.error("🚫 Account locked after 5 failed login attempts.")
else:
    if st.button("SIGN IN"):

        success, user = login_user(email, password)

        if success:
            st.session_state.logged_in = True
            st.session_state.username = user["username"]
            st.session_state.email = user["email"]
            st.session_state.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.login_attempts = 0

            st.success("Login successful 🎉")
            st.write("Welcome,", user["username"])

        else:
            st.session_state.login_attempts += 1
            remaining = 5 - st.session_state.login_attempts

            if st.session_state.login_attempts >= 5:
                st.session_state.account_locked = True
                st.error("🚫 Account locked after 5 failed attempts.")
            else:
                st.error(f"Invalid credentials. Attempts left: {remaining}")

st.divider()

st.info("New user? Run register.py file to create account.")
st.divider()

if st.button("Go to Register"):
    st.markdown("👉 Please stop this file and run:")
    st.code("streamlit run frontend/register.py")
st.divider()

st.markdown(
    """
    <a href="http://localhost:8501/?page=register" target="_self">
        <button style="
            width:100%;
            padding:10px;
            border-radius:8px;
            background:#444;
            color:white;
            border:none;">
            Go to Register
        </button>
    </a>
    """,
    unsafe_allow_html=True
)