#!/bin/bash
set -e

# Функция для проверки доступности базы данных
wait_for_postgres() {
  echo "Waiting for database..."
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.5
  done
  echo "Database is ready!"
}

# Проверка доступности базы данных
wait_for_postgres

# Выполнение миграций Django
echo "Running database migrations..."
label-studio migrate

# Сбор статических файлов, если они еще не собраны
if [ ! -d "/app/staticfiles" ] || [ -z "$(ls -A /app/staticfiles)" ]; then
  echo "Collecting static files..."
  label-studio collectstatic --no-input
fi

# Создание суперпользователя если он не существует
echo "Creating superuser if not exists..."
label-studio shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Запуск обработчика изображений, если файл существует
if [ -f "/app/image_processor.py" ]; then
    echo "Running image processor..."
    python /app/image_processor.py
fi

# Запуск основного приложения
exec "$@"