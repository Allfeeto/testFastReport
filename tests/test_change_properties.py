import pyautogui
import time

def test_create_report():
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5

    print("Запускаем FastReport...")
    pyautogui.hotkey('win', 'r')
    pyautogui.write(r"C:\Program Files (x86)\Fast Reports\.NET\2025.2.3\FastReport .NET WinForms Pack Trial\Designer.exe")
    pyautogui.press('enter')
    time.sleep(5)

    print("Нажимаем кнопку 'OK' в начальном окне...")
    pyautogui.click(x=990, y=595)
    time.sleep(1)

    print("Создаём новый отчёт...")
    pyautogui.doubleClick(x=1040, y=460)
    time.sleep(1)

    print("Тест создания нового отчёта завершён.")