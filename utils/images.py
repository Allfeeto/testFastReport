import pyautogui
from PIL import Image
import os

def take_screenshot(save_path):
    screenshot = pyautogui.screenshot()
    screenshot.save(save_path)

def compare_images(image_path1, image_path2):
    from PIL import ImageChops
    import numpy as np

    img1 = Image.open(image_path1).convert('RGB')
    img2 = Image.open(image_path2).convert('RGB')

    if img1.size != img2.size:
        img2 = img2.resize(img1.size)

    diff = ImageChops.difference(img1, img2)
    diff_data = np.array(diff)
    diff_pixels = np.sum(diff_data > 0)
    total_pixels = np.prod(img1.size)

    return 1 - (diff_pixels / total_pixels)