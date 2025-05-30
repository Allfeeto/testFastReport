import pyautogui
import time
import os
from datetime import datetime
import yaml
from utils.logger import setup_logger
from utils.image_matcher import click_on, double_click_on, find_template_center
import subprocess

from utils.verifications import take_screenshot

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
    app_path = CONFIG.get("app_path")
    app_launch_delay = CONFIG.get("delays", {}).get("app_launch", 6)
    after_action_delay = CONFIG.get("delays", {}).get("after_action", 0.5)
    app_demo_version = CONFIG.get("app_demo_version")

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

    if app_demo_version:
        logger.info("У Dас выбрана Демо версия FastReport. Нажимаем 'Enter' в окне информации об этом.")
        pyautogui.press('enter')
    else:
        logger.info("У Вас выбрана Полная версия FastReport.")

    time.sleep(after_action_delay)

def create_new_report(template_name="null_report"):
    """Создаёт новый отчёт."""
    after_click_delay = CONFIG.get("delays", {}).get("after_click", 1)
    logger.info("Создаём новый отчёт...")
    click_on(template_name)
    time.sleep(after_click_delay)

def close_fastreport():
    """Закрывает приложение FastReport с обработкой окна подтверждения сохранения."""
    close_delay = CONFIG.get("delays", {}).get("close_delay", 2)
    confirmation_delay = CONFIG.get("delays", {}).get("confirmation_delay", 1)
    after_action_delay = CONFIG.get("delays", {}).get("after_action", 0.5)

    logger.info("Закрываем FastReport...")

    # Нажатие Alt+F4 для закрытия основного окна
    try:
        pyautogui.hotkey('alt', 'f4')
        time.sleep(confirmation_delay)  # Ждём появления окна подтверждения
    except Exception as e:
        logger.error(f"Ошибка при закрытии окна через Alt+F4: {e}")
        raise

    # Обработка окна подтверждения (выбор "Нет" и Enter)
    try:
        logger.info("Обрабатываем окно подтверждения сохранения...")
        pyautogui.press('right')  # Перемещаем фокус на "Нет"
        time.sleep(0.5)  # Короткая задержка для стабильности
        pyautogui.press('enter')  # Подтверждаем выбор "Нет"
        time.sleep(close_delay)  # Ждём полного закрытия приложения
    except Exception as e:
        logger.error(f"Ошибка при обработке окна подтверждения: {e}")
        raise

    logger.info("FastReport успешно закрыт.")
    time.sleep(after_action_delay)



def create_object(object_type, canvas_template="canvas_new", x=None, y=None):
    """
    Создаёт объект в указанной позиции или по шаблону canvas_template.

    Args:
        object_type: Тип объекта (например, "text_button").
        canvas_template: Шаблон рабочей области (по умолчанию "canvas_new").
        x, y: Координаты для клика (если указаны, перекрывают canvas_template).
    """
    after_click_delay = CONFIG.get("delays", {}).get("after_click", 1)
    logger.info(f"Создаём объект типа {object_type}...")
    click_on(object_type)  # Выбираем тип объекта (например, кнопку текстового блока)
    if x is not None and y is not None:
        logger.info(f"Кликаем в координаты ({x}, {y}) для размещения объекта...")
        pyautogui.click(x=x, y=y)
    else:
        logger.info(f"Кликаем по шаблону {canvas_template} для размещения объекта...")
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

def resize_object(handle_template="resize_handle_right_top", offset_x=50, offset_y=50, duration=1):
    """
    Изменяет размер объекта, находя угловой квадратик через шаблон.

    Args:
        handle_template: Шаблон углового квадратика для изменения размера.
        offset_x, offset_y: Смещение для конечной точки перетаскивания (в пикселях).
        duration: Длительность перетаскивания в секундах.
    """
    after_action_delay = CONFIG.get("delays", {}).get("after_action", 0.5)
    after_resize_delay = CONFIG.get("delays", {}).get("after_resize", 1)

    logger.info(f"Ищем угловой квадратик '{handle_template}'...")
    x_handle, y_handle = find_template_center(handle_template)

    logger.info(f"Изменяем размер объекта: с ({x_handle}, {y_handle}) на ({x_handle + offset_x}, {y_handle + offset_y})...")
    pyautogui.click(x=x_handle, y=y_handle)
    time.sleep(after_action_delay)
    pyautogui.dragRel(offset_x, offset_y, duration=duration)
    time.sleep(after_resize_delay)

