import cv2
import numpy as np

def classic_cartoon(image, intensity="medium"):
    # ---------- Resize for speed ----------
    h, w = image.shape[:2]
    if max(h, w) > 800:
        scale = 800 / max(h, w)
        image = cv2.resize(image, (int(w*scale), int(h*scale)))

    # ---------- Intensity settings ----------
    if intensity == "light":
        smooth_val = 7
        color_k = 12
        edge_block = 9
    elif intensity == "strong":
        smooth_val = 13
        color_k = 6
        edge_block = 15
    else:  # medium
        smooth_val = 9
        color_k = 8
        edge_block = 11

    # ---------- Noise reduction ----------
    image = cv2.medianBlur(image, 5)

    # ---------- Bilateral Filtering ----------
    smooth = cv2.bilateralFilter(image, smooth_val, 300, 300)

    # ---------- Color Quantization ----------
    data = np.float32(smooth).reshape((-1, 3))
    _, label, center = cv2.kmeans(
        data, color_k, None,
        (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001),
        10, cv2.KMEANS_RANDOM_CENTERS
    )
    center = np.uint8(center)
    quantized = center[label.flatten()]
    quantized = quantized.reshape(smooth.shape)

    # ---------- Edge Detection ----------
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    edges = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        edge_block, 2
    )
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)

    # ---------- Combine ----------
    cartoon = cv2.bitwise_and(quantized, edges)

    return cartoon