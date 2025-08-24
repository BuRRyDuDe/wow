#!/bin/bash
set -e

# Ожидание доступности базы данных
echo "Waiting for database..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "Database is ready!"

# Выполнение миграций Django
echo "Running database migrations..."
label-studio migrate

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

# Запуск Label Studio
echo "Starting Label Studio..."
exec "$@"