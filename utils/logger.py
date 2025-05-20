import logging
import os

def setup_logger(log_file):
    """Настраивает логгер для записи в файл и консоль."""
    logger = logging.getLogger('UITestLogger')
    logger.setLevel(logging.INFO)

    # Очистка существующих обработчиков
    logger.handlers = []

    # Формат логов
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Обработчик для файла
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger