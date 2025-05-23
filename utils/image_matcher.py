import pyautogui
import cv2
import numpy as np
from pathlib import Path
import yaml

TEMPLATES_DIR = Path("data/templates")
CONFIG = yaml.safe_load(open("data/config.yaml", encoding="utf-8"))

import pyautogui
import cv2
import numpy as np
from pathlib import Path

TEMPLATES_DIR = Path("data/templates")

def find_template_center(template_name: str, threshold=0.6, scale_range=(0.8, 2), step=0.05):
    """
    Ищет шаблон на экране в разных масштабах и возвращает координаты центра совпадения.
    """
    # 1. Скрин экрана
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # 2. Чтение шаблона
    template_path = TEMPLATES_DIR / f"{template_name}.png"
    template_orig = cv2.imread(str(template_path))
    if template_orig is None:
        raise FileNotFoundError(f"Template '{template_name}' not found.")

    best_match_val = -1
    best_match_pos = None
    best_template_shape = None

    # 3. Мульти-масштабный поиск
    for scale in np.arange(scale_range[0], scale_range[1] + step, step):
        resized_template = cv2.resize(
            template_orig,
            dsize=None,
            fx=scale,
            fy=scale,
            interpolation=cv2.INTER_AREA
        )

        if resized_template.shape[0] > screenshot.shape[0] or resized_template.shape[1] > screenshot.shape[1]:
            continue  # не искать, если шаблон больше экрана

        result = cv2.matchTemplate(screenshot, resized_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val > best_match_val:
            best_match_val = max_val
            best_match_pos = max_loc
            best_template_shape = resized_template.shape

    if best_match_val < threshold:
        raise ValueError(
            f"No good match for template '{template_name}' (best confidence: {best_match_val:.2f})"
        )

    h, w = best_template_shape[:2]
    center_x = best_match_pos[0] + w // 2
    center_y = best_match_pos[1] + h // 2
    return center_x, center_y



def click_on(template_name: str):
    x, y = find_template_center(template_name)
    pyautogui.click(x, y)

def double_click_on(template_name: str):
    x, y = find_template_center(template_name)
    pyautogui.doubleClick(x, y)