import cv2
import numpy as np

# ---------- Bilateral Filter ----------
def smooth_image(image, strength=9):
    smooth = cv2.bilateralFilter(image, strength, 300, 300)
    return smooth


# ---------- Color Quantization ----------
def reduce_colors(image, k=8):
    data = np.float32(image).reshape((-1, 3))

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, label, center = cv2.kmeans(
        data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )

    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(image.shape)

    return result


# ---------- Combine both ----------
def cartoon_base(image, smooth_strength=9, colors=8):
    smooth = smooth_image(image, smooth_strength)
    cartoon = reduce_colors(smooth, colors)
    return cartoon