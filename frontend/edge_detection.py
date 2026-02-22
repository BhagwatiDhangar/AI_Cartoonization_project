import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


# =====================================================
# 1️⃣ Preprocessing (Noise Reduction)
# =====================================================
def apply_median_blur(image, kernel_size=5):
    """
    Reduces noise before edge detection.
    """
    return cv2.medianBlur(image, kernel_size)


# =====================================================
# 2️⃣ Canny Edge Detection
# =====================================================
def canny_edge_detection(image, threshold1=100, threshold2=200):
    """
    Canny edge detection with adjustable thresholds.
    """
    edges = cv2.Canny(image, threshold1, threshold2)
    return edges


# =====================================================
# 3️⃣ Adaptive Threshold Edge Detection
# =====================================================
def adaptive_edge_detection(image, block_size=9, C=2):
    """
    Adaptive thresholding for better lighting handling.
    """
    adaptive_edges = cv2.adaptiveThreshold(
        image,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        block_size,
        C
    )
    return adaptive_edges


# =====================================================
# 4️⃣ Adjust Edge Thickness
# =====================================================
def adjust_edge_thickness(edges, thickness=1):
    """
    Increase edge thickness using dilation.
    """
    kernel = np.ones((thickness, thickness), np.uint8)
    thick_edges = cv2.dilate(edges, kernel, iterations=1)
    return thick_edges


# =====================================================
# 5️⃣ Complete Cartoon Edge Pipeline
# =====================================================
def cartoon_edges(
    pil_image,
    method="canny",
    threshold1=100,
    threshold2=200,
    block_size=9,
    C=2,
    blur_kernel=5,
    thickness=1
):
    """
    Full edge detection pipeline.
    """

    # Convert PIL to OpenCV
    img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Noise reduction
    blurred = apply_median_blur(gray, blur_kernel)

    # Edge detection method selection
    if method == "canny":
        edges = canny_edge_detection(blurred, threshold1, threshold2)

    elif method == "adaptive":
        edges = adaptive_edge_detection(blurred, block_size, C)

    else:
        raise ValueError("Invalid method selected")

    # Adjust thickness
    edges = adjust_edge_thickness(edges, thickness)

    # Convert back to PIL
    return Image.fromarray(edges)


# =====================================================
# 6️⃣ Comparison Function
# =====================================================
def compare_images(original_pil, edge_pil):
    """
    Display original vs edge-detected image side by side.
    """

    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

    ax[0].imshow(original_pil)
    ax[0].set_title("Original")
    ax[0].axis("off")

    ax[1].imshow(edge_pil, cmap="gray")
    ax[1].set_title("Edge Detection")
    ax[1].axis("off")

    plt.tight_layout()
    plt.show()