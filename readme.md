# Курсовая работа

[![CI](https://github.com/joosey973/coursework-first-course/actions/workflows/lint.yml/badge.svg)](https://github.com/joosey973/coursework-first-course/actions/workflows/lint.yml)
![Python](https://img.shields.io/badge/Python-3.9%2B-pink)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)

Десктопное учебное приложение на Python с графическим интерфейсом (Tkinter). Реализует обучающий курс по высшей математике с поддержкой светлой и тёмной темы оформления.

---

## Возможности

- Графический интерфейс на основе Tkinter
- Разделы курса с теоретическим и визуальным материалом (изображения интегралов)
- Диалоговые окна для взаимодействия с пользователем
- Поддержка светлой и тёмной цветовой темы, настраиваемой через переменные окружения
- CI-проверка кода через GitHub Actions

---

## Структура проекта

```
.
├── main.py                  # Точка входа
├── config.py                # Конфигурация цветовых тем и переменных окружения
├── settings.py              # Настройки приложения
├── auxiliaryClasses/        # Вспомогательные классы (меню и пр.)
├── courseThemes/            # Модули тематических разделов курса
├── dialogs/                 # Диалоговые окна
├── media/integrals/         # Медиафайлы (изображения)
├── configs/                 # Дополнительные конфигурации
├── requirements/
│   ├── prod.txt             # Продакшн-зависимости
│   ├── dev.txt              # Dev-зависимости
│   └── test.txt             # Тестовые зависимости
├── .env.example             # Пример файла переменных окружения
└── .github/workflows/       # CI/CD пайплайны
```

---

## Требования

- Python >= 3.9
- pip

---

## Установка и запуск

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/joosey973/coursework-first-course.git coursework
cd coursework
```

### 2. Создайте и активируйте виртуальное окружение

| Linux / macOS | Windows |
|---|---|
| `python3 -m venv venv` | `python -m venv venv` |
| `source venv/bin/activate` | `.\venv\Scripts\activate` |

### 3. Установите зависимости

```bash
# Продакшн-зависимости
pip install -r requirements/prod.txt

# Dev-зависимости (для разработки)
pip install -r requirements/dev.txt

# Тестовые зависимости
pip install -r requirements/test.txt
```

### 4. Настройте переменные окружения

| Linux / macOS | Windows |
|---|---|
| `cp .env.example .env` | `copy .env.example .env` |

Откройте `.env` (`nano .env` или через графический интерфейс) и заполните переменные:

```env
# Путь к папке с медиафайлами
MEDIA_ROOT=media/integrals/

# Цветовая тема: "black" (тёмная) или "white" (светлая)
COLOR_THEME=black
```

### 5. Запустите приложение

| Linux / macOS | Windows |
|---|---|
| `python3 main.py` | `python main.py` |

---

## Цветовые темы

Тема задаётся переменной окружения `COLOR_THEME` в файле `.env`.

| Значение | Описание |
|---|---|
| `black` | Тёмная тема (по умолчанию) |
| `white` | Светлая тема |

---

## Разработка

Для начала скопируйте файлы настроек в директорию проекта:
```bash
# Копия настроек для flake8
cp configs/.flake8 .flake8

# Копия настроек для isort
cp configs/.isort.cfg .isort.cfg

# Копия настроек для black
cp configs/pyproject.toml pyproject.toml
```

Перед коммитом убедитесь, что код проходит линтер:

```bash
# Установите dev-зависимости, если ещё не сделали
pip install -r requirements/dev.txt

# Запустите проверку
flake8 --verobose .
isort --check .
black --check .
```

CI автоматически запускается при каждом push через GitHub Actions.

---

## Авторы

- [@joosey973](https://github.com/joosey973)
