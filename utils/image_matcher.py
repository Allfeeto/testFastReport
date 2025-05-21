import pyautogui
import cv2
import numpy as np
from pathlib import Path
import yaml

TEMPLATES_DIR = Path("data/templates")
CONFIG = yaml.safe_load(open("data/config.yaml", encoding="utf-8"))

def get_screen_scale():
    screen_w, screen_h = pyautogui.size()
    base_w, base_h = CONFIG["base_resolution"]
    return screen_w / base_w, screen_h / base_h

def scale_template(template_img, scale_w, scale_h):
    h, w = template_img.shape[:2]
    new_w = int(w * scale_w)
    new_h = int(h * scale_h)
    return cv2.resize(template_img, (new_w, new_h), interpolation=cv2.INTER_AREA)

def find_template_center(template_name: str, confidence=0.9):
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    template_path = TEMPLATES_DIR / f"{template_name}.png"
    template = cv2.imread(str(template_path))
    if template is None:
        raise FileNotFoundError(f"Template {template_path} not found.")

    # масштабируем шаблон
    scale_w, scale_h = get_screen_scale()
    template = scale_template(template, scale_w, scale_h)

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