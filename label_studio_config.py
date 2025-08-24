import os
from label_studio.core.settings.base import *

# Основные настройки
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = ['*']

# Настройки базы данных
if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRE_NAME', 'labelstudio'),
            'USER': os.getenv('POSTGRE_USER', 'postgres'),
            'PASSWORD': os.getenv('POSTGRE_PASSWORD', 'password'),
            'HOST': os.getenv('POSTGRE_HOST', 'localhost'),
            'PORT': os.getenv('POSTGRE_PORT', '5432'),
        }
    }

# Настройки медиа файлов
MEDIA_URL = '/media/'
MEDIA_ROOT = os.getenv('LABEL_STUDIO_MEDIA_DIR', '/app/media')

# Настройки статических файлов
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Настройки безопасности
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'http://localhost:8080',
    'http://127.0.0.1:8080'
]

# Настройки CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Настройки Label Studio
LABEL_STUDIO_HOST = os.getenv('LABEL_STUDIO_HOST', '0.0.0.0')
LABEL_STUDIO_PORT = int(os.getenv('PORT', os.getenv('LABEL_STUDIO_PORT', '8080')))

# Отключение регистрации без ссылки
DISABLE_SIGNUP_WITHOUT_LINK = os.getenv('LABEL_STUDIO_DISABLE_SIGNUP_WITHOUT_LINK', 'true').lower() == 'true'

# Настройки логирования
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}