def drag_object(handle_template="resize_handle_right_top", offset_x=150, offset_y=0, duration=1):
    """
    Перетаскивает объект, определяя его положение через координаты resize-ручки и смещение вверх/влево.

    Args:
        handle_template: Шаблон resize-ручки (обычно правый нижний угол).
        offset_x, offset_y: Смещение для перетаскивания (в пикселях).
        duration: Длительность перетаскивания в секундах.
    """
    after_action_delay = CONFIG.get("delays", {}).get("after_action", 0.5)
    after_drag_delay = CONFIG.get("delays", {}).get("after_drag", 1)

    # Смещение от resize-ручки до "тела" объекта
    object_offset_x = -10  # сместиться влево от правого нижнего угла
    object_offset_y = 10  # сместиться вверх от правого нижнего угла

    logger.info(f"Ищем resize-ручку '{handle_template}' для вычисления положения объекта...")
    x_handle, y_handle = find_template_center(handle_template)

    # Получаем примерную точку в теле объекта
    x_start = x_handle + object_offset_x
    y_start = y_handle + object_offset_y

    logger.info(f"Перетаскиваем объект: от координат ({x_start}, {y_start}) со смещением ({offset_x}, {offset_y})...")
    pyautogui.moveTo(x=x_start, y=y_start)
    time.sleep(after_action_delay)
    pyautogui.mouseDown()
    pyautogui.moveRel(offset_x, offset_y, duration=duration)
    pyautogui.mouseUp()
    time.sleep(after_drag_delay)

def fill_object(template_name="color_textbox", fill_button_template="fill_color_button", color_template="color_red"):
    """
    Заливает объект цветом через кнопку заливки и выбор цвета.

    Args:
        template_name: Шаблон объекта для выбора.
        fill_button_template: Шаблон кнопки заливки.
        color_template: Шаблон цвета в выпадающем списке.
    """
    after_action_delay = CONFIG.get("delays", {}).get("after_action", 0.5)

    # 1) Выбираем объект
    logger.info(f"Ищем объект '{template_name}' для заливки...")
    x_obj, y_obj = find_template_center(template_name)
    pyautogui.click(x=x_obj, y=y_obj)
    time.sleep(after_action_delay)

    # 2) Находим кнопку заливки и кликаем правее центра
    logger.info(f"Ищем кнопку заливки '{fill_button_template}'...")
    x_fill, y_fill = find_template_center(fill_button_template)
    pyautogui.click(x=x_fill + 20, y=y_fill)  # Клик правее для выпадающего списка
    time.sleep(after_action_delay * 2)  # Ждём появления списка

    # 3) Выбираем цвет
    logger.info(f"Ищем цвет '{color_template}' в выпадающем списке...")
    x_color, y_color = find_template_center(color_template)
    pyautogui.click(x=x_color, y=y_color)
    time.sleep(after_action_delay)

    logger.info(f"Объект '{template_name}' залит цветом '{color_template}'")

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

