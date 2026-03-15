import streamlit as st
import sqlite3
import hashlib
import cv2
import time
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
from db import store_image_history,create_connection
from download_module import cleanup_old_files
from image_processing.color_cartoon import cartoon_base
from edge_detection import cartoon_edges
from ui import load_advanced_ui
load_advanced_ui()
from download_utils import prepare_download,cleanup_old_files,add_watermark
from payment_utils import create_payment_order,update_transaction_status

from db import create_tables
create_tables()
import secrets
from io import BytesIO
from datetime import datetime,timedelta
from db import create_tables
create_tables()
import os
os.makedirs("uploads",exist_ok=True)
os.makedirs("downloads",exist_ok=True)
if "payment_success" not in st.session_state:
    st.session_state.payment_success = False

if "processed" not in st.session_state:
    st.session_state.processed = None

if "original" not in st.session_state:
    st.session_state.original = None
import sqlite3
def verify_payment(user_id, order_id):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT status FROM transactions
    WHERE user_id=? AND order_id=?
    """,(user_id,order_id))

    result = cursor.fetchone()
    conn.close()

    if result and result[0] == "Success":
        return True
    return False
import time

def check_rate_limit():

    now = time.time()

    if "last_download" not in st.session_state:
        st.session_state.last_download = 0

    if now - st.session_state.last_download < 5:
        st.warning("Too many downloads. Please wait")
        return False

    st.session_state.last_download = now

    return True
conn = sqlite3.connect("cartoon_app.db", check_same_thread=False)
cursor = conn.cursor()

# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users(
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
email TEXT UNIQUE,
password TEXT,
created_at TEXT,
last_login TEXT
)
""")

# IMAGE HISTORY
cursor.execute("""
CREATE TABLE IF NOT EXISTS image_history(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
image_path TEXT,
effect TEXT,
created_at TEXT
)
""")

