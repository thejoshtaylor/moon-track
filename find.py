# Moon Tracker
# Joshua Taylor - 2024

from helper import resize

import cv2
from math import ceil

def get_circles(image):
    # get a properly sized image
    img = image.copy()
    # img, scale = resize(img)
    # print(scale)
    scale = 1

    # confirm size
    h, w = img.shape[:2]

    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # find the circles
    max_size = min(h, w) // 2
    min_size = min(h, w) // 100
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        1,
        minDist=min_size,
        param1=150,
        param2=30,
        minRadius=min_size,
        maxRadius=max_size,
    )
    if circles is None:
        return
    # print(circles)
    for circle in circles[0]:
        (x, y, r) = circle
        x = int(x * (1 / scale))
        y = int(y * (1 / scale))
        r = int(r * 1.1 * (1 / scale))
        yield (x, y, r)