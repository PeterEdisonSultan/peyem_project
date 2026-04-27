"""
Production settings for Peyem project on PythonAnywhere.
Copy this file to peyem/settings_production.py and update the ALLOWED_HOSTS and other settings.
"""

from .settings import *

# Production settings
DEBUG = False

# Replace 'your-username' with your actual PythonAnywhere username
ALLOWED_HOSTS = [
    'your-username.pythonanywhere.com',
    'www.your-username.pythonanywhere.com',
]

# Security settings
SECRET_KEY = 'your-secure-secret-key-here-change-this-in-production'

# CORS settings for production
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    f"https://your-username.pythonanywhere.com",
    f"https://www.your-username.pythonanywhere.com",
]

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    f"https://your-username.pythonanywhere.com",
    f"https://www.your-username.pythonanywhere.com",
]

# Database (using SQLite for simplicity, consider PostgreSQL for production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (if needed)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Email settings (configure for production)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django_error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}