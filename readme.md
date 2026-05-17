# Курсовая работа

![CI](https://github.com/joosey973/gents-telegram-bot/actions/workflows/lint.yml/badge.svg)

## Как запустить проект в dev-режиме

## Требования

Перед началом убедитесь, что у вас установлены следующие компоненты:

>- Python >= 3.9
>- pip (менеджер пакетов Python)

## Установка

1. **Клонируйте репозиторий:**

    `git clone https://github.com/joosey973/coursework-first-course.git coursework`

    Перейдите в папку с проектом

    `cd coursework`

2. **Создайте и активируйте виртуальное окружение:**

    |Linux / MacOS|Windows|
    |-------|-----|
    |`python3 -m venv venv`|`python -m venv venv`|
    |`source venv/bin/activate`|`.\venv\Scripts\activate`|

3. **Установите все зависимости из файлов:**

    *Чтобы установить зависимости, пропишите команды:*

    Prod зависимости:

    `pip install -r requirements/prod.txt`

    Dev зависимости:

    `pip install -r requirements/dev.txt`

    Test зависимости:

    `pip install -r requirements/test.txt`

4. **Созадайте файл .env в корневой папке проекта и настройте переменные окружения:**
    
    |Linux / MacOS|Windows|
    |-------|-----|
    |`cp .env.example .env`|`copy .env.example .env`|

    Не забудьте указать переменные окружения для корректной работы программы!

5. **Запустите проект:**

    |Linux / MacOS|Windows|
    |-------|-----|
    |`python3 main.py`|`python main.py`|

