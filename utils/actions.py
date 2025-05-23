import pyautogui
import time
import os
from datetime import datetime
import yaml
from utils.logger import setup_logger
from utils.image_matcher import click_on, double_click_on, find_template_center
from utils.images import take_screenshot
import subprocess

# Настройка логгера
logger = setup_logger(log_file=os.path.join("logs", "ui_test.log"))

# Загрузка конфигурации
CONFIG = yaml.safe_load(open("data/config.yaml", encoding="utf-8"))

def setup_pyautogui():
    """Настраивает параметры PyAutoGUI из конфига."""
    pyautogui.FAILSAFE = CONFIG.get("pyautogui", {}).get("failsafe", True)
    pyautogui.PAUSE = CONFIG.get("pyautogui", {}).get("pause", 0.5)
    logger.info(f"PyAutoGUI настроен: FAILSAFE={pyautogui.FAILSAFE}, PAUSE={pyautogui.PAUSE}")

def open_fastreport():
    """Открывает приложение FastReport альтернативными способами."""
    app_path = CONFIG.get("app_path", r"C:\Program Files (x86)\Fast Reports\.NET\2025.2.3\FastReport .NET WinForms Pack Trial\Designer.exe")
    app_launch_delay = CONFIG.get("delays", {}).get("app_launch", 6)
    after_action_delay = CONFIG.get("delays", {}).get("after_action", 0.5)

    logger.info("Запускаем FastReport...")

    # Способ 1: Через subprocess (предпочтительный)
    try:
        subprocess.Popen([app_path])
    except Exception as e:
        logger.warning(f"Не удалось запустить через subprocess: {e}")

        # Способ 2: Через os.startfile (для Windows)
        try:
            os.startfile(app_path)
        except Exception as e:
            logger.error(f"Не удалось запустить через os.startfile: {e}")

            # Способ 3: Резервный вариант через Win+R
            logger.warning("Используем резервный метод Win+R")
            pyautogui.hotkey('win', 'r')
            pyautogui.write(app_path)
            pyautogui.press('enter')

    time.sleep(app_launch_delay)

    logger.info("Нажимаем кнопку 'OK' в начальном окне...")
    pyautogui.press('enter')
    time.sleep(after_action_delay)

def create_new_report(template_name="null_report"):
    """Создаёт новый отчёт."""
    after_click_delay = CONFIG.get("delays", {}).get("after_click", 1)
    logger.info("Создаём новый отчёт...")
    click_on(template_name)
    time.sleep(after_click_delay)

def create_object(object_type, canvas_template="canvas_new"):
    """
    Создаёт объект (текстовое поле, фигура, изображение) на canvas.

    Args:
        object_type: Название кнопки в toolbar ("text_button", "image_button", "figure_button" и т.д.).
        canvas_template: Шаблон для точки вставки на canvas.
    """
    after_click_delay = CONFIG.get("delays", {}).get("after_click", 1)
    logger.info(f"Создаём объект типа {object_type}...")
    click_on(object_type)
    click_on(canvas_template)
    time.sleep(after_click_delay)

def input_text(text, use_hotkey=True):
    """
    Вводит текст в редакторе и подтверждает.

    Args:
        text: Текст для ввода.
        use_hotkey: Если True, подтверждает через Ctrl+Enter, иначе через кнопку OK.
    """
    after_double_click_delay = CONFIG.get("delays", {}).get("after_double_click", 1)
    after_text_input_delay = CONFIG.get("delays", {}).get("after_text_input", 1)

    logger.info(f"Открываем редактор текста для ввода: {text}")
    if use_hotkey:
        click_on("new_textbox")
        pyautogui.hotkey('ctrl', 'enter')
    else:
        double_click_on("new_textbox")
    time.sleep(after_double_click_delay)

    logger.info(f"Вводим текст: {text}")
    pyautogui.write(text, interval=0.1)
    time.sleep(after_text_input_delay)

    logger.info("Подтверждаем ввод текста...")
    if use_hotkey:
        pyautogui.hotkey('ctrl', 'enter')
    else:
        click_on("text_editor_ok_button")
    time.sleep(after_text_input_delay)

def resize_object(template_name="new_textbox", handle_template="resize_handle", offset_x=50, offset_y=50, duration=1):
    """
    Изменяет размер объекта, находя угловой квадратик через шаблон.

    Args:
        template_name: Шаблон объекта для определения начальной позиции.
        handle_template: Шаблон углового квадратика для изменения размера.
        offset_x, offset_y: Смещение для конечной точки перетаскивания (в пикселях).
        duration: Длительность перетаскивания в секундах.
    """
    after_action_delay = CONFIG.get("delays", {}).get("after_action", 0.5)
    after_resize_delay = CONFIG.get("delays", {}).get("after_resize", 1)

    logger.info(f"Ищем объект '{template_name}' для изменения размера...")
    x_start, y_start = find_template_center(template_name)
    logger.info(f"Ищем угловой квадратик '{handle_template}'...")
    x_handle, y_handle = find_template_center(handle_template)

    logger.info(f"Изменяем размер объекта: с ({x_handle}, {y_handle}) на ({x_handle + offset_x}, {y_handle + offset_y})...")
    pyautogui.click(x=x_handle, y=y_handle)
    time.sleep(after_action_delay)
    pyautogui.dragRel(offset_x, offset_y, duration=duration)
    time.sleep(after_resize_delay)

def drag_object(template_name="new_textbox", offset_x=150, offset_y=0, duration=1):
    """
    Перетаскивает объект, находя его через шаблон.

    Args:
        template_name: Шаблон объекта для перетаскивания.
        offset_x, offset_y: Смещение для перетаскивания (в пикселях).
        duration: Длительность перетаскивания в секундах.
    """
    after_action_delay = CONFIG.get("delays", {}).get("after_action", 0.5)
    after_drag_delay = CONFIG.get("delays", {}).get("after_drag", 1)

    logger.info(f"Ищем объект '{template_name}' для перетаскивания...")
    x_start, y_start = find_template_center(template_name)

    logger.info(f"Перетаскиваем объект: с ({x_start}, {y_start}) на смещение ({offset_x}, {offset_y})...")
    pyautogui.moveTo(x=x_start, y=y_start)
    time.sleep(after_action_delay)
    pyautogui.mouseDown()
    pyautogui.moveRel(offset_x, offset_y, duration=duration)
    pyautogui.mouseUp()
    time.sleep(after_drag_delay)

def take_screenshot_with_timestamp(folder="after"):
    """
    Делает скриншот и сохраняет его с временной меткой.

    Args:
        folder: Папка для сохранения ("before" или "after").

    Returns:
        Путь к сохранённому скриншоту.
    """
    screenshot_path = os.path.join("screenshots", folder, f"{folder}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    take_screenshot(screenshot_path)
    logger.info(f"Скриншот сохранён: {screenshot_path}")
    return screenshot_path