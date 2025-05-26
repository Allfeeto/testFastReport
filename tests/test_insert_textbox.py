import os
import yaml
from pyautogui import moveTo
import time

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
from utils.verifications import verify_region_changed, verify_region_matches_reference, check_region_changed, \
    check_region_matches_reference

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
    input_text(test_text)

    # Сохранение скриншота после создания текстового блока
    after_screenshot_base = take_screenshot_with_timestamp("after")

    # Проверка изменений и соответствия эталонному изображению
    canvas_region = CONFIG.get("canvas_region", [200, 170, 1460, 800])
    check_region_changed(before_screenshot, after_screenshot_base, canvas_region,
                         "Изменения в области canvas успешно зафиксированы: текстовый блок создан.")
    check_region_matches_reference(after_screenshot_base, os.path.join("screenshots", "references", "textbox_reference.png"),canvas_region, threshold=0.95,
                                   success_msg="Скриншот соответствует эталонному изображению: текстовый блок создан корректно.",)

    # Изменение размера текстового блока
    resize_object(handle_template="resize_handle_right_top", offset_x=50, offset_y=-80)
    after_resize_screenshot = take_screenshot_with_timestamp("after")
    check_region_changed(after_screenshot_base, after_resize_screenshot, canvas_region,
                         "Изменения в области canvas успешно зафиксированы: размер блока изменён.",
                         "Ошибка проверки после изменения размера: ")

    # Перетаскивание текстового блока
    logger.info("Перетаскиваем первый текстовый блок...")
    drag_object(handle_template="resize_handle_right_top", offset_x=150, offset_y=70)
    after_drag_screenshot = take_screenshot_with_timestamp("after")
    check_region_changed(after_screenshot_base, after_drag_screenshot, canvas_region,
                         "Изменения в области canvas успешно зафиксированы: блок перетащен.",
                         "Ошибка проверки после перетаскивания: ")
    check_region_matches_reference(after_screenshot_base, os.path.join("screenshots", "references", "textbox_full_reference.png"),canvas_region, threshold=0.95,
                                   success_msg="Скриншот соответствует эталонному изображению: текстовый блок увеличен и перемещен корректно.",)

    logger.info("Тест создания, изменения размера и перетаскивания текстового блока завершён.")