import pyautogui
import time
import os
import json
from datetime import datetime
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
    time.sleep(5)

    # Нажатие кнопки 'OK' в начальном окне
    logger.info("Нажимаем кнопку 'OK' в начальном окне...")
    pyautogui.press('enter')
    time.sleep(2)

    # Создание нового отчёта
    logger.info("Создаём новый отчёт...")
    pyautogui.doubleClick(x=1040, y=460)
    time.sleep(2)

    # Сохранение скриншота до создания текстового блока
    before_screenshot = os.path.join("screenshots", "before", f"before_textbox_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    take_screenshot(before_screenshot)
    logger.info(f"Скриншот до создания текстового блока сохранён: {before_screenshot}")

    # Создание текстового блока
    logger.info("Создаём текстовый блок...")
    # Нажатие на кнопку Text в toolbar
    pyautogui.click(x=coords["toolbar"]["text_button"][0], y=coords["toolbar"]["text_button"][1])
    time.sleep(1)

    # Клик по точке добавления текста
    pyautogui.click(x=coords["canvas"]["text_add_point"][0], y=coords["canvas"]["text_add_point"][1])
    time.sleep(1)

    # Двойной клик для открытия редактора текста
    pyautogui.doubleClick(x=coords["canvas"]["text_add_point"][0], y=coords["canvas"]["text_add_point"][1]-10)
    time.sleep(1)

    # Ввод текста
    test_text = "Test Report Text"
    pyautogui.write(test_text, interval=0.1)
    logger.info(f"Введён текст: {test_text}")

    # Нажатие кнопки OK в редакторе текста
    # pyautogui.click(x=coords["text_editor"]["ok_button"][0], y=coords["text_editor"]["ok_button"][1])
    pyautogui.hotkey('ctrl', 'enter')  # Самый удобный способ
    time.sleep(1)

    # Сохранение скриншота после создания текстового блока
    after_screenshot = os.path.join("screenshots", "after", f"after_textbox_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    take_screenshot(after_screenshot)
    logger.info(f"Скриншот после создания текстового блока сохранён: {after_screenshot}")

    # Проверка изменений и соответствия эталонному изображению
    try:
        # Определяем область canvas для проверки (x, y, w, h)
        canvas_region = (
            coords["canvas"]["text_add_point"][0] - 50,  # x
            coords["canvas"]["text_add_point"][1] - 50,  # y
            100,  # ширина
            100   # высота
        )
        # Проверка изменений в области
        verify_region_changed((before_screenshot, after_screenshot), canvas_region)
        logger.info("Изменения в области canvas успешно зафиксированы: текстовый блок создан.")

        # Проверка соответствия эталонному изображению
        reference_screenshot = os.path.join("screenshots", "references", "textbox_reference.png")
        verify_region_matches_reference(after_screenshot, reference_screenshot, canvas_region, threshold=0.95)
        logger.info("Скриншот соответствует эталонному изображению: текстовый блок создан корректно.")
    except AssertionError as e:
        logger.error(f"Ошибка проверки: {e}")
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка при проверке: {e}")
        raise

    logger.info("Тест создания нового отчёта и текстового блока завершён.")