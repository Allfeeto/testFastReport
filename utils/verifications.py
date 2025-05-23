import cv2
import numpy as np
from pathlib import Path
import logging
import pyautogui
# Получаем логгер из вызывающего модуля
logger = logging.getLogger('UITestLogger')


def verify_region_changed(screenshots, region):
    """
    Проверяет, что в указанной области между двумя скриншотами произошли изменения.

    Args:
        screenshots: Кортеж (before_path, after_path) с путями к скриншотам.
        region: Кортеж (x, y, w, h) с координатами и размером области для сравнения.

    Raises:
        AssertionError: Если изменения в области не зафиксированы.
        FileNotFoundError: Если один из скриншотов не найден.
        ValueError: Если область некорректна или изображения не удалось обработать.
    """
    before_path, after_path = screenshots
    x, y, w, h = region

    # Проверка существования файлов
    for path in (before_path, after_path):
        if not Path(path).is_file():
            logger.error(f"Файл скриншота не найден: {path}")
            raise FileNotFoundError(f"Файл скриншота не найден: {path}")

    # Чтение изображений
    try:
        img1 = cv2.imread(str(before_path))
        img2 = cv2.imread(str(after_path))

        if img1 is None or img2 is None:
            logger.error("Не удалось загрузить одно или оба изображения.")
            raise ValueError("Не удалось загрузить одно или оба изображения.")

        # Проверка, что область находится в пределах изображения
        if (x < 0 or y < 0 or x + w > img1.shape[1] or y + h > img1.shape[0] or
                x + w > img2.shape[1] or y + h > img2.shape[0]):
            logger.error(f"Некорректная область для сравнения: {region}")
            raise ValueError(f"Некорректная область для сравнения: {region}")

        # Вырезаем области интереса (ROI)
        roi1 = img1[y:y + h, x:x + w]
        roi2 = img2[y:y + h, x:x + w]

        # Проверка, что области имеют одинаковый размер
        if roi1.shape != roi2.shape:
            logger.error("Размеры областей интереса не совпадают.")
            raise ValueError("Размеры областей интереса не совпадают.")

        # Вычисляем разницу между областями
        diff = cv2.absdiff(roi1, roi2)
        mean_diff = np.mean(diff)

        # Порог для определения изменений (можно настроить)
        threshold = 5
        if mean_diff < threshold:
            logger.error(f"Изменения в области не зафиксированы (mean_diff={mean_diff:.2f} < {threshold}).")
            raise AssertionError(f"Изменения в области не зафиксированы (mean_diff={mean_diff:.2f} < {threshold}).")

        logger.info(f"Изменения в области зафиксированы (mean_diff={mean_diff:.2f}).")

    except Exception as e:
        logger.error(f"Ошибка при сравнении изображений: {e}")
        raise


def verify_region_matches_reference(screenshot_path, reference_path, region, threshold=0.95):
    """
    Проверяет, что область на скриншоте соответствует области того же размера на эталонном изображении.

    Args:
        screenshot_path: Путь к скриншоту "после" действия.
        reference_path: Путь к эталонному изображению (может быть целым скриншотом).
        region: Кортеж (x, y, w, h) с координатами и размером области для сравнения.
        threshold: Порог сходства (0-1), по умолчанию 0.95.

    Raises:
        AssertionError: Если область не соответствует эталонному изображению.
        FileNotFoundError: Если один из файлов не найден.
        ValueError: Если область некорректна или изображения не удалось обработать.
    """
    x, y, w, h = region

    # Проверка существования файлов
    for path in (screenshot_path, reference_path):
        if not Path(path).is_file():
            logger.error(f"Файл не найден: {path}")
            raise FileNotFoundError(f"Файл не найден: {path}")

    # Чтение изображений
    try:
        img = cv2.imread(str(screenshot_path))
        ref_img = cv2.imread(str(reference_path))

        if img is None or ref_img is None:
            logger.error("Не удалось загрузить одно или оба изображения.")
            raise ValueError("Не удалось загрузить одно или оба изображения.")

        # Проверка, что область находится в пределах обоих изображений
        if (x < 0 or y < 0 or x + w > img.shape[1] or y + h > img.shape[0] or
                x + w > ref_img.shape[1] or y + h > ref_img.shape[0]):
            logger.error(f"Некорректная область для сравнения: {region}")
            raise ValueError(f"Некорректная область для сравнения: {region}")

        # Вырезаем области интереса (ROI) из обоих изображений
        roi = img[y:y + h, x:x + w]
        ref_roi = ref_img[y:y + h, x:x + w]

        # Проверка, что области имеют одинаковый размер
        if roi.shape != ref_roi.shape:
            logger.error("Размеры областей интереса не совпадают.")
            raise ValueError("Размеры областей интереса не совпадают.")

        # Вычисляем разницу между областями
        diff = cv2.absdiff(roi, ref_roi)
        mean_diff = np.mean(diff)

        # Вычисляем коэффициент сходства (1 - нормированная разница)
        max_diff = 255 * 3
        similarity = 1 - (mean_diff / max_diff)

        if similarity < threshold:
            logger.error(
                f"Область не соответствует эталонному изображению (similarity={similarity:.2f} < {threshold}).")
            raise AssertionError(
                f"Область не соответствует эталонному изображению (similarity={similarity:.2f} < {threshold}).")

        logger.info(f"Область соответствует эталонному изображению (similarity={similarity:.2f} >= {threshold}).")

    except Exception as e:
        logger.error(f"Ошибка при сравнении с эталонным изображением: {e}")
        raise