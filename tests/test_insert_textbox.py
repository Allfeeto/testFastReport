import os

import yaml
from pyautogui import moveTo

from utils.actions import (
    setup_pyautogui,
    open_fastreport,
    create_new_report,
    create_object,
    input_text,
    resize_object,
    drag_object,
    take_screenshot_with_timestamp
)
from utils.logger import setup_logger
from utils.image_matcher import find_template_center
from utils.verifications import verify_region_changed, verify_region_matches_reference

# Настройка логгера
logger = setup_logger(log_file=os.path.join("logs", "ui_test.log"))

# Загрузка конфигурации
CONFIG = yaml.safe_load(open("data/config.yaml", encoding="utf-8"))

def test_create_report_and_textbox():
    # Настройка PyAutoGUI
    setup_pyautogui()

    # Создание директорий для скриншотов
    os.makedirs("screenshots/before", exist_ok=True)
    os.makedirs("screenshots/after", exist_ok=True)

    logger.info("Запуск теста создания отчёта и текстового блока...")
    test_text = CONFIG.get("test_text", "Test Text Тест Текст 123")

    # Открытие приложения и создание нового отчёта
    open_fastreport()
    create_new_report("null_report")

    # Сохранение скриншота до создания текстового блока
    before_screenshot = take_screenshot_with_timestamp("before")

    # Создание текстового блока и ввод текста
    create_object("text_button", "canvas_new")
    textbox_center = find_template_center("new_textbox")
    input_text(test_text)

    # Сохранение скриншота после создания текстового блока
    after_screenshot_base = take_screenshot_with_timestamp("after")

    # Проверка изменений и соответствия эталонному изображению
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


    moveTo(656, 261, duration=1) #todo это костыль - надо будет реализовать иначе все что ниже

    # Изменение размера текстового блока
    resize_object(x_start=656, y_start=261, x_end=710, y_end=200)
    after_resize_screenshot = take_screenshot_with_timestamp("after")

    try:
        verify_region_changed((after_screenshot_base, after_resize_screenshot), canvas_region)
        logger.info("Изменения в области canvas успешно зафиксированы: размер блока изменён.")

    except AssertionError as e:
        logger.error(f"Ошибка проверки после изменения размера: {e}")
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка после изменения размера: {e}")
        raise

    # Перетаскивание текстового блока
    drag_object(x_start=textbox_center[0], y_start=textbox_center[1], x_offset=150, y_offset=0)
    after_drag_screenshot = take_screenshot_with_timestamp("after")

    try:
        verify_region_changed((after_screenshot_base, after_drag_screenshot), canvas_region)
        logger.info("Изменения в области canvas успешно зафиксированы: блок перетащен.")

    except AssertionError as e:
        logger.error(f"Ошибка проверки после перетаскивания: {e}")
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка после перетаскивания: {e}")
        raise

    logger.info("Тест создания, изменения размера и перетаскивания текстового блока завершён.")