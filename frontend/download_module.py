import os
import cv2
import time
from datetime import datetime
from PIL import Image


# ---------------------------
# STEP 4: Unique Filename
# ---------------------------
def generate_filename(user_id, original_filename):
    name, ext = os.path.splitext(original_filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{user_id}_{timestamp}_{name}"


# ---------------------------
# STEP 5: Watermark Function
# ---------------------------
import numpy as np
import cv2

def add_watermark(image):

    # Agar PIL image hai to numpy me convert karo
    if not isinstance(image, np.ndarray):
        image = np.array(image)

    h, w = image.shape[:2]

    watermark_text = "AI Cartoon"
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = w / 600
    thickness = 2

    text_size = cv2.getTextSize(watermark_text, font, font_scale, thickness)[0]
    text_x = w - text_size[0] - 10
    text_y = h - 10

    cv2.putText(
        image,
        watermark_text,
        (text_x, text_y),
        font,
        font_scale,
        (255, 255, 255),
        thickness,
        cv2.LINE_AA
    )

    return image


# ---------------------------
# STEP 6: Save Image (Multi Format + Quality)
# ---------------------------
def save_image(image, path, format="PNG", quality="high"):
    try:
        if format == "PNG":
            cv2.imwrite(path + ".png", image)

        elif format == "JPG":
            jpeg_quality = 95 if quality == "high" else 70
            cv2.imwrite(
                path + ".jpg",
                image,
                [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality]
            )

        elif format == "PDF":
            pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            pil_img.save(path + ".pdf")

        return True

    except Exception as e:
        print("Error saving image:", e)
        return False


# ---------------------------
# Main Download Preparation
# ---------------------------
def prepare_download(
    user_id,
    original_filename,
    image,
    style_name,
    format="PNG",
    quality="high",
    is_paid=False
):

    os.makedirs("temp_downloads", exist_ok=True)

    filename = generate_filename(user_id, original_filename)
    full_path = os.path.join("temp_downloads", filename)

    # Watermark only for free users
    if not is_paid:
        image = add_watermark(image)

    success = save_image(image, full_path, format, quality)

    if not success:
        return None

    return full_path + "." + format.lower()


# ---------------------------
# Cleanup Old Files (24 hrs)
# ---------------------------
def cleanup_old_files(folder="temp_downloads"):
    now = time.time()

    if not os.path.exists(folder):
        return

    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)

        if os.path.isfile(file_path):
            if now - os.path.getmtime(file_path) > 86400:
                os.remove(file_path)