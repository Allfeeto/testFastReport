import pyautogui
import time
import os
import json
from datetime import datetime

from utils.image_matcher import click_on, double_click_on, find_template_center
from utils.images import take_screenshot
from utils.logger import setup_logger
from utils.verifications import verify_region_changed, verify_region_matches_reference

# Настройка логгера
logger = setup_logger(log_file=os.path.join("logs", "ui_test.log"))

# Загрузка координат из файла
with open(os.path.join("data", "coordinates.json"), "r") as f:
    coords = json.load(f)

def test_create_report_and_textbox():
    # Настройка PyAutoGUI
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5

    # Создание директорий для скриншотов, если их нет
    os.makedirs("screenshots/before", exist_ok=True)
    os.makedirs("screenshots/after", exist_ok=True)

    # Логирование старта теста
    logger.info("Запуск теста создания отчёта и текстового блока...")

    # Запуск FastReport
    logger.info("Запускаем FastReport...")
    pyautogui.hotkey('win', 'r')
    pyautogui.write(r"C:\Program Files (x86)\Fast Reports\.NET\2025.2.3\FastReport .NET WinForms Pack Trial\Designer.exe")
    pyautogui.press('enter')
    time.sleep(6)

    # Нажатие кнопки 'OK' в начальном окне
    logger.info("Нажимаем кнопку 'OK' в начальном окне...")
    pyautogui.press('enter')
    time.sleep(1)

    # Создание нового отчёта
    logger.info("Создаём новый отчёт...")
    click_on("null_report")
    time.sleep(1)

    # Сохранение скриншота до создания текстового блока
    before_screenshot = os.path.join("screenshots", "before", f"before_textbox_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    take_screenshot(before_screenshot)
    logger.info(f"Скриншот до создания текстового блока сохранён: {before_screenshot}")

    # Создание текстового блока
    logger.info("Создаём текстовый блок...")
    # Нажатие на кнопку Text в toolbar
    click_on("text_button")
    # time.sleep(1)

    # Клик по точке добавления текста
    click_on("canvas_new")
    # time.sleep(1)

    # Двойной клик для открытия редактора текста
    # Получаем координаты центра текстового блока для будущей проверки
    textbox_center = find_template_center("new_textbox")
    double_click_on("new_textbox")
    time.sleep(1)

    # Ввод текста
    test_text = "Test Text"
    pyautogui.write(test_text, interval=0.1)
    logger.info(f"Введён текст: {test_text}")

    # Нажатие кнопки OK в редакторе текста
    pyautogui.hotkey('ctrl', 'enter')
    time.sleep(1)

    # Сохранение скриншота после создания текстового блока
    after_screenshot_base = os.path.join("screenshots", "after", f"after_textbox_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    take_screenshot(after_screenshot_base)
    logger.info(f"Скриншот после создания текстового блока сохранён: {after_screenshot_base}")

    # Проверка изменений и соответствия эталонному изображению после создания
    try:

        # Определяем область вокруг найденного центра
        canvas_region = (
            textbox_center[0] - 50,
            textbox_center[1] - 50,
            100,
            100
        )

        verify_region_changed((before_screenshot, after_screenshot_base), canvas_region)
        logger.info("Изменения в области canvas успешно зафиксированы: текстовый блок создан.")

        reference_screenshot = os.path.join("screenshots", "references", "textbox_reference.png")
        verify_region_matches_reference(after_screenshot_base, reference_screenshot, canvas_region, threshold=0.95)
        logger.info("Скриншот соответствует эталонному изображению: текстовый блок создан корректно.")

    except AssertionError as e:
        logger.error(f"Ошибка проверки после создания: {e}")
        raise
    except FileNotFoundError as e:
        logger.error(f"Шаблон не найден: {e}")
        raise
    except ValueError as e:
        logger.error(f"Проблема с поиском шаблона: {e}")
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка после создания: {e}")
        raise
"""
    # Изменение размера текстового блока
    logger.info("Начинаем изменение размера текстового блока...")
    pyautogui.click(x=353, y=271)
    time.sleep(0.5)

    # Перетаскивание правее
    pyautogui.dragTo(x=453, y=271, duration=1)
    time.sleep(1)

    after_resize_screenshot = os.path.join("screenshots", "after", f"after_resize_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    take_screenshot(after_resize_screenshot)
    logger.info(f"Скриншот после изменения размера сохранён: {after_resize_screenshot}")

    try:
        verify_region_changed((after_screenshot_base, after_resize_screenshot), canvas_region)
        logger.info("Изменения в области canvas успешно зафиксированы: размер блока изменён.")

    except AssertionError as e:
        logger.error(f"Ошибка проверки после изменения размера: {e}")
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка после изменения размера: {e}")
        raise

    # --- Перетаскивание текстового блока ---
    logger.info("Начинаем перетаскивание текстового блока...")
    pyautogui.moveTo(x=coords["canvas"]["text_add_point"][0], y=coords["canvas"]["text_add_point"][1]-10)
    time.sleep(0.5)

    pyautogui.mouseDown()
    pyautogui.moveRel(150, 0, duration=1)
    pyautogui.mouseUp()
    time.sleep(1)

    # Сохранение скриншота
    after_drag_screenshot = os.path.join("screenshots", "after", f"after_drag_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    take_screenshot(after_drag_screenshot)
    logger.info(f"Скриншот после перетаскивания сохранён: {after_drag_screenshot}")

    try:
        verify_region_changed((after_resize_screenshot, after_drag_screenshot), canvas_region)
        logger.info("Изменения в области canvas успешно зафиксированы: блок перетащен.")

    except AssertionError as e:
        logger.error(f"Ошибка проверки после перетаскивания: {e}")
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка после перетаскивания: {e}")
        raise

    logger.info("Тест создания, изменения размера и перетаскивания текстового блока завершён.")
"""