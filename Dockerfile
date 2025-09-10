FROM python:3.9-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-traditional \
    libwebp-dev \
    libjpeg-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY requirements.txt .

# Upgrade pip and install build tools
RUN pip install --upgrade pip setuptools wheel

# Установка Python зависимостей с оптимизацией
RUN pip install --no-cache-dir -r requirements.txt

# Копирование конфигурационных файлов
COPY label_studio_config.py .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Копирование остальных файлов
COPY . .

# Создание директорий для данных
RUN mkdir -p /app/data /app/media /app/staticfiles

# Сбор статических файлов
RUN python -m label_studio collectstatic --no-input

# Установка переменных окружения
ENV LABEL_STUDIO_HOST=0.0.0.0
ENV LABEL_STUDIO_PORT=8080
ENV LABEL_STUDIO_DATA_DIR=/app/data
ENV LABEL_STUDIO_MEDIA_DIR=/app/media
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Открытие порта
EXPOSE 8080

# Команда запуска
ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--threads", "2", "--timeout", "120", "--keep-alive", "5", "--max-requests", "1000", "--max-requests-jitter", "50", "label_studio.wsgi:application"]