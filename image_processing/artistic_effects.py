import cv2
import numpy as np

# ---------- Sketch Effect ----------
def sketch_effect(image, ksize=21, contrast=1.2):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (ksize, ksize), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256)
    sketch = cv2.convertScaleAbs(sketch, alpha=contrast, beta=0)
    sketch_rgb = cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)
    return sketch_rgb

# ---------- Pencil Color Effect ----------
def pencil_color_effect(image, ksize=21, contrast=1.2, saturation=0.5):
    sketch = sketch_effect(image, ksize, contrast)
    # Reduce saturation
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV).astype(np.float32)
    hsv[...,1] = hsv[...,1]*saturation
    colored = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
    pencil_color = cv2.bitwise_and(colored, sketch)
    return pencil_color