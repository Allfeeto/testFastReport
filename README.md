# testFastReport

# Структура проекта

```
testFastReport/
│
├── tests/                     # 📂 Основные UI-тесты (по функциям и сценариям)
│   ├── test_insert_textbox.py
│   ├── test_insert_shape.py
│   ├── test_insert_image.py
│   ├── test_change_properties.py
│   ├── test_drag_object.py
│   └── ...
│
├── utils/                     # 📂 Вспомогательные модули
│   ├── logger.py              # Логирование в файл + консоль
│   ├── images.py              # Работа со скриншотами
│   ├── image_matcher.py       # Поиск и клики по шаблонам
│   ├── verifications.py       # Проверки "до/после" и сравнение с эталоном
│   ├── actions.py             # Новая утилита для общих действий (открытие, создание объектов, ввод текста и т.д.)
│   └── coordinates.py         # Новая утилита для загрузки и управления координатами
│
├── data/                      # 📂 Данные для тестов
│   ├── coordinates.json       # Координаты элементов UI
│   ├── config.yaml            # Конфиги: паузы, разрешения, путь до exe и т.д.
│   └── templates/             # Шаблоны изображений для image_matcher
│
├── screenshots/               # 📂 Все скрины
│   ├── before/                # 📂 До действия
│   ├── after/                 # 📂 После действия
│   └── references/            # 📂 Эталонные скрины
│
├── logs/                      # 📂 Лог-файлы
│   └── ui_test.log
│
├── conftest.py                # Общие фикстуры для pytest
├── requirements.txt           # Зависимости проекта
└── README.md                  # Краткое описание и инструкция
```

