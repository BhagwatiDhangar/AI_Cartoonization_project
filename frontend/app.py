import streamlit as st
import sqlite3
import hashlib
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from datetime import datetime
import uuid
import os
import random

# ================= PAGE CONFIG =================
st.set_page_config(page_title="AI Cartoon Studio", layout="wide")

# ================= FOLDER =================
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# ================= DATABASE =================
conn = sqlite3.connect("app.db", check_same_thread=False)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
email TEXT UNIQUE,
password TEXT,
failed_attempts INTEGER DEFAULT 0,
account_locked INTEGER DEFAULT 0,
last_login TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS image_history(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
image_path TEXT,
effect TEXT,
created_at TEXT
)
""")

conn.commit()

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "landing"

if "user" not in st.session_state:
    st.session_state.user = ""

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

# ================= STYLE =================
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{
    background: linear-gradient(-45deg,#0f2027,#203a43,#2c5364,#1b1b1b);
    background-size:400% 400%;
    animation: gradientBG 12s ease infinite;
}
@keyframes gradientBG{
    0%{background-position:0% 50%;}
    50%{background-position:100% 50%;}
    100%{background-position:0% 50%;}
}
.block-container{
    padding-top:2rem !important;
}
.box{
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
    padding:20px;
    border-radius:15px;
    text-align:center;
    font-weight:bold;
    color:white;
    border:1px solid rgba(255,255,255,0.3);
}
.box:hover{
    transform:scale(1.05);
}
.card{
    background:white;
    padding:40px;
    border-radius:20px;
    width:420px;
    margin:auto;
    box-shadow:0px 10px 30px rgba(0,0,0,0.3);
}
.stButton>button{
    background:#00b4d8;
    color:white;
    border-radius:10px;
    padding:8px 16px;
    border:none;
}
.stButton>button:hover{
    background:#0077b6;
}
input{
    border-radius:10px !important;
            }


            
/* ✅ REMOVE TOP SPACE COMPLETELY */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}

/* ✅ REMOVE HEADER SPACE */
header {
    visibility: hidden;
}

/* ✅ FULL WIDTH */
.main {
    padding: 0rem !important;
}

/* ✅ REMOVE SIDEBAR EXTRA GAP */
[data-testid="stSidebar"] {
    padding-top: 0rem !important;

}


/* ✅ Remove Top Padding Only */
.block-container {
    padding-top: 0px !important;
}

/* ✅ Hide Default Header Text */
header {
    visibility: hidden;
}

/* ✅ Full Width */
.main {
    padding: 0px !important;
}

</style>

""",unsafe_allow_html=True)

# =====================================================
# ================= LANDING PAGE ======================
# =====================================================

if not st.session_state.logged_in and st.session_state.page == "landing":

    st.title("🎨 AI Cartoon Studio")
    st.subheader("Modern Image Processing Platform 🚀")

    col1,col2,col3,col4 = st.columns(4)

    features = ["🔥 Cartoon","🧠 Edge","🎨 Sketch","🔐 Secure"]

    for i,col in enumerate([col1,col2,col3,col4]):
        with col:
            st.markdown(f"<div class='box'>{features[i]}</div>",
                        unsafe_allow_html=True)

    st.markdown("<br><br><br>",unsafe_allow_html=True)

    colA,colB = st.columns(2)

    with colA:
        if st.button("🔐 Login", use_container_width=True):
            st.session_state.page = "login"
            st.rerun()

    with colB:
        if st.button("📝 Register", use_container_width=True):
            st.session_state.page = "register"
            st.rerun()

# =====================================================
# ================= LOGIN PAGE ========================
# ====================================================

elif st.session_state.page == "login":

    #st.markdown("<div class='card'>", unsafe_allow_html=True)

    # 🔥 Header Inside Card
    st.markdown("""
    <div style="text-align:center;
                font-size:22px;
                font-weight:bold;
                color:#00b4d8;
                margin-bottom:20px;">
    🔐 Login
    <br>
    <span style="font-size:14px;color:gray;">
    Welcome Back 🚀
    </span>
    </div>
    """, unsafe_allow_html=True)

    email = st.text_input("Email or Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login Now"):

        cursor.execute("""
        SELECT * FROM users
        WHERE email=? OR username=?
        """,(email,email))

        user = cursor.fetchone()

        if not user:
            st.error("User Not Found")

        elif user[5] == 1:
            st.error("Account Locked 🔒")

        elif user[3] == hash_password(password):

            st.session_state.logged_in = True
            st.session_state.user = user[1]
            st.session_state.page = "dashboard"
            st.rerun()

        else:
            failed = user[4] + 1
            lock = 1 if failed >= 5 else 0

            cursor.execute("""
            UPDATE users
            SET failed_attempts=?,account_locked=?
            WHERE id=?
            """,(failed,lock,user[0]))

            conn.commit()
            st.error(f"Wrong Password ❌ Attempts: {failed}/5")

    # 🔥 Forgot Password
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("❓ Forgot Password"):
        st.info("Reset Feature Coming Soon 🚀")

    st.markdown("<br>", unsafe_allow_html=True)

    # 🔥 Register Redirect (Inside Card)
    st.write("Don't have an account?")

    if st.button("📝 Go To Register"):
        st.session_state.page = "register"
        st.rerun()

    # 🔥 Back Button
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("⬅ Back"):
        st.session_state.page = "landing"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# ================= REGISTER PAGE =====================