def change_z_order(template_name="new_textbox", action="bring_to_front"):
    """
    Изменяет Z-порядок объекта (вынос на передний или задний план) с использованием поиска по скриншотам.
    """
    after_action_delay = CONFIG.get("delays", {}).get("after_action", 0.5)

    # 1) Находим объект по шаблону
    logger.info(f"Ищем объект '{template_name}' для изменения Z-порядка...")
    try:
        x_obj, y_obj = find_template_center(template_name, confidence=0.7)
        logger.info(f"Объект '{template_name}' найден на ({x_obj}, {y_obj})")
    except ValueError as e:
        logger.error(f"Не удалось найти объект '{template_name}': {e}")
        raise

    # 2) Открываем контекстное меню через правый клик по центру объекта
    offset_x = 20
    pyautogui.moveTo(x_obj + offset_x, y_obj)
    pyautogui.rightClick()
    time.sleep(after_action_delay * 2)  # ждем появления меню

    # 3) Определяем, какой пункт меню искать
    if action == "foreground":
        menu_template = "foreground"
        log_action = "Вынос на передний план"
    elif action == "background":
        menu_template = "background"
        log_action = "Вынос на задний план"
    else:
        logger.error(f"Неверное действие для Z-порядка: {action}")
        raise ValueError("Допустимые значения action: 'foreground' или 'background'")

    logger.info(f"Ищем пункт меню '{menu_template}' ({log_action})...")
    try:
        x_menu, y_menu = find_template_center(menu_template, confidence=0.7)
        logger.info(f"Пункт меню '{menu_template}' найден на ({x_menu}, {y_menu})")
        pyautogui.click(x=x_menu, y=y_menu)
        time.sleep(after_action_delay)
        logger.info(f"Действие '{log_action}' выполнено для объекта '{template_name}'")
    except ValueError as e:
        logger.error(f"Не удалось найти пункт меню '{menu_template}': {e}")
        debug_screenshot = take_screenshot_with_timestamp("debug_z_order_error")
        logger.info(f"Скриншот для отладки сохранён: {debug_screenshot}")
        raise

    logger.info(f"Z-порядок изменён на '{action}' для объекта '{template_name}'")

def context_menu_action(template_name="new_textbox", action="copy"):
    """
    Выполняет действие через контекстное меню для указанного объекта.

    Args:
        template_name: Шаблон объекта (например, "new_textbox").
        action: Действие для выполнения ("copy", "paste", "cut", "edit", "clear", "delete").

    Raises:
        ValueError: Если объект или пункт меню не найден, или указано неверное действие.
    """
    after_action_delay = CONFIG.get("delays", {}).get("after_action", 0.5)

    # 1) Находим объект по шаблону
    logger.info(f"Ищем объект '{template_name}' для действия '{action}'...")
    try:
        x_obj, y_obj = find_template_center(template_name, confidence=0.7)
        logger.info(f"Объект '{template_name}' найден на ({x_obj}, {y_obj})")
    except ValueError as e:
        logger.error(f"Не удалось найти объект '{template_name}': {e}")
        raise

    # 2) Открываем контекстное меню через правый клик
    pyautogui.moveTo(x_obj, y_obj)
    pyautogui.rightClick()
    time.sleep(after_action_delay * 2)  # Ждём появления меню

    # 3) Определяем шаблон для пункта меню
    menu_templates = {
        "copy": "copy_menu",
        "paste": "paste_menu",
        "cut": "cut_menu",
        "edit": "edit_menu",
        "clear": "clear_menu",
        "delete": "delete_menu"
    }
    if action not in menu_templates:
        logger.error(f"Неверное действие для контекстного меню: {action}")
        raise ValueError(f"Допустимые действия: {', '.join(menu_templates.keys())}")

    menu_template = menu_templates[action]
    log_action = action.capitalize()

    # 4) Кликаем по пункту меню
    logger.info(f"Ищем пункт меню '{menu_template}' ({log_action})...")
    try:
        x_menu, y_menu = find_template_center(menu_template, confidence=0.7)
        logger.info(f"Пункт меню '{menu_template}' найден на ({x_menu}, {y_menu})")
        pyautogui.click(x=x_menu, y=y_menu)
        time.sleep(after_action_delay)
        logger.info(f"Действие '{log_action}' выполнено для объекта '{template_name}'")
    except ValueError as e:
        logger.error(f"Не удалось найти пункт меню '{menu_template}': {e}")
        debug_screenshot = take_screenshot_with_timestamp(f"debug_{action}_error")
        logger.info(f"Скриншот для отладки сохранён: {debug_screenshot}")
        raise

    # 5) Дополнительные действия для редактирования или очищения
    if action == "edit":
        logger.info("Ожидаем открытия редактора для ввода текста...")
        time.sleep(after_action_delay)
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.write("Edited Text", interval=0.1)
        pyautogui.hotkey('ctrl', 'enter')
        time.sleep(after_action_delay)
    elif action == "clear":
        logger.info("Ожидаем открытия редактора для очищения текста...")
        time.sleep(after_action_delay)
        time.sleep(after_action_delay)

    logger.info(f"Действие '{action}' через контекстное меню выполнено для объекта '{template_name}'")