# TRANSACTIONS
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
order_id TEXT,
payment_id TEXT,
amount INTEGER,
status TEXT,
created_at TEXT
)
""")

# DOWNLOAD HISTORY
cursor.execute("""
CREATE TABLE IF NOT EXISTS downloads(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
image_path TEXT,
download_time TEXT
)
""")

conn.commit()
# ================= SESSION STATE INITIALIZATION =================
def verify_payment(user_id, order_id):

    cursor.execute("""
    SELECT status FROM transactions
    WHERE user_id=? AND order_id=?
    """,(user_id,order_id))

    result = cursor.fetchone()

    if result and result[0] == "success":
        return True

    return False
def generate_download_token():

    token = secrets.token_hex(16)
    expiry = datetime.now() + timedelta(hours=1)

    return token, expiry
def init_session():

    defaults = {
        "order_id": None,
        "payment_pending": False,
        "is_paid": False,
        "download_file": None,
        "processed": None,
        "original": None
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session()
if "order_id" not in st.session_state:
    st.session_state.order_id = None

if "payment_pending" not in st.session_state:
    st.session_state.payment_pending = False

if "is_paid" not in st.session_state:
    st.session_state.is_paid = False

if "download_file" not in st.session_state:
    st.session_state.download_file = None

# ================= PAGE CONFIG =================
st.set_page_config(page_title="AI Cartoon Studio", layout="wide")
st.set_page_config(layout="wide", initial_sidebar_state="expanded")
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
from db import create_connection
conn = sqlite3.connect("cartoon_app.db", check_same_thread=False)
cursor = conn.cursor()


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
        SELECT * FROM Users
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
            st.session_state.user_id=user[0]
            st.session_state.page = "dashboard"
            st.rerun()

        else:
            failed = user[4] + 1
            lock = 1 if failed >= 5 else 0

            cursor.execute("""
            UPDATE Users
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
    remember = st.checkbox("🔔 Remember Me")
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

    
    terms = st.checkbox("✔ I Agree To Terms")

    
    
    if st.button("Create Account", key="register_btn"):

       if username.strip()=="" or email.strip()=="" or password.strip()=="" or confirm_password.strip()=="" :
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
            INSERT INTO Users(username,email,password,created_at)
            VALUES(?,?,?,?)
            """,(username,email,hash_password(password),datetime.now()))

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

# ================= DASHBOARD =================

elif st.session_state.logged_in:

    st.sidebar.title("📌 Navigation")

    page = st.sidebar.radio(
        "Menu",
        [
            "Image Process",
            "Gallery",
            "Payment History",
            "Profile",
            "Download History",
            "Logout"
        ]
    )

    st.title(f"Welcome {st.session_state.user} 👋")

# ================= LOGOUT =================

    if page == "Logout":

        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()


# ================= PROFILE =================

    elif page == "Profile":

        st.subheader("👤 User Profile")

        cursor.execute("""
        SELECT username,email,last_login
        FROM Users
        WHERE username=?
        """,(st.session_state.user,))

        data = cursor.fetchone()

        if data:
            st.write("Username:",data[0])
            st.write("Email:",data[1])
            st.write("Last Login:",data[2])

       # st.divider()

        # ===== ACCOUNT STATS =====

        st.subheader("📊 Account Statistics")

        cursor.execute("""
        SELECT COUNT(*) FROM image_history
        WHERE username=?
        """,(st.session_state.user,))

        total_images = cursor.fetchone()[0]

        cursor.execute("""
        SELECT SUM(amount) FROM transactions
        WHERE user_id=?
        """,(st.session_state.user_id,))

        spent = cursor.fetchone()[0]

        if spent is None:
            spent = 0

        st.write("Total Images Processed:",total_images)
        st.write("Total Amount Spent: ₹",spent)


# ================= DOWNLOAD HISTORY =================

    #elif page == "Download History":
    elif page == "Image Process":

        st.subheader("🎨 Cartoon Image Processor")
         
# ---------- SESSION STATE SAFE ----------

        if "original" not in st.session_state:
          st.session_state.original = None

        if "processed" not in st.session_state:
          st.session_state.processed = None


# ---------- IMAGE UPLOAD ----------

        uploaded = st.file_uploader(
         "📤 Upload Image",
         type=["jpg","png","jpeg"]
         )

        if uploaded is not None:

          st.session_state.original = Image.open(uploaded).convert("RGB")

          img = cv2.cvtColor(
            np.array(st.session_state.original),
            cv2.COLOR_RGB2BGR
               )

          st.success("Image Uploaded")

          style = st.radio(
            "Choose Style",
            [
                "Classic Cartoon","Sketch","Pencil Color",
                "Edge Only","Black & White",
                "Oil Painting","Watercolor","Vintage"
            ]
               )


# ---------- PROCESS IMAGE ----------

          if st.button("🚀 Process Image"):

             with st.spinner("Processing Image..."):

                gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                blur = cv2.medianBlur(gray,5)

                edges = cv2.adaptiveThreshold(
                    blur,255,
                    cv2.ADAPTIVE_THRESH_MEAN_C,
                    cv2.THRESH_BINARY,
                    9,9
                )

                color = cv2.bilateralFilter(img,9,250,250)

                cartoon = cv2.bitwise_and(color,color,mask=edges)

                st.session_state.processed = Image.fromarray(
                    cv2.cvtColor(cartoon,cv2.COLOR_BGR2RGB)
                )

                filename = f"uploads/{uuid.uuid4()}.png"
                st.session_state.processed.save(filename)

                cursor.execute("""
                INSERT INTO image_history
                (username,image_path,effect,created_at)
                VALUES (?,?,?,?)
                """,(
                    st.session_state.user,
                    filename,
                    style,
                    datetime.now()
                ))

                conn.commit()

                st.success("✅ Image Processed")


# ---------- TABS ----------

        tabs = st.tabs(["Original","Processed","Comparison","Payment"])


# ---------- ORIGINAL ----------

        with tabs[0]:

           st.subheader("Original Image")

           if st.session_state.original is not None:
            st.image(st.session_state.original,width=400)
           else:
             st.info("Upload image first")


# ---------- PROCESSED ----------

        with tabs[1]:

          st.subheader("Processed Image")

          if st.session_state.processed is not None:
            st.image(st.session_state.processed,width=400)
          else:
            st.info("Process image first")


# ---------- COMPARISON ----------

        with tabs[2]:

          st.subheader("Before & After Comparison")

          if st.session_state.original and st.session_state.processed:

            width = 400

            orig_resized = st.session_state.original.resize(
                (width,int(width*st.session_state.original.height/st.session_state.original.width))
            )

            proc_resized = st.session_state.processed.resize(
                (width,int(width*st.session_state.processed.height/st.session_state.processed.width))
            )

            slider = st.slider("Compare",0,100,50)

            blended = Image.new("RGB",(width,orig_resized.height))

            split = int(width*(slider/100))

            blended.paste(orig_resized.crop((0,0,split,orig_resized.height)),(0,0))
            blended.paste(proc_resized.crop((split,0,width,orig_resized.height)),(split,0))

            st.image(blended,width=400)

          else:
            st.info("Process image first")


# ---------- PAYMENT ----------

        #with tabs[3]:
        with tabs[3]:  # Payment tab
         st.markdown("## 💳 Payment Checkout")

         price = st.selectbox("Select Price", ["₹10 Basic Download", "₹50 HD Download"])
         format_selected = st.selectbox("Download Format", ["PNG", "JPG", "PDF"])

    # Simulate payment status
         payment_status = st.radio("Simulate Payment Status", ["Success", "Failed", "Cancelled"])

         if st.button("💳 Proceed to Payment"):

        # Check if image is processed
            if st.session_state.get("processed") is None:
              st.warning("⚠ Please process image first")
            else:
            # Success case
             if payment_status == "Success":
                 st.success("✅ Payment Successful")
                 payment_id = "pay_" + str(uuid.uuid4())[:8]
                 order_id = "order_" + str(uuid.uuid4())[:8]
                 st.write("Transaction ID:", payment_id)
                 st.session_state.payment_success = True
                 st.session_state.transaction_id = payment_id
                  
                # Save transaction to DB
                 amount = 10 if "10" in price else 50
                 cursor.execute("""
                    INSERT INTO transactions
                    (user_id, order_id, payment_id, amount, status, created_at)
                    VALUES (?,?,?,?,?,?)
                """, (
                    st.session_state.user_id,
                    order_id,
                    payment_id,
                    amount,
                    "Success",
                    datetime.now()
                ))
                 conn.commit()
                  # ================= DOWNLOAD AFTER PAYMENT =================
                 if st.session_state.get("payment_success") and st.session_state.get("processed"):
                    st.markdown("### ⬇ Download Your Image")

    # Ensure downloads folder exists
                    if not os.path.exists("downloads"):
                     os.makedirs("downloads")

    # Prepare filename based on selected format
                    ext = format_selected.lower()
                    image_path = f"downloads/{uuid.uuid4()}.{ext}"

                    try:
                      if ext == "png":
                        st.session_state.processed.save(image_path, "PNG")
                      elif ext == "jpg":
                       st.session_state.processed.save(image_path, "JPEG")
                      else:  # PDF
                       img_rgb = st.session_state.processed.convert("RGB")
                       img_rgb.save(image_path, "PDF")
                    except Exception as e:
                      st.error(f"⚠ Failed to save image: {e}")

    # Download button
                    with open(image_path, "rb") as file:
                       st.download_button(
                       label="⬇ Download Image",
                        data=file,
                        file_name=f"cartoon.{ext}",
                         mime=f"image/{ext}" if ext != "pdf" else "application/pdf"
                            )

    # Save to download history only once
                    if 'download_saved' not in st.session_state:
                      cursor.execute("""
                      INSERT INTO downloads
                        (user_id, image_path, download_time)
                       VALUES (?,?,?)
                        """, (
                           st.session_state.user_id,
                           image_path,
                             datetime.now()
        ))
                      conn.commit()
                      st.session_state.download_saved = True
                # Ensure downloads folder exists
                 if not os.path.exists("downloads"):
                   os.makedirs("downloads")

                # Save image in selected format
                   ext = format_selected.lower()
                   image_path = f"downloads/{uuid.uuid4()}.{ext}"

                   if format_selected == "PNG":
                     st.session_state.processed.save(image_path, "PNG")
                   elif format_selected == "JPG":
                     st.session_state.processed.save(image_path, "JPEG")
                   else:  # PDF
                     img_rgb = st.session_state.processed.convert("RGB")
                     img_rgb.save(image_path, "PDF")

                # Download button
                   with open(image_path, "rb") as file:
                     st.download_button(
                        "⬇ Download Image",
                        data=file,
                        file_name=f"cartoon.{ext}",
                        mime=f"image/{ext}" if ext != "pdf" else "application/pdf"
                    )

                # Save to download history
                   cursor.execute("""
                    INSERT INTO downloads
                    (user_id, image_path, download_time)
                     VALUES (?,?,?)
                  """, (
                    st.session_state.user_id,
                    image_path,
                    datetime.now()
                ))
                   conn.commit()

            # Failed payment
                 elif payment_status == "Failed":
                  st.error("❌ Payment Failed. Try Again.")

            # Cancelled payment
                 else:
                  st.warning("⚠ Payment Cancelled.")
                 

                
# ================= GALLERY =================

    elif page == "Gallery":

      st.subheader("🖼 Image Gallery")

      cursor.execute("""
    SELECT image_path,effect,created_at
    FROM image_history
    WHERE username=?
    ORDER BY created_at DESC
    """,(st.session_state.user,))

      rows = cursor.fetchall()

      if rows:

        cols = st.columns(3)

        for i,r in enumerate(rows):

            with cols[i%3]:

                try:
                    img = Image.open(r[0])
                    st.image(img,use_column_width=True)
                    st.caption(r[1])
                    st.caption(r[2])
                except:
                    st.warning("Image missing")

      else:
        st.info("No images yet")

     # ================= DOWNLOAD HISTORY =================

    #elif page == "Download History":
    elif page == "Download History":
      st.subheader("📥 Download History")

      cursor.execute("""
        SELECT id, image_path, download_time
        FROM downloads
        WHERE user_id=?
        ORDER BY download_time DESC
      """, (st.session_state.user_id,))

      rows = cursor.fetchall()
      if rows:
        for r in rows:
            st.write("Downloaded at:", r[2])
            try:
                img = Image.open(r[1])
                st.image(img, width=200)
            except:
                pass

            # ReDownload button
            with open(r[1], "rb") as file:
                st.download_button(
                    "🔄 ReDownload",
                    data=file,
                    file_name=os.path.basename(r[1]),
                    mime="image/png"
                )
            st.divider()
      else:
        st.info("No downloads yet.")
# ================= PAYMENT HISTORY =================

    elif page == "Payment History":

     st.subheader("💳 Payment History")

     cursor.execute("""
    SELECT order_id,payment_id,amount,status,created_at
    FROM transactions
    WHERE user_id=?
    ORDER BY id DESC
    """,(st.session_state.user_id,))

     rows = cursor.fetchall()

     if rows:

        for r in rows:

            st.write("Order ID:",r[0])
            st.write("Payment ID:",r[1])
            st.write("Amount:",r[2])
            st.write("Status:",r[3])
            st.write("Date:",r[4])

            st.divider()

     else:
        st.info("No payments yet")
        
