import cv2
import numpy as np
from PIL import Image

def convert_to_grayscale(img):
    # Convert a PIL Image to grayscale
    img_np = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    return Image.fromarray(img_np)
