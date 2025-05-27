import pytest
import os
from pathlib import Path

def test_object_functions(logger, config, canvas_region, actions, verifications, image_matcher):
    """
    Тест функций объектов (удаление, копирование, вырезание, вставка, редактирование, очищение,
    вынос на передний и задний план) через горячие клавиши и контекстное меню.

    Args:
        logger: Фикстура логгера.
        config: Фикстура конфигурации.
        canvas_region: Фикстура области canvas.
        actions: Фикстура для действий из utils.actions.
        verifications: Фикстура для функций верификации из utils.verifications.
        image_matcher: Фикстура для функций поиска по шаблонам из utils.image_matcher.
    """
    logger.info("Запуск теста функций объектов...")
    test_text = config.get("test_text", "Test Text Тест Текст 123")
    canvas_region = tuple(config.get("canvas_region", [220, 180, 720, 400]))  # [x, y, w, h]
    after_action_delay = config.get("delays", {}).get("after_action", 0.5)

    # Открытие приложения и создание нового отчёта
    actions.open_fastreport()
    actions.create_new_report("null_report")

    # Сохранение скриншота до создания текстового блока
    before_screenshot = actions.take_screenshot_with_timestamp("before")

    # Создание текстового блока и ввод текста
    actions.create_object("text_button", "canvas_new")
    center_x, center_y = image_matcher.find_template_center("new_textbox")
    text_region = (center_x - 70, center_y - 20, 200, 100)  # Область вокруг текстового блока
    actions.input_text(test_text)

    # Сохранение скриншота после создания текстового блока
    after_screenshot_base = actions.take_screenshot_with_timestamp("after")

    # Проверка создания текстового блока
    verifications.check_region_changed(
        before_screenshot,
        after_screenshot_base,
        text_region,
        "Изменения в области canvas успешно зафиксированы: текстовый блок создан.",
        "Ошибка проверки после создания текстового блока: "
    )

    # Тестирование функций через горячие клавиши
    logger.info("Тестирование функций через горячие клавиши...")

    # 1. Копирование (Ctrl+C)
    logger.info("Копирование текстового блока (Ctrl+C)...")
    image_matcher.click_on("test_text_123")
    actions.pyautogui.hotkey('ctrl', 'c')
    after_copy_screenshot = actions.take_screenshot_with_timestamp("after")

    # 2. Вставка (Ctrl+V)
    logger.info("Вставка текстового блока (Ctrl+V)...")
    actions.pyautogui.hotkey('ctrl', 'v')
    actions.pyautogui.click(x=center_x - 100, y=center_y)  # Клик левее первого блока, на той же высоте
    actions.pyautogui.sleep(after_action_delay)
    after_paste_screenshot = actions.take_screenshot_with_timestamp("after")
    verifications.check_region_changed(
        after_copy_screenshot,
        after_paste_screenshot,
        canvas_region,
        "Изменения в области canvas успешно зафиксированы: текстовый блок вставлен (горячие клавиши).",
        "Ошибка проверки после вставки (горячие клавиши): "
    )

    # 3. Вырезание (Ctrl+X)
    logger.info("Вырезание текстового блока (Ctrl+X)...")
    image_matcher.click_on("test_text_123")
    actions.pyautogui.hotkey('ctrl', 'x')
    after_cut_screenshot = actions.take_screenshot_with_timestamp("after")
    verifications.check_region_changed(
        after_paste_screenshot,
        after_cut_screenshot,
        text_region,
        "Изменения в области canvas успешно зафиксированы: текстовый блок вырезан (горячие клавиши).",
        "Ошибка проверки после вырезания (горячие клавиши): "
    )

    # 4. Вставка вырезанного блока (Ctrl+V)
    logger.info("Вставка вырезанного текстового блока (Ctrl+V)...")
    actions.pyautogui.hotkey('ctrl', 'v')
    actions.pyautogui.click(x=center_x - 100, y=center_y)  # Клик левее первого блока, на той же высоте
    actions.pyautogui.sleep(after_action_delay)
    after_paste2_screenshot = actions.take_screenshot_with_timestamp("after")
    verifications.check_region_changed(
        after_cut_screenshot,
        after_paste2_screenshot,
        canvas_region,
        "Изменения в области canvas успешно зафиксированы: вырезанный блок вставлен (горячие клавиши).",
        "Ошибка проверки после вставки вырезанного блока (горячие клавиши): "
    )

    # 5. Редактирование текста
    logger.info("Редактирование текстового блока (горячие клавиши)...")
    image_matcher.double_click_on("test_text_123")
    actions.pyautogui.hotkey('ctrl', 'a')
    actions.pyautogui.write("Edited Text", interval=0.1)
    actions.pyautogui.hotkey('ctrl', 'enter')
    after_edit_screenshot = actions.take_screenshot_with_timestamp("after")
    verifications.check_region_changed(
        after_paste2_screenshot,
        after_edit_screenshot,
        text_region,
        "Изменения в области canvas успешно зафиксированы: текст отредактирован (горячие клавиши).",
        "Ошибка проверки после редактирования (горячие клавиши): "
    )

    # 6. Очищение текста
    logger.info("Очищение текстового блока (горячие клавиши)...")
    image_matcher.double_click_on("edited_text")
    actions.pyautogui.hotkey('ctrl', 'a')
    actions.pyautogui.press('delete')
    actions.pyautogui.hotkey('ctrl', 'enter')
    after_clear_screenshot = actions.take_screenshot_with_timestamp("after")
    verifications.check_region_changed(
        after_edit_screenshot,
        after_clear_screenshot,
        text_region,
        "Изменения в области canvas успешно зафиксированы: текст очищен (горячие клавиши).",
        "Ошибка проверки после очищения (горячие клавиши): "
    )

    # 7. Удаление объекта (Delete)
    logger.info("Удаление текстового блока (Delete)...")
    image_matcher.click_on("empty_block")
    actions.pyautogui.press('delete')
    after_delete_screenshot = actions.take_screenshot_with_timestamp("after")
    verifications.check_region_changed(
        after_clear_screenshot,
        after_delete_screenshot,
        text_region,
        "Изменения в области canvas успешно зафиксированы: текстовый блок удалён (горячие клавиши).",
        "Ошибка проверки после удаления (горячие клавиши): "
    )



    # Тестирование функций через контекстное меню
    logger.info("Тестирование функций через контекстное меню...")

    # 8. Копирование через контекстное меню
    logger.info("Копирование текстового блока через контекстное меню...")
    actions.context_menu_action("test_text123", action="copy")
    after_copy_menu_screenshot = actions.take_screenshot_with_timestamp("after")

    # 9. Вставка через контекстное меню
    logger.info("Вставка текстового блока через контекстное меню...")
    actions.context_menu_action("test_text123", action="paste")
    actions.pyautogui.click(x=center_x - 100, y=center_y)  # Клик левее первого блока, на той же высоте
    actions.pyautogui.sleep(after_action_delay)
    after_paste_menu_screenshot = actions.take_screenshot_with_timestamp("after")
    verifications.check_region_changed(
        after_copy_menu_screenshot,
        after_paste_menu_screenshot,
        canvas_region,
        "Изменения в области canvas успешно зафиксированы: текстовый блок вставлен (контекстное меню).",
        "Ошибка проверки после вставки (контекстное меню): "
    )

    # 10. Вырезание через контекстное меню
    logger.info("Вырезание текстового блока через контекстное меню...")
    actions.context_menu_action("test_text123", action="cut")
    after_cut_menu_screenshot = actions.take_screenshot_with_timestamp("after")
    verifications.check_region_changed(
        after_paste_menu_screenshot,
        after_cut_menu_screenshot,
        text_region,
        "Изменения в области canvas успешно зафиксированы: текстовый блок вырезан (контекстное меню).",
        "Ошибка проверки после вырезания (контекстное меню): "
    )

    # 11. Вставка вырезанного блока через контекстное меню
    logger.info("Вставка вырезанного текстового блока через контекстное меню...")
    actions.context_menu_action("test_text123", action="paste")
    actions.pyautogui.click(x=center_x - 100, y=center_y)  # Клик левее первого блока, на той же высоте
    actions.pyautogui.sleep(after_action_delay)
    after_paste2_menu_screenshot = actions.take_screenshot_with_timestamp("after")
    verifications.check_region_changed(
        after_cut_menu_screenshot,
        after_paste2_menu_screenshot,
        canvas_region,
        "Изменения в области canvas успешно зафиксированы: вырезанный блок вставлен (контекстное меню).",
        "Ошибка проверки после вставки вырезанного блока (контекстное меню): "
    )

    # 12. Редактирование через контекстное меню
    logger.info("Редактирование текстового блока через контекстное меню...")
    actions.context_menu_action("test_text123", action="edit")
    after_edit_menu_screenshot = actions.take_screenshot_with_timestamp("after")
    verifications.check_region_changed(
        after_paste2_menu_screenshot,
        after_edit_menu_screenshot,
        text_region,
        "Изменения в области canvas успешно зафиксированы: текст отредактирован (контекстное меню).",
        "Ошибка проверки после редактирования (контекстное меню): "
    )

    # 13. Очищение через контекстное меню
    logger.info("Очищение текстового блока через контекстное меню...")
    actions.context_menu_action("test_text123", action="clear")
    after_clear_menu_screenshot = actions.take_screenshot_with_timestamp("after")
    verifications.check_region_changed(
        after_edit_menu_screenshot,
        after_clear_menu_screenshot,
        text_region,
        "Изменения в области canvas успешно зафиксированы: текст очищен (контекстное меню).",
        "Ошибка проверки после очищения (контекстное меню): "
    )

    # 14. Удаление через контекстное меню
    logger.info("Удаление текстового блока через контекстное меню...")
    actions.context_menu_action("test_text123", action="delete")
    after_delete_menu_screenshot = actions.take_screenshot_with_timestamp("after")
    verifications.check_region_changed(
        after_clear_menu_screenshot,
        after_delete_menu_screenshot,
        text_region,
        "Изменения в области canvas успешно зафиксированы: текстовый блок удалён (контекстное меню).",
        "Ошибка проверки после удаления (контекстное меню): "
    )

    # # 15. Вынос на передний план через контекстное меню
    # logger.info("Вынос текстового блока на передний план через контекстное меню...")
    # actions.create_object("text_button", "canvas_new")  # Создаём новый блок для теста Z-порядка
    # actions.input_text(test_text)
    # after_create3_screenshot = actions.take_screenshot_with_timestamp("after")
    # actions.change_z_order("test_text_123", action="foreground")
    # after_foreground_screenshot = actions.take_screenshot_with_timestamp("after")
    # verifications.check_region_changed(
    #     after_create3_screenshot,
    #     after_foreground_screenshot,
    #     canvas_region,
    #     "Изменения в области canvas успешно зафиксированы: блок вынесен на передний план (контекстное меню).",
    #     "Ошибка проверки после выноса на передний план (контекстное меню): "
    # )
    #
    # # 16. Вынос на задний план через контекстное меню
    # logger.info("Вынос текстового блока на задний план через контекстное меню...")
    # actions.change_z_order("test_text_123", action="background")
    # after_background_screenshot = actions.take_screenshot_with_timestamp("after")
    # verifications.check_region_changed(
    #     after_foreground_screenshot,
    #     after_background_screenshot,
    #     canvas_region,
    #     "Изменения в области canvas успешно зафиксированы: блок вынесен на задний план (контекстное меню).",
    #     "Ошибка проверки после выноса на задний план (контекстное меню): "
    # )
    #
    # logger.info("Тест функций объектов завершён.")