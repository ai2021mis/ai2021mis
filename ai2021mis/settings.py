"""
Django settings for ai2021mis project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fzmt-*5xw9(k276s#r8hzm1mvq72ukz9p*omp&2xc$g-^+h*aa'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*',]


# Application definition

INSTALLED_APPS = [
    'django_crontab',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'db_api',
    'linebot',
    'mylinebot',
    'employee',
    'website',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django.contrib.sites',
    'django_celery_results',
    'dbbackup',
    

]

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': BASE_DIR/ 'backup'}

#activate this.. then backup will automatically run every 1 minut 
# CRONJOBS = [
#     ('*/1 * * * *', 'ai2021mis.cron.backup_function')
# ]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ai2021mis.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'ai2021mis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CACHES = {
    "default": {
        # 預設使用
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1", # 指定redis://IP/第幾個DB
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        'KEY_PREFIX': 'Cache'
    },
    # 其他redis庫
    "testRedis": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        'KEY_PREFIX': 'Cache'
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# to disable the check
DATA_UPLOAD_MAX_NUMBER_FIELDS = None

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'nchutamtam@gmail.com'
EMAIL_HOST_PASSWORD = 'tamtexuievan'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
#DEFAULT_FROM_EMAIL = 'cscheng5282@smail.nchu.edu.tw'
RECIPIENT_ADDRESS = 'wiratamawidarto@gmail.com'


WEB_HOST = 'https://933e-223-141-32-22.ngrok.io'
LINE_CHANNEL_ACCESS_TOKEN = 'sRRx49jYLQL+JbvGmq9s8CkvelMEJMexixUGnUJD77Nje9aW6Nf3jf4jGQ7zNrTM1tk0UBVsPc5Ezm4zrU7q8ZHoRI6kHkcxu4dADMmLjKcmQETiUVe1ov0G44yMTbzwVwrKd8JjI8lJjRJ4R5H2LgdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'dc642785c53e406cdcc72ec324aa6ca8'
LINE_CHANNEL_ID = '@224zbfei'

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us' #'zh-hant'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = False

USE_TZ = True

# DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'

# Celery
BROKER_URL = 'redis://localhost:6379/'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_TIME_LIMIT = 60      # 為任務設定超時時間，單位秒。超時即中止，執行下個任務。
# CELERY_RESULT_EXPIRES = xx    # 為儲存結果設定過期日期，預設1天過期。如果beat開啟，Celery每天會自動清除。設為0，儲存結果永不過期
# CELERY_TASK_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}}   # 任務限流
# CELERY_WORKER_CONCURRENCY = 2     # Worker並行數量，一般預設CPU核數，可以不設定
# CELERY_WORKER_MAX_TASKS_PER_CHILD = 200  # 每個worker執行了多少任務就會死掉，預設是無限的
# CELERY_TASK_DEFAULT_QUEUE = 'default'
# CELERY_TASK_DEFAULT_ROUTING_KEY = 'default'
# CELERY_QUEUES = (
# Queue('default', Exchange('default'), routing_key='default'),
# Queue('heavy_tasks', Exchange('heavy_tasks'), routing_key='heavy_tasks'),
# )
# CELERY_TASK_ROUTES = {
# 'myapp.tasks.heave_tasks': 'heavy_tasks'
# }


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = '/home/christopher0908/ai2021mis/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
