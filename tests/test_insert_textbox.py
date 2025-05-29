def test_create_report_and_textbox(logger, config, canvas_region, actions, verifications, image_matcher):
    """
    Тест создания отчёта, текстового блока, изменения размера и перетаскивания.

    Args:
        logger: Фикстура логгера.
        config: Фикстура конфигурации.
        canvas_region: Фикстура области canvas.
        actions: Фикстура для действий из utils.actions.
        verifications: Фикстура для функций верификации из utils.verifications.
    """
    logger.info("Запуск теста создания отчёта и текстового блока...")
    test_text = config.get("test_text", "Test Text Тест Текст 123")

    # Открытие приложения и создание нового отчёта
    actions.open_fastreport()
    actions.create_new_report("null_report")

    # Сохранение скриншота до создания текстового блока
    before_screenshot = actions.take_screenshot_with_timestamp("before")

    # Создание текстового блока и ввод текста
    actions.create_object("text_button", "canvas_new")
    # Находим координаты текстового блока по квадратику
    center_x, center_y = image_matcher.find_template_center("resize_handle_left_top")
    # Задаём область текста
    text_region = (center_x, center_y, 90, 16)
    actions.input_text(test_text)



    # Сохранение скриншота после создания текстового блока
    after_screenshot_base = actions.take_screenshot_with_timestamp("after")

    # Проверка изменений и соответствия эталонному изображению
    verifications.check_region_changed(before_screenshot, after_screenshot_base, text_region,
                                       "Изменения в области canvas успешно зафиксированы: текстовый блок создан.")
    verifications.check_region_matches_reference(
        after_screenshot_base,
        actions.get_path("screenshots", "references", "textbox_reference.png"),
        text_region,
        threshold=0.95,
        success_msg="Скриншот соответствует эталонному изображению: текстовый блок создан корректно."
    )

    # Изменение размера текстового блока
    actions.resize_object(handle_template="resize_handle_right_bottom", offset_x=50, offset_y=-80)
    # Находим координаты текстового блока по квадратику
    center_x, center_y = image_matcher.find_template_center("resize_handle_left_top")
    # Задаём область текста
    text_region = (center_x, center_y, 90, 16)
    after_resize_screenshot = actions.take_screenshot_with_timestamp("after")
    verifications.check_region_changed(
        after_screenshot_base,
        after_resize_screenshot,
        text_region,
        "Изменения в области canvas успешно зафиксированы: размер блока изменён.",
        "Ошибка проверки после изменения размера: "
    )

    # Перетаскивание текстового блока
    logger.info("Перетаскиваем первый текстовый блок...")
    actions.drag_object(handle_template="resize_handle_right_top", offset_x=150, offset_y=70)
    # Находим координаты текстового блока по квадратику
    center_x, center_y = image_matcher.find_template_center("resize_handle_left_top")
    # Задаём область текста
    text_region = (center_x, center_y, 90, 16)
    after_drag_screenshot = actions.take_screenshot_with_timestamp("after")
    verifications.check_region_changed(
        after_resize_screenshot,
        after_drag_screenshot,
        text_region,
        "Изменения в области canvas успешно зафиксированы: блок перетащен.",
        "Ошибка проверки после перетаскивания: "
    )
    verifications.check_region_matches_reference(
        after_drag_screenshot,
        actions.get_path("screenshots", "references", "textbox_full_reference.png"),
        text_region,
        threshold=0.95,
        success_msg="Скриншот соответствует эталонному изображению: текстовый блок увеличен и перемещён корректно."
    )

    # Закрытие приложения
    actions.close_fastreport()

    logger.info("Тест создания, изменения размера и перетаскивания текстового блока завершён.")