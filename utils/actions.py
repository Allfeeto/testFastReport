import pyautogui
import time
import os
from datetime import datetime
from utils.logger import setup_logger
from utils.image_matcher import click_on, double_click_on, find_template_center
from utils.images import take_screenshot

# Настройка логгера
logger = setup_logger(log_file=os.path.join("logs", "ui_test.log"))


def setup_pyautogui():
    """Настраивает параметры PyAutoGUI."""
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5


def open_fastreport(
        app_path=r"C:\Program Files (x86)\Fast Reports\.NET\2025.2.3\FastReport .NET WinForms Pack Trial\Designer.exe"):
    """Открывает приложение FastReport."""
    logger.info("Запускаем FastReport...")
    pyautogui.hotkey('win', 'r')
    pyautogui.write(app_path)
    pyautogui.press('enter')
    time.sleep(6)  # Ждём загрузки приложения
    logger.info("Нажимаем кнопку 'OK' в начальном окне...")
    pyautogui.press('enter')
    time.sleep(1)


def create_new_report(template_name="null_report"):
    """Создаёт новый отчёт."""
    logger.info("Создаём новый отчёт...")
    click_on(template_name)
    time.sleep(1)


def create_object(object_type, canvas_template="canvas_new"):
    """
    Создаёт объект (текстовое поле, фигура, изображение) на canvas.

    Args:
        object_type: Название кнопки в toolbar ("text_button", "image_button", "figure_button" и т.д.).
        canvas_template: Шаблон для точки вставки на canvas.
    """
    logger.info(f"Создаём объект типа {object_type}...")
    click_on(object_type)
    click_on(canvas_template)
    time.sleep(1)


def input_text(text, use_hotkey=True):
    """
    Вводит текст в редакторе и подтверждает.

    Args:
        text: Текст для ввода.
        use_hotkey: Если True, подтверждает через Ctrl+Enter, иначе через кнопку OK.
    """
    logger.info(f"Вводим текст: {text}")
    if use_hotkey: # todo в случае если поле текста не в фокусе - добавить нажатие на него
        pyautogui.hotkey('ctrl', 'enter')
    else:
        double_click_on("new_textbox")
    time.sleep(1)
    pyautogui.write(text, interval=0.1)
    if use_hotkey:
        pyautogui.hotkey('ctrl', 'enter')
    else:
        click_on("text_editor_ok_button")
    time.sleep(1)







def resize_object(x_start, y_start, x_end, y_end, duration=1):
    """
    Изменяет размер объекта, перетаскивая его границу.

    Args:
        x_start, y_start: Начальные координаты для клика.
        x_end, y_end: Конечные координаты для перетаскивания.
        duration: Длительность перетаскивания в секундах.
    """
    logger.info(f"Изменяем размер объекта: с ({x_start}, {y_start}) до ({x_end}, {y_end})...")
    pyautogui.click(x=x_start, y=y_start)
    time.sleep(0.5)
    pyautogui.dragTo(x=x_end, y=y_end, duration=duration)
    time.sleep(1)


def drag_object(x_start, y_start, x_offset, y_offset, duration=1):
    """
    Перетаскивает объект на заданное смещение.

    Args:
        x_start, y_start: Начальные координаты для клика.
        x_offset, y_offset: Смещение для перетаскивания.
        duration: Длительность перетаскивания в секундах.
    """
    logger.info(f"Перетаскиваем объект: с ({x_start}, {y_start}) на смещение ({x_offset}, {y_offset})...")
    pyautogui.moveTo(x=x_start, y=y_start)
    time.sleep(0.5)
    pyautogui.mouseDown()
    pyautogui.moveRel(x_offset, y_offset, duration=duration)
    pyautogui.mouseUp()
    time.sleep(1)


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