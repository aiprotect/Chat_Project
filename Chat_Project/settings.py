"""
Django settings for Chat_Project project.
"""

from pathlib import Path
from django.utils.translation import gettext_lazy as _
import os

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-6zcd*82%j*_eg8pcitr$g5)!p7qwe)5417l^3&4%kvzl=ycpig')

# Debug settings
DEBUG = True  # در محیط تولید باید False باشد
DEVELOPMENT_MODE = os.getenv('DEVELOPMENT_MODE', 'False') == 'True'

# Security headers
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_SSL_REDIRECT = not DEVELOPMENT_MODE
# SESSION_COOKIE_SECURE = not DEVELOPMENT_MODE
# CSRF_COOKIE_SECURE = not DEVELOPMENT_MODE
# X_FRAME_OPTIONS = 'DENY'
# SECURE_HSTS_SECONDS = 31536000 if not DEVELOPMENT_MODE else 0
# SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEVELOPMENT_MODE
# SECURE_HSTS_PRELOAD = not DEVELOPMENT_MODE
# SECURE_REFERRER_POLICY = 'same-origin'

# Host settings
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '0.0.0.0',
    '[::1]',
    'yourdomain.com',  # جایگزین با دامنه واقعی
    'www.yourdomain.com',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.direction',  # پردازشگر سفارشی شما
            ],
            'builtins': [
                'django.templatetags.static',  # برای تگ static
            ],
        },
    },
]


# برای محیط توسعه
if DEVELOPMENT_MODE:
    DEBUG = True
    ALLOWED_HOSTS.extend(['*'])
    INTERNAL_IPS = ['127.0.0.1']
    SECURITY_STRICT_HOST_CHECK = False
    SECURITY_BLOCK_PRIVATE_IPS = False
    SECURITY_BLOCK_LOCALHOST = False
else:
    SECURITY_STRICT_HOST_CHECK = True
    ENABLE_DNS_VALIDATION = True

# Application definition
INSTALLED_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chat',
    'accounts',
    'index',
    'core',
    'security_app',
    'hcaptcha'
]

# زبان‌های راست‌به‌چپ (RTL)
RTL_LANGUAGES = ['fa', 'ar', 'he']  # کد زبان‌های فارسی، عربی، عبری

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # برای فایل‌های استاتیک
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'security_app.logging_middleware.AdvancedMonitoringMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'security_app.super_middleware.AdvancedSecurityMiddleware',
    # 'security_app.super_middleware.AdvancedAuthMiddleware',
    # 'security_app.super_middleware.RequestLoggingMiddleware',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydb',
        'USER': 'shayan',
        'PASSWORD': 'shayan.2020@AIprotect',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}




# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
ROOT_URLCONF = 'Chat_Project.urls'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings
# SECURITY_ALLOWED_IPS = [
#     '192.168.1.0/24',
#     '10.0.0.0/8',
#     '127.0.0.1'
# ]

# MALICIOUS_USER_AGENTS = [
#     'nmap', 'sqlmap', 'metasploit', 'nikto',
#     'w3af', 'owasp', 'dirbuster', 'hydra'
# ]
#

# Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.getenv('REDIS_HOST', '127.0.0.1'), 6379)],
        },
    # } if not DEVELOPMENT_MODE else {
    #     "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

GEOIP_PATH = '/usr/share/GeoIP'  # مسیر دایرکتوری حاوی فایل
GEOIP_CITY = 'GeoLite2-City.mmdb'  #

# settings.py
# تنظیمات لاگینگ پیشرفته
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '''
                asctime: %(asctime)s
                levelname: %(levelname)s
                name: %(name)s
                message: %(message)s
                pathname: %(pathname)s
                lineno: %(lineno)d
            ''',
        },
    },
    'handlers': {
        'security_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'security_app/security.log',
            'when': 'midnight',
            'backupCount': 30,
            'formatter': 'json',
            'encoding': 'utf-8',
        },
        'security_console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['security_file', 'security_console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

HCAPTCHA_SITEKEY = '10000000-ffff-ffff-ffff-000000000001'  # کلید تستی
HCAPTCHA_SECRET = '0x0000000000000000000000000000000000000000'  # کلید تستی

# Custom settings
AUTH_USER_MODEL = 'accounts.User'
ASGI_APPLICATION = 'Chat_Project.asgi.application'
WSGI_APPLICATION = 'Chat_Project.wsgi.application'

CSP_ENABLED = False  #
