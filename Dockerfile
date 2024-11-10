FROM python:3.10-slim

WORKDIR /app

# Установка необходимых системных пакетов
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов requirements и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование остальных файлов проекта
COPY . .

# Запуск бота
CMD ["python", "weather_bot.py"]