import pyautogui
import cv2
import numpy as np
from pathlib import Path

TEMPLATES_DIR = Path("data/templates")

def find_template_center(template_name: str, confidence=0.9):
    """
    Ищет шаблон на экране и возвращает координаты центра совпадения.
    """
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    template_path = TEMPLATES_DIR / f"{template_name}.png"
    template = cv2.imread(str(template_path))
    if template is None:
        raise FileNotFoundError(f"Template {template_path} not found.")

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val < confidence:
        raise ValueError(f"No good match found for template '{template_name}' (confidence: {max_val:.2f})")

    h, w = template.shape[:2]
    center_x = max_loc[0] + w // 2
    center_y = max_loc[1] + h // 2
    return center_x, center_y


def click_on(template_name: str):
    x, y = find_template_center(template_name)
    pyautogui.click(x, y)

def double_click_on(template_name: str):
    x, y = find_template_center(template_name)
    pyautogui.doubleClick(x, y)