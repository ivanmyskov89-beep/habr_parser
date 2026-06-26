\# Парсинг свежих статей с Хабра



\## Описание



Скрипт парсит страницу https://habr.com/ru/articles/ и выбирает статьи, в которых встречаются ключевые слова:

\- дизайн

\- фото

\- web

\- python



\## Установка и запуск



```bash

\# Клонирование репозитория

git clone https://github.com/ivanmyskov89-beep/habr\_parser.git

cd habr\_parser



\# Создание виртуального окружения

python -m venv venv

source venv/Scripts/activate  # Windows

\# или

source venv/bin/activate      # macOS/Linux



\# Установка зависимостей

pip install -r requirements.txt



\# Запуск

python main.py

