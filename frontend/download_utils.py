import os
import uuid
import time
from datetime import datetime, timedelta
from PIL import ImageDraw, ImageFont,Image

OUTPUT_FOLDER = "output"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)


# -----------------------------
# Generate Unique Filename
# -----------------------------
def generate_filename(user_id, original_name, format_option):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name_without_ext = os.path.splitext(original_name)[0]
    unique_name = f"{user_id}_{timestamp}_{name_without_ext}.{format_option.lower()}"
    return unique_name


# -----------------------------
# Add Watermark (Free Preview)
# -----------------------------
from PIL import Image, ImageDraw, ImageFont

def add_watermark(image):

    image = image.convert("RGBA")
    watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark_layer)

    watermark_text = "AI Cartoonizer - Preview"

    width, height = image.size

    font_size = int(width / 15)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # ✅ Pillow new method
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = width - text_width - 20
    y = height - text_height - 20

    draw.text(
        (x, y),
        watermark_text,
        font=font,
        fill=(255, 255, 255, 120)
    )

    combined = Image.alpha_composite(image, watermark_layer)

    return combined.convert("RGB")
# -----------------------------
# Save Image in Different Formats
# -----------------------------
def save_image(image, path, format_option, quality_option):
    try:
        if format_option == "PNG":
            image.save(path, format="PNG")

        elif format_option == "JPG":
            if quality_option == "Optimized":
                image.save(path, format="JPEG", quality=60)
            else:
                image.save(path, format="JPEG", quality=95)

        elif format_option == "PDF":
            image.save(path, format="PDF")

        return True

    except Exception as e:
        print("Error saving image:", e)
        return False


# -----------------------------
# Prepare Download Function
# -----------------------------
def prepare_download(image, user_id, original_name,
                     style, format_option,
                     quality_option, is_paid,
                     cursor, conn):
    if not is_paid:
        image=add_watermark(image)
    try:
        filename = generate_filename(user_id, original_name, format_option)
        path = os.path.join(OUTPUT_FOLDER, filename)

        # Add watermark only if NOT paid
        if not is_paid:
            image_to_save = add_watermark(image)
            payment_status = "free_preview"
        else:
            image_to_save = image
            payment_status = "paid"

        success = save_image(image_to_save, path, format_option, quality_option)

        if not success:
            return None

        # Store metadata in DB
        cursor.execute("""
            INSERT INTO ImageHistory
            (user_id, image_path, style, download_timestamp, payment_status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            path,
            style,
            datetime.now(),
            payment_status
        ))
        conn.commit()

        return path

    except Exception as e:
        print("Download preparation failed:", e)
        return None


# -----------------------------
# Cleanup Old Files (24 hours)
# -----------------------------
def cleanup_old_files():
    now = time.time()
    for filename in os.listdir(OUTPUT_FOLDER):
        path = os.path.join(OUTPUT_FOLDER, filename)
        if os.stat(path).st_mtime < now - 86400:
            os.remove(path)

from PIL import ImageDraw, ImageFont
