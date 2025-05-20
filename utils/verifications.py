import cv2
import numpy as np
from pathlib import Path

def verify_region_changed(screenshots, region):
    before_path, after_path = screenshots
    x, y, w, h = region

    img1 = cv2.imread(str(before_path))
    img2 = cv2.imread(str(after_path))
    roi1 = img1[y:y+h, x:x+w]
    roi2 = img2[y:y+h, x:x+w]

    diff = cv2.absdiff(roi1, roi2)
    mean_diff = np.mean(diff)

    if mean_diff < 5:
        raise AssertionError("Изменения в заданной области не зафиксированы")
