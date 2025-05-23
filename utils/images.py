import pyautogui
from PIL import Image
import os

def take_screenshot(save_path):
    """Сохраняет скриншот экрана в указанный путь."""
    screenshot = pyautogui.screenshot()
    screenshot.save(save_path) # todo перенести в другой файл

# def compare_images(image_path1, image_path2):
#     """Сравнивает два изображения и возвращает коэффициент сходства (0-1)."""
#     from PIL import ImageChops
#     import numpy as np
#
#     img1 = Image.open(image_path1).convert('RGB')
#     img2 = Image.open(image_path2).convert('RGB')
#
#     # Убедимся, что изображения одного размера
#     if img1.size != img2.size:
#         img2 = img2.resize(img1.size)
#
#     # Вычисляем разницу между изображениями
#     diff = ImageChops.difference(img1, img2)
#     diff_data = np.array(diff)
#     diff_pixels = np.sum(diff_data > 0)
#     total_pixels = np.prod(img1.size)
#
#     # Возвращаем коэффициент сходства
#     return 1 - (diff_pixels / total_pixels)