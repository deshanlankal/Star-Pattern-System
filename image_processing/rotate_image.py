from PIL import Image

def rotate_image(img):
    return img.rotate(90, expand=True)
