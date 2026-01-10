import os
from django.core.management.utils import get_random_secret_key
from pathlib import Path
from decouple import config


try:
    from decouple import config
except ImportError:
    import os
    config = os.environ.get


BASE_DIR2 = Path(__file__).resolve().parent.parent.parent

DEBUG = config("DJANGO_DEBUG", cast=bool, default=False)
SECRET_KEY = config("DJANGO_SECRET_KEY", cast=str, default=get_random_secret_key())

print(DEBUG)
print(SECRET_KEY)

ALLOWED_HOSTS = [
    '.example.com',
    '.onrender.com',
    'cbesync-production.up.railway.app',
]
if DEBUG:
    ALLOWED_HOSTS+=[
        "localhost",
        "127.0.0.1",
    ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "whitenoise.runserver_nostatic", #to prevent runserver default staticfiles serving
    'django.contrib.staticfiles',
    "trial",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images) and caching for faster send and retrieval
# https://docs.djangoproject.com/en/6.0/howto/static-files/
CLOUDFLARE_R2_BUCKET=config("CLOUDFLARE_R2_BUCKET", cast=str)
CLOUDFLARE_R2_ACCESS_KEY=config("CLOUDFLARE_R2_ACCESS_KEY", cast=str)
CLOUDFLARE_R2_SECRET_KEY=config("CLOUDFLARE_R2_SECRET_KEY", cast=str)
CLOUDFLARE_R2_BUCKET_ENDPOINT=config("CLOUDFLARE_R2_BUCKET_ENDPOINT", cast=str)


CLOUD_FLARE_R2_CONFIG_OPTIONS = {
    "bucket_name": CLOUDFLARE_R2_BUCKET,
    "access_key": CLOUDFLARE_R2_ACCESS_KEY,
    "secret_key": CLOUDFLARE_R2_SECRET_KEY,
    "endpoint_url": CLOUDFLARE_R2_BUCKET_ENDPOINT,
    "default_acl": "private", #public read is also an option
    "signature_version": "s3v4",
}


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR2 / "staticfiles"
STORAGES = {
    "default": {
        "BACKEND": "helpers.cloudr2.storages.MediaFileStorage", #django-storages s[3]
        "OPTIONS": CLOUD_FLARE_R2_CONFIG_OPTIONS,
    }, #default user file fields upload
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

