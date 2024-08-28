# Moon Tracker
# Joshua Taylor - 2024

from find import get_circles

import cv2
import numpy as np
import os

def generate_photo(directory, every=1, crop="original"):
    # get the rest of the images
    # find the files
    files = os.listdir(directory)
    files = [os.path.join(directory, f) for f in files if f.lower().endswith(".jpg")]
    # sort the files based on date
    files.sort(key=lambda f: os.path.getmtime(f))

    # get every nth file
    files = files[::every]

    # if there are no files, return None
    if len(files) == 0:
        return None

    result = None
    minX = 10_000
    minY = 10_000
    maxX = 0
    maxY = 0

    # from helper import resize

    # go through all and add them to the result
    for i, file in enumerate(files):
        print(f' [{i+1}/{len(files)}] {file}', ' '*20, end='\r')
        img = cv2.imread(file)
        circles = list(get_circles(img))
        mask = np.zeros_like(img)
        for x, y, r in circles:
            cv2.circle(mask, (x, y), r, (255, 255, 255), -1)
            minX = min(minX, x - r)
            minY = min(minY, y - r)
            maxX = max(maxX, x + r)
            maxY = max(maxY, y + r)
            # cv2.circle(result, (x, y), r, (0, 0, 255), 2)
        if result is None:
            result = np.where(mask == 0, 0, img)
        else:
            result = cv2.addWeighted(result, 1, np.where(mask == 0, 0, img), 1, 0)
            
    print(' '*80, end='\r')

    # crop the image
    if crop != "original":
        left = right = top = bottom = 0
        center = (minX + maxX) // 2, (minY + maxY) // 2

        if crop == "fit":
            left = minX
            right = maxX
            top = minY
            bottom = maxY
        elif crop == "square":
            size = max(maxX - minX, maxY - minY)
            halfSize = size // 2

            left = center[0] - halfSize
            right = center[0] + halfSize
            top = center[1] - halfSize
            bottom = center[1] + halfSize

        width = right - left
        height = bottom - top

        desiredMargin = 0.05

        # get the physical maximum bounds for our margins
        maxHorizontalMargin = min(left, result.shape[1] - right)
        maxVerticalMargin = min(top, result.shape[0] - bottom)

        # get the margin we're going to use
        margin = int(min(maxVerticalMargin, maxHorizontalMargin, max(width, height) * desiredMargin))

        newWidth = width + 2 * margin
        newHeight = height + 2 * margin

        newLeft = center[0] - newWidth // 2
        newRight = center[0] + newWidth // 2
        newTop = center[1] - newHeight // 2
        newBottom = center[1] + newHeight // 2

        # do the crop
        result = result[newTop:newBottom, newLeft:newRight]


    print('Done!')

    return result
