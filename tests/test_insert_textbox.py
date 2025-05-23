import os
import pyautogui
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
    change_z_order,
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


    # Перетаскивание текстового блока
    logger.info("Перетаскиваем первый текстовый блок...")
    drag_object(template_name="test_text_123", offset_x=150, offset_y=0)
    after_drag_screenshot = take_screenshot_with_timestamp("after")

    try:
        # Пересчитываем координаты первого объекта после перетаскивания
        textbox_center_after_drag = find_template_center("test_text_123")
        canvas_region = (
            textbox_center_after_drag[0] - 75,
            textbox_center_after_drag[1] - 75,
            100,
            100
        )
        verify_region_changed((after_screenshot_base, after_drag_screenshot), canvas_region)
        logger.info("Изменения в области canvas успешно зафиксированы: блок перетащен.")
    except AssertionError as e:
        logger.error(f"Ошибка проверки после перетаскивания: {e}")
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка после перетаскивания: {e}")
        raise

    logger.info("Тест создания, изменения размера и перетаскивания текстового блока завершён.")


    # # Изменение размера текстового блока
    # resize_object(template_name="test_text_123", handle_template="resize_handle", offset_x=50, offset_y=0)
    # after_resize_screenshot = take_screenshot_with_timestamp("after")
    #
    # try:
    #     verify_region_changed((after_screenshot_base, after_resize_screenshot), canvas_region)
    #     logger.info("Изменения в области canvas успешно зафиксированы: размер блока изменён.")
    #
    # except AssertionError as e:
    #     logger.error(f"Ошибка проверки после изменения размера: {e}")
    #     raise
    # except Exception as e:
    #     logger.error(f"Неожиданная ошибка после изменения размера: {e}")
    #     raise

    logger.info("Вставляем изображение из буфера обмена с помощью Ctrl+V...")
    text_block_width = 50
    left_edge_x = textbox_center_after_drag[0] - (text_block_width // 2)  # Левый край текстового блока
    y_position = textbox_center_after_drag[1] + 10  # Смещение вниз на 10 пикселей

    pyautogui.click(left_edge_x, y_position)  # Клик для размещения изображения # Клик для установки фокуса
    time.sleep(0.2)

    pyautogui.hotkey("ctrl", "v")  # Вставка изображения из буфера
    time.sleep(0.5)

    pyautogui.click(left_edge_x, y_position)  # Повторный клик для "подтверждения" вставки
    time.sleep(2)  # Ожидание рендеринга изображения

    after_image_screenshot = take_screenshot_with_timestamp("after")

    # Проверяем, что изображение успешно вставлено
    try:
        find_template_center("inserted_image", confidence=0.9)
        verify_region_changed((after_drag_screenshot, after_image_screenshot), canvas_region)
        logger.info("Изменения в области canvas успешно зафиксированы: изображение вставлено.")
    except ValueError as e:
        logger.error(f"Не удалось найти вставленное изображение: {e}")
        raise
    except AssertionError as e:
        logger.error(f"Ошибка проверки после вставки изображения: {e}")
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка после вставки изображения: {e}")
        raise

    # Изменение Z-порядка (вынос изображения на передний план)
    logger.info("Изменяем Z-порядок изображения (вынос на передний план)...")
    change_z_order(template_name="inserted_image", action="background")
  # Исправлено на inserted_image
    after_z_order_front_screenshot = take_screenshot_with_timestamp("after")

    # Проверка изменения Z-порядка (вынос на передний план)
    try:
        verify_region_changed((after_image_screenshot, after_z_order_front_screenshot), canvas_region)
        logger.info(
            "Изменения в области canvas успешно зафиксированы: Z-порядок изменён (вынос изображения на передний план).")

        z_order_front_reference = os.path.join("screenshots", "references", "z_order_front_reference.png")
        verify_region_matches_reference(
            after_z_order_front_screenshot,
            z_order_front_reference,
            canvas_region,
            threshold=0.95
        )
        logger.info(
            "Скриншот соответствует эталонному изображению: Z-порядок изображения изменён корректно (вынос на передний план).")
    except AssertionError as e:
        logger.error(f"Ошибка проверки после выноса изображения на передний план: {e}")
        raise
    except FileNotFoundError as e:
        logger.error(f"Эталонный скриншот не найден: {e}")
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка после выноса изображения на передний план: {e}")
        raise

    # Изменение Z-порядка (вынос изображения на задний план)
    logger.info("Изменяем Z-порядок изображения (вынос на задний план)...")
    change_z_order(template_name="inserted_image", action="background")  # Исправлено на inserted_image
    after_z_order_back_screenshot = take_screenshot_with_timestamp("after")

    # Проверка изменения Z-порядка (вынос на задний план)
    try:
        verify_region_changed((after_z_order_front_screenshot, after_z_order_back_screenshot), canvas_region)
        logger.info(
            "Изменения в области canvas успешно зафиксированы: Z-порядок изменён (вынос изображения на задний план).")

        z_order_back_reference = os.path.join("screenshots", "references", "z_order_back_reference.png")
        verify_region_matches_reference(
            after_z_order_back_screenshot,
            z_order_back_reference,
            canvas_region,
            threshold=0.95
        )
        logger.info(
            "Скриншот соответствует эталонному изображению: Z-порядок изображения изменён корректно (вынос на задний план).")
    except AssertionError as e:
        logger.error(f"Ошибка проверки после выноса изображения на задний план: {e}")
        raise
    except FileNotFoundError as e:
        logger.error(f"Эталонный скриншот не найден: {e}")
        raise
    except Exception as e:
        logger.error(f"Неожиданная ошибка после выноса изображения на задний план: {e}")
        raise

    logger.info("Тест создания текстового блока, вставки изображения и изменения Z-порядка завершён.")