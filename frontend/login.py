import streamlit as st
from backend.auth import login_user

st.set_page_config(
    page_title="Login | AI Cartoonization",
    page_icon="🎨",
    layout="centered"
)

# Session state initialize
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:

    st.markdown("""
    <style>
    body { background-color: #0f172a; }
    .card {
        background-color: #1e293b;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 0px 20px rgba(0,0,0,0.4);
    }
    h1 { color: #38bdf8; text-align: center; }
    label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h1>🔐 Login</h1>", unsafe_allow_html=True)

    email_or_username = st.text_input("📧 Email or Username")
    password = st.text_input("🔒 Password", type="password")

    if st.button("Login"):
        success, result = login_user(email_or_username, password)

        if success:
            st.session_state.logged_in = True
            st.session_state.user = result
            st.success("Login successful 🎉")
            st.rerun()
        else:
            st.error(result)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- DASHBOARD ----------------
else:
    user = st.session_state.user

    st.sidebar.title("📂 Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Image Processing", "Payment History", "Profile", "Logout"]
    )

    if page == "Dashboard":
        st.title(f"👋 Welcome, {user['username']}!")
        st.write("This is your dashboard.")
        st.info("Use the sidebar to navigate.")

    elif page == "Image Processing":
        st.title("🎨 Image Cartoonization")
        st.write("Image processing module will be added here.")

    elif page == "Payment History":
        st.title("💳 Payment History")
        st.write("Payments data will appear here.")

    elif page == "Profile":
        st.title("👤 Profile Details")
        st.write(f"Username: {user['username']}")
        st.write(f"Email: {user['email']}")

    elif page == "Logout":
        st.session_state.logged_in = False
        st.session_state.user = None
        st.success("Logged out successfully")
        st.rerun()