# =====================================================



elif st.session_state.page == "register":
    
    #st.markdown("<div class='card'>",unsafe_allow_html=True)
    st.title("📝 Register")

    username = st.text_input("Username", key="reg_user")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_pass")
    confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")

    remember = st.checkbox("🔔 Remember Me")
    terms = st.checkbox("✔ I Agree To Terms")

    
    
    if st.button("Create Account", key="register_btn"):

       if not username or not email or not password or not confirm_password:
        st.error("All fields are required ❗")

       elif len(password) < 8:
        st.error("Password must be at least 8 characters long 🔐")

       elif not any(char.isupper() for char in password):
        st.error("Password must contain at least 1 uppercase letter 🔠")

       elif not any(char.islower() for char in password):
        st.error("Password must contain at least 1 lowercase letter 🔡")

       elif not any(char.isdigit() for char in password):
        st.error("Password must contain at least 1 number 🔢")

       elif password != confirm_password:
        st.error("Passwords Do Not Match ❌")

       elif not terms:
        st.error("Accept Terms First ❗")

       else:
        try:
            cursor.execute("""
            INSERT INTO users(username,email,password,failed_attempts,account_locked)
            VALUES(?,?,?,?,?)
            """,(username,email,hash_password(password),0,0))

            conn.commit()

            st.success("Account Created 🎉")
            st.session_state.page = "login"
            st.rerun()

        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("<br>", unsafe_allow_html=True)

    st.write("Already have an account?")

    if st.button("🔐 Go To Login"):
      st.session_state.page = "login"
      st.rerun()

    if st.button("⬅ Back"):
        st.session_state.page = "landing"
        st.rerun()

    st.markdown("</div>",unsafe_allow_html=True)

# =====================================================
# ================= DASHBOARD =========================
# =====================================================

elif st.session_state.logged_in:

    st.sidebar.title("📌 Navigation")

    page = st.sidebar.radio(
        "Menu",
        ["Image Process","Gallery","Profile","Logout"]
    )

    st.title(f"Welcome {st.session_state.user} 👋")

    # ---------- LOGOUT ----------
    if page == "Logout":
        st.session_state.logged_in = False
        st.session_state.page = "landing"
        st.rerun()

    # ---------- PROFILE ----------
    elif page == "Profile":

        cursor.execute("""
        SELECT username,email,last_login
        FROM users
        WHERE username=?
        """,(st.session_state.user,))

        data = cursor.fetchone()

        if data:
            st.write("Username:",data[0])
            st.write("Email:",data[1])
            st.write("Last Login:",data[2])

    # ---------- IMAGE PROCESS ----------
    
    elif page == "Image Process":

     uploaded = st.file_uploader(
        "📤 Upload Image (Max 10MB)",
        type=["jpg","png","jpeg"]
    )

     if uploaded:

        if uploaded.size > 10*1024*1024:
            st.error("❌ File Too Large (Max 10MB)")
            st.stop()

        image = Image.open(uploaded).convert("RGB")
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        st.success("✅ Image Uploaded Successfully")
        st.write("📦 Size:", round(uploaded.size/1024/1024,2), "MB")

        # ================= STYLE SELECTION =================

        st.markdown("## 🎨 Choose Style")

        style = st.radio(
            "Select Effect",
            [
                "Classic Cartoon",
                "Sketch Advanced",
                "Pencil Color",
                "Black & White",
                "Oil Painting",
                "Edge Only"
            ],
            help="Select style and click Process Image"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original")
            st.image(image, use_container_width=True)

        process = st.button("🚀 Process Image")

        processed = image

        if process:

            with st.spinner("⏳ Processing Image..."):

                # -------- EFFECT LOGIC --------

                if style == "Classic Cartoon":
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray,100,200)
                    color = cv2.bilateralFilter(img,9,300,300)
                    cartoon = cv2.bitwise_and(color,color,mask=edges)
                    processed = Image.fromarray(cartoon)

                elif style == "Sketch Advanced":
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    inverted = 255 - gray
                    blur = cv2.GaussianBlur(inverted,(21,21),0)
                    sketch = cv2.divide(gray,255-blur,scale=256)
                    sketch = cv2.convertScaleAbs(sketch,alpha=1.5,beta=0)
                    processed = Image.fromarray(sketch)

                elif style == "Pencil Color":
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    inverted = 255 - gray
                    blur = cv2.GaussianBlur(inverted,(21,21),0)
                    sketch = cv2.divide(gray,255-blur,scale=256)
                    sketch = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

                    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                    hsv[:,:,1] = hsv[:,:,1] * 0.5
                    reduced = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

                    final = cv2.bitwise_and(reduced, sketch)
                    processed = Image.fromarray(
                        cv2.cvtColor(final, cv2.COLOR_BGR2RGB)
                    )

                elif style == "Black & White":
                    bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    processed = Image.fromarray(bw)

                elif style == "Oil Painting":
                    try:
                        oil = cv2.xphoto.oilPainting(img,7,1)
                        processed = Image.fromarray(
                            cv2.cvtColor(oil, cv2.COLOR_BGR2RGB)
                        )
                    except:
                        st.error("Install opencv-contrib-python for Oil Effect")

                elif style == "Edge Only":
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray,100,200)
                    processed = Image.fromarray(edges)

            # -------- DISPLAY AFTER PROCESS --------

            with col2:
                st.subheader("Processed")
                st.image(processed, use_container_width=True)

            # -------- DOWNLOAD PROCESS --------

            buffer = BytesIO()
            processed.save(buffer, format="PNG")

            st.download_button(
                "⬇ Download Processed Image",
                buffer.getvalue(),
                "processed.png",
                "image/png"
            )

            # -------- SIDE BY SIDE DOWNLOAD --------

            combined = Image.new(
                "RGB",
                (image.width + processed.width, image.height)
            )

            combined.paste(image,(0,0))
            combined.paste(processed,(image.width,0))

            combo_buffer = BytesIO()
            combined.save(combo_buffer, format="PNG")

            st.download_button(
                "📥 Download Before/After Comparison",
                combo_buffer.getvalue(),
                "comparison.png",
                "image/png"
            )

        st.button("🔄 Try Another Style", key="reset_btn")
     
     # ================= TASK 13 : IMAGE COMPARISON MODULE =================

if 'processed' in locals():

    st.markdown("---")
    st.subheader("🔍 Image Comparison Module")

    # ================= SIDE BY SIDE VIEW =================

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🟢 Original")
        st.image(image, use_container_width=True)

        st.write("📏 Dimensions:", image.size)
        st.write("📦 File Size:", round(uploaded.size/1024/1024,2), "MB")

    with col2:
        st.markdown("### 🔵 Processed")
        st.image(processed, use_container_width=True)

        # Processing time
        start_time = datetime.now()
        processing_time = datetime.now() - start_time
        st.write("⏱ Processing Time:", processing_time)

    # ================= SLIDER EFFECT =================

    st.markdown("## 🎚 Before / After Slider")

    slider = st.slider("Slide to Compare", 0, 100, 50)

    if slider:

        width = image.width
        height = image.height

        before = image.resize((width, height))
        after = processed.resize((width, height))

        split = int(width * (slider / 100))

        blended = Image.new("RGB", (width, height))
        blended.paste(before.crop((0,0,split,height)), (0,0))
        blended.paste(after.crop((split,0,width,height)), (split,0))

        st.image(blended, use_container_width=True)

    # ================= DOWNLOAD COMPARISON =================

    combined = Image.new(
        "RGB",
        (image.width + processed.width, image.height)
    )

    combined.paste(image, (0,0))
    combined.paste(processed, (image.width,0))

    buffer = BytesIO()
    combined.save(buffer, format="PNG")

    st.download_button(
        "📥 Download Side-by-Side Comparison",
        buffer.getvalue(),
        "comparison.png",
        "image/png"
    )

    # ================= IMAGE STATISTICS =================

    st.markdown("## 📊 Image Statistics")

    def image_stats(img):
        gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
        brightness = np.mean(gray)
        contrast = np.std(gray)
        return brightness, contrast

    b1, c1 = image_stats(image)
    b2, c2 = image_stats(processed)

    col3, col4 = st.columns(2)

    with col3:
        st.write("🔹 Original Brightness:", round(b1,2))
        st.write("🔹 Original Contrast:", round(c1,2))

    with col4:
        st.write("🔹 Processed Brightness:", round(b2,2))
        st.write("🔹 Processed Contrast:", round(c2,2))



    # ---------- GALLERY ----------  
elif 'page' in locals() and page == "Gallery":

        st.subheader("🖼 History")

        cursor.execute("""
        SELECT image_path,effect,created_at
        FROM image_history
        WHERE username=?
        ORDER BY id DESC
        """,(st.session_state.user,))

        rows = cursor.fetchall()

        for row in rows:
            st.write("Effect:",row[1])
            st.write("Created:",row[2])
            try:
                img = Image.open(row[0])
                st.image(img,width=250)
            except:
                pass
            st.divider()