import cv2
import numpy as np

def final_cartoon(image, edge_thickness=7, smooth_strength=9, colors=8):

    # ---------- EDGE DETECTION ----------
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray = cv2.medianBlur(gray, 7)

    edges = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        edge_thickness * 2 + 1,
        2
    )

    # ---------- COLOR SMOOTHING ----------
    color = cv2.bilateralFilter(image, smooth_strength, 300, 300)

    # ---------- COLOR QUANTIZATION ----------
    data = np.float32(color).reshape((-1, 3))
    _, label, center = cv2.kmeans(
        data, colors, None,
        (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001),
        10, cv2.KMEANS_RANDOM_CENTERS
    )

    center = np.uint8(center)
    quantized = center[label.flatten()]
    quantized = quantized.reshape(color.shape)

    # ---------- MERGE EDGE + COLOR ----------
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
    cartoon = cv2.bitwise_and(quantized, edges)

    return cartoon