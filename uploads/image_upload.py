import streamlit as st
from PIL import Image
import os
import uuid

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="Image Upload | AI Cartoonization",
    page_icon="🖼️",
    layout="centered"
)

st.title("🖼️ Image Upload & Preview")
st.write("Upload an image (JPG, JPEG, PNG, BMP). Max size: 10MB")

# ---------------- Session State ----------------
if "image_path" not in st.session_state:
    st.session_state.image_path = None

# ---------------- Constants ----------------
UPLOAD_FOLDER = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_TYPES = ["jpg", "jpeg", "png", "bmp"]

# Create uploads folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- File Uploader ----------------
uploaded_file = st.file_uploader(
    "Choose an image",
    type=ALLOWED_TYPES
)

# ---------------- Validation & Processing ----------------
if uploaded_file is not None:

    # File size validation
    if uploaded_file.size > MAX_FILE_SIZE:
        st.error("❌ File size exceeds 10MB limit")

    else:
        try:
            # Open image (checks corruption too)
            image = Image.open(uploaded_file)
            image.verify()

            # Reopen after verify
            image = Image.open(uploaded_file)

            # Generate unique filename
            file_extension = uploaded_file.name.split(".")[-1]
            unique_name = f"{uuid.uuid4()}.{file_extension}"
            file_path = os.path.join(UPLOAD_FOLDER, unique_name)

            # Save image
            image.save(file_path)

            # Save path in session
            st.session_state.image_path = file_path

            # ---------------- Display Image ----------------
            st.subheader("📸 Uploaded Image Preview")
            st.image(image, use_container_width=True)

            # ---------------- Metadata ----------------
            width, height = image.size
            file_size_kb = round(uploaded_file.size / 1024, 2)

            st.subheader("🧾 Image Metadata")
            st.write(f"**Format:** {image.format}")
            st.write(f"**Dimensions:** {width} x {height}")
            st.write(f"**File Size:** {file_size_kb} KB")
            st.write(f"**Saved Path:** {file_path}")

            st.success("✅ Image uploaded successfully")

        except Exception:
            st.error("❌ Invalid or corrupted image file")

# ---------------- Replace Image ----------------
if st.session_state.image_path:
    if st.button("🔄 Upload New Image"):
        st.session_state.image_path = None
        st.rerun()