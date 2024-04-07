# Базовый образ Python
FROM python:3.8-slim

# Устанавливаем рабочую директорию в /app
WORKDIR /app

# Копируем зависимости проекта и устанавливаем их
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Копируем исходный код проекта в контейнер
COPY audio_books_bot .

# Команда, которая будет запущена при старте контейнера
CMD ["python", "main.py"]
