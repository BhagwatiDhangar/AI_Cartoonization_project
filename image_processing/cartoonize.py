import cv2
import numpy as np
import os

# Load image
img = cv2.imread("images/test.jpg")
img = cv2.resize(img, (600, 600))

# Create output folder
os.makedirs("outputs", exist_ok=True)

# ---------- CARTOON EFFECT ----------
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_blur = cv2.medianBlur(gray, 5)

edges = cv2.adaptiveThreshold(
    gray_blur,
    255,
    cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY,
    9,
    9
)

color = cv2.bilateralFilter(img, 9, 300, 300)
cartoon = cv2.bitwise_and(color, color, mask=edges)

cv2.imwrite("outputs/cartoon.jpg", cartoon)

# ---------- SKETCH EFFECT ----------
sketch_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
sketch = cv2.adaptiveThreshold(
    sketch_gray,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11,
    2
)

cv2.imwrite("outputs/sketch.jpg", sketch)

# ---------- PENCIL COLOR EFFECT ----------
pencil_color = cv2.pencilSketch(
    img, sigma_s=60, sigma_r=0.07, shade_factor=0.05
)[1]

cv2.imwrite("outputs/pencil_color.jpg", pencil_color)

print("✅ Images processed successfully!")
print("➡️ Check outputs folder:")
print(" - outputs/cartoon.jpg")
print(" - outputs/sketch.jpg")
print(" - outputs/pencil_color.jpg")