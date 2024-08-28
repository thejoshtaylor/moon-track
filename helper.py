# Moon Tracker
# Joshua Taylor - 2024

import cv2

def resize(image):
    img = image.copy()

    h, w = img.shape[:2]
    scale = 1.0
    while max(h, w) > 1000:
        scale /= 2
        h, w = int(h / 2), int(w / 2)

    # no change needed
    if scale == 1:
        return img, scale

    # downsize
    return cv2.resize(
        img,  # original image
        (0, 0),  # set fx and fy, not the final size
        fx=scale,
        fy=scale,
        interpolation=cv2.INTER_NEAREST,
    ), scale
