import cv2
import numpy as np
from PIL import Image

def sharpen_image(img):
    # Define a sharpening kernel
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    img_np = np.array(img)
    img_sharpened = cv2.filter2D(img_np, -1, kernel)
    return Image.fromarray(img_sharpened)
