import streamlit as st
from backend.auth import register_user

# Page config
st.set_page_config(
    page_title="Register | AI Cartoonization",
    page_icon="🎨",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
body {
    background-color: #0f172a;
}
.main {
    background-color: #0f172a;
}
.card {
    background-color: #1e293b;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.4);
}
h1 {
    color: #38bdf8;
    text-align: center;
}
label {
    color: white !important;
}
.stTextInput input {
    background-color: #020617;
    color: white;
    border-radius: 8px;
}
.stButton button {
    background: linear-gradient(90deg, #38bdf8, #6366f1);
    color: white;
    border-radius: 10px;
    height: 45px;
    font-size: 18px;
}
.stCheckbox label {
    color: #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# UI Card
st.markdown("<div class='card'>", unsafe_allow_html=True)

st.markdown("<h1>📝 Create Your Account</h1>", unsafe_allow_html=True)

username = st.text_input("👤 Username")
email = st.text_input("📧 Email")

password = st.text_input("🔒 Password", type="password")
confirm_password = st.text_input("🔁 Confirm Password", type="password")

terms = st.checkbox("I agree to the Terms & Conditions")

if st.button("🚀 Register"):
    if not username or not email or not password:
        st.error("⚠️ All fields are required")

    elif password != confirm_password:
        st.error("❌ Passwords do not match")

    elif not terms:
        st.error("📜 Please accept terms & conditions")

    else:
        success, message = register_user(username, email, password)
        if success:
            st.success("🎉 " + message)
        else:
            st.error("❌ " + message)

st.markdown("</div>", unsafe_allow_html=True)