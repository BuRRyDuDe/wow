FROM python:3.9-slim

# Установка Rust для компиляции orjson
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

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

# Установка Python зависимостей
# Install with dependency resolution backtracking disabled for faster builds
RUN pip install --no-cache-dir --no-deps -r requirements.txt || \
    pip install --no-cache-dir -r requirements.txt

# Копирование конфигурационных файлов
COPY label_studio_config.py .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Создание директорий для данных
RUN mkdir -p /app/data /app/media

# Установка переменных окружения
ENV LABEL_STUDIO_HOST=0.0.0.0
ENV LABEL_STUDIO_PORT=8080
ENV LABEL_STUDIO_DATA_DIR=/app/data
ENV LABEL_STUDIO_MEDIA_DIR=/app/media

# Открытие порта
EXPOSE 8080

# Команда запуска
ENTRYPOINT ["./entrypoint.sh"]
CMD ["label-studio", "start", "--host", "0.0.0.0", "--port", "8080", "--data-dir", "/app/data"]