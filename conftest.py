import os
import yaml
import pytest
import pyautogui

from utils.actions import (
    setup_pyautogui,
    open_fastreport,
    create_new_report,
    create_object,
    input_text,
    resize_object,
    drag_object,
    take_screenshot_with_timestamp,
    change_z_order,
    context_menu_action,
    close_fastreport,
    fill_object
)
from utils.logger import setup_logger
from utils.image_matcher import find_template_center, click_on, double_click_on
from utils.verifications import verify_region_changed, verify_region_matches_reference, check_region_changed, check_region_matches_reference

# Класс для хранения всех действий из utils.actions
class Actions:
    def __init__(self, os_module):
        self.os = os_module
        self.pyautogui = pyautogui
        self.open_fastreport = open_fastreport
        self.create_new_report = create_new_report
        self.create_object = create_object
        self.input_text = input_text
        self.resize_object = resize_object
        self.drag_object = drag_object
        self.take_screenshot_with_timestamp = take_screenshot_with_timestamp
        self.change_z_order = change_z_order
        self.context_menu_action = context_menu_action
        self.close_fastreport = close_fastreport
        self.fill_object = fill_object

    def get_path(self, *args):
        """Формирует путь с использованием os.path.join."""
        return self.os.path.join(*args)

# Класс для хранения всех функций поиска изображений
class ImageMatcher:
    def __init__(self):
        self.find_template_center = find_template_center
        self.click_on = click_on
        self.double_click_on = double_click_on

# Класс для хранения всех функций верификации
class Verifications:
    def __init__(self):
        self.verify_region_changed = verify_region_changed
        self.verify_region_matches_reference = verify_region_matches_reference
        self.check_region_changed = check_region_changed
        self.check_region_matches_reference = check_region_matches_reference

# Настройка логгера
@pytest.fixture(scope="session")
def logger():
    """Настройка логгера для всех тестов."""
    return setup_logger(log_file=os.path.join("logs", "ui_test.log"))

# Загрузка конфигурации
@pytest.fixture(scope="session")
def config():
    """Загрузка конфигурации из data/config.yaml."""
    return yaml.safe_load(open("data/config.yaml", encoding="utf-8"))

# Создание директорий для скриншотов и настройка PyAutoGUI
@pytest.fixture(scope="function", autouse=True)
def setup_test_environment():
    """Создаёт директории для скриншотов и настраивает PyAutoGUI перед каждым тестом."""
    os.makedirs("screenshots/before", exist_ok=True)
    os.makedirs("screenshots/after", exist_ok=True)
    setup_pyautogui()

# Предоставление области canvas из конфига
@pytest.fixture(scope="function")
def canvas_region(config):
    """Возвращает область canvas из конфигурации."""
    return config.get("canvas_region", [220, 180, 720, 700])

# Фикстура для предоставления всех действий
@pytest.fixture(scope="session")
def actions():
    """Предоставляет объект с действиями из utils.actions."""
    return Actions(os)

# Фикстура для предоставления функций поиска изображений
@pytest.fixture(scope="session")
def image_matcher():
    """Предоставляет объект с функциями поиска изображений."""
    return ImageMatcher()

# Фикстура для предоставления функций верификации
@pytest.fixture(scope="session")
def verifications():
    """Предоставляет объект с функциями верификации."""
    return Verifications()