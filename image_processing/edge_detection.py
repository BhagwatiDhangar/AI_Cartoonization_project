import cv2
import numpy as np

def get_edges(image):
    # black & white
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # noise kam
    blur = cv2.medianBlur(gray, 5)

    # edges
    edges = cv2.Canny(blur, 100, 200)

    return edges