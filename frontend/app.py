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
import sys
from download_module import prepare_download
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..")))
from db import store_image_history
from download_module import cleanup_old_files
from image_processing.color_cartoon import cartoon_base
from edge_detection import cartoon_edges

# ================= PAGE CONFIG =================
st.set_page_config(page_title="AI Cartoon Studio", layout="wide")
st.markdown("""
<style>
[data-testid="stAppViewContainer"]{
    background-color:#0f172a;
}
</style>
""", unsafe_allow_html=True)
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
if "user_id" not in st.session_state:
   st.session_state.user_id=None
def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

# ================= STYLE =================

st.markdown("""
<style>

/* ===== APP BACKGROUND ===== */
[data-testid="stAppViewContainer"]{
    background: linear-gradient(135deg,#0f172a,#1e293b);
}

/* ===== REMOVE DEFAULT HEADER ===== */
header {visibility:hidden;}

/* ===== MAIN CONTAINER WIDTH CONTROL ===== */
.block-container{
    max-width:1100px;
    margin:auto;
    padding-top:3rem;
    padding-bottom:3rem;
}

/* ===== FEATURE GRID ===== */
.features-grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
    gap:25px;
    margin-top:40px;
}

/* ===== FEATURE CARD ===== */
.feature-card{
    background:#1e293b;
    border:1px solid #334155;
    border-radius:18px;
    padding:30px;
    text-align:center;
    color:#f1f5f9;
    font-size:16px;
    font-weight:500;
    transition:all 0.3s ease;
}

.feature-card:hover{
    transform:translateY(-6px);
    border-color:#6366f1;
    box-shadow:0 10px 25px rgba(99,102,241,0.4);
}


/* ===== BUTTON STYLE ===== */
.stButton>button{
    border-radius:12px;
    height:48px;
    font-weight:600;
    background:#6366f1;
    color:white;
    border:none;
}

.stButton>button:hover{
    background:#4f46e5;
}

/* ===== INPUT STYLE ===== */
input{
    border-radius:10px !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# ================= LANDING PAGE ======================
# =====================================================
if not st.session_state.logged_in and st.session_state.page == "landing":
    st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
}

.hero-title {
    font-size: 55px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg,#00f5ff,#00c6ff);
    -webkit-background-clip: text;
    color: transparent;
}

.hero-sub {
    text-align: center;
    font-size: 18px;
    opacity: 0.8;
    margin-bottom: 50px;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 25px;
    margin-top: 40px;
}

.feature-card {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(12px);
    padding: 30px 20px;
    border-radius: 18px;
    text-align: center;
    transition: 0.3s;
}

.feature-card:hover {
    transform: translateY(-6px);
    background: rgba(255,255,255,0.12);
}
</style>
""", unsafe_allow_html=True)


    

    # ===== HERO SECTION =====
    st.markdown("""
<div class="hero-title">🎨 AI Cartoon Studio</div>
<div class="hero-sub">
Transform your images into stunning AI art styles.<br>
Fast • Secure • Professional
</div>
""", unsafe_allow_html=True)


    


    # ===== FEATURES SECTION =====

if not st.session_state.logged_in and st.session_state.page == "landing":

    st.markdown("## 🚀 Why Choose Us")

    features = [
    "🔥 Classic Cartoon",
    "✏ Sketch Effect",
    "🖌 Pencil Color",
    "⚡ Fast Processing",
    "📂 Image History",
    "🔐 Secure Authentication"

]

    feature_html = "<div class='features-grid'>"

    for f in features:
     feature_html += f"<div class='feature-card'>{f}</div>"

    feature_html += "</div>"

    st.markdown(feature_html, unsafe_allow_html=True)

        
            

    # ===== CTA BUTTONS =====
    st.markdown("<div style='height:50px;'></div>",unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
       if st.button("🚀 Login", use_container_width=True):
        st.session_state.page = "login"
        st.rerun()

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
        type=["jpg", "png", "jpeg"]
    )

    if "uploaded" in locals() and uploaded is not None:

        if uploaded.size > 10 * 1024 * 1024:
            st.error("❌ File Too Large (Max 10MB)")
            st.stop()

        image = Image.open(uploaded).convert("RGB")
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        st.success("✅ Image Uploaded Successfully")
        st.write("📦 Size:", round(uploaded.size / 1024 / 1024, 2), "MB")

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
            ]
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original")
            st.image(image, use_container_width=True)

        if st.button("🚀 Process Image"):

            with st.spinner("🤖 AI is processing..."):

                if style == "Classic Cartoon":
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray, 100, 200)
                    color = cv2.bilateralFilter(img, 9, 300, 300)
                    cartoon = cv2.bitwise_and(color, color, mask=edges)
                    processed = Image.fromarray(
                        cv2.cvtColor(cartoon, cv2.COLOR_BGR2RGB)
                    )

                elif style == "Sketch Advanced":
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    inverted = 255 - gray
                    blur = cv2.GaussianBlur(inverted, (21, 21), 0)
                    sketch = cv2.divide(gray, 255 - blur, scale=256)
                    processed = Image.fromarray(sketch)

                elif style == "Pencil Color":
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    inverted = 255 - gray
                    blur = cv2.GaussianBlur(inverted, (21, 21), 0)
                    sketch = cv2.divide(gray, 255 - blur, scale=256)
                    sketch = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

                    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                    hsv[:, :, 1] = hsv[:, :, 1] * 0.5
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
                        oil = cv2.xphoto.oilPainting(img, 7, 1)
                        processed = Image.fromarray(
                            cv2.cvtColor(oil, cv2.COLOR_BGR2RGB)
                        )
                    except:
                        st.error("Install opencv-contrib-python")
                        st.stop()

                elif style == "Edge Only":
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray, 100, 200)
                    processed = Image.fromarray(edges)

            # Save processed image in session
            st.session_state.processed = processed
            st.session_state.style = style

        # ---------------- DISPLAY AFTER PROCESS ----------------
        if "processed" in st.session_state:

            with col2:
                st.subheader("Processed")
                st.image(st.session_state.processed, use_container_width=True)

            # ---------------- PREPARE DOWNLOAD ----------------
            if st.button("📥 Prepare Download"):

                file_path = prepare_download(
                    user_id=st.session_state.user_id,
                    original_filename=uploaded.name,
                    image=st.session_state.processed,
                    style_name=st.session_state.style,
                    format="PNG",
                    quality="high",
                    is_paid=False
                )

                if file_path:
                    st.session_state.download_file = file_path

                    store_image_history(
                        st.session_state.user_id,
                        uploaded.name,
                        st.session_state.style
                    )

                    st.success("Download Ready ✅")

        # ---------------- ACTUAL DOWNLOAD ----------------
        if "download_file" in st.session_state:

            with open(st.session_state.download_file, "rb") as f:
                st.download_button(
                    "⬇ Download Image",
                    f,
                    file_name=os.path.basename(st.session_state.download_file),
                    mime="image/png"
                )

        # ---------------- BEFORE/AFTER ----------------
        if "processed" in st.session_state:

            combined = Image.new(
                "RGB",
                (image.width + st.session_state.processed.width, image.height)
            )

            combined.paste(image, (0, 0))
            combined.paste(st.session_state.processed, (image.width, 0))

            buffer = BytesIO()
            combined.save(buffer, format="PNG")

            st.download_button(
                "📥 Download Before/After",
                buffer.getvalue(),
                "comparison.png",
                "image/png"
            )

        
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

     img_array = np.array(img)
 
    # Agar image already grayscale hai
     if len(img_array.shape) == 2:
        gray = img_array
     else:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

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