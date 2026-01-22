import os, ast
from django.core.management.utils import get_random_secret_key
from pathlib import Path
from decouple import config
from django.utils.csp import CSP


try:
    from decouple import config
except ImportError:
    import os
    config = os.environ.get

BASE_DIR2 = Path(__file__).resolve().parent.parent.parent

DEBUG = config("DJANGO_DEBUG", cast=bool, default=False)
SECRET_KEY = config("DJANGO_SECRET_KEY", cast=str, default=get_random_secret_key())


ALLOWED_HOSTS=[]

if DEBUG:
    ALLOWED_HOSTS += [
        "127.0.0.1",
        "localhost",
    ]
    CSRF_TRUSTED_ORIGINS = [
        'http://localhost', 'http://127.0.0.1',  # local host management
    ]

if not DEBUG:
    allowed_hosts_env = config("DJANGO_ALLOWED_HOSTS", default=[])
    ALLOWED_HOSTS = ast.literal_eval(allowed_hosts_env)
    #csrf forms setup to avoid csrf token erros
    allowed_csrf_origin = [f"https://{domain}" for domain in ALLOWED_HOSTS]
    CSRF_TRUSTED_ORIGINS = allowed_csrf_origin
    print(f"{ALLOWED_HOSTS}\n{allowed_csrf_origin}")
    # Ensure cookies are only sent over HTTPS
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

    # Prevent client-side JS access to cookies
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_HTTPONLY = True

    # Optional but helps with modern browsers
    CSRF_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SAMESITE = 'Lax'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "whitenoise.runserver_nostatic", #to prevent runserver default staticfiles serving
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    #thirdparty
    "allauth_ui",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "widget_tweaks",
    "slippers",
    "phonenumber_field",
    # "tailwind",
    # "theme",
    #custom project apps
    "accounts",
    "trial",
    "schools",
    "students",
    "teachers",
]
ALLAUTH_UI_THEME = "forest"
# TAILWIND_APP_NAME = "theme"
# ALLAUTH_UI_USE_TAILWIND = False


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    "django.contrib.auth.middleware.LoginRequiredMiddleware", #login required everywhere
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
    "django.middleware.csp.ContentSecurityPolicyMiddleware", #for csp

]

SECURE_CSP = {
    "default-src": [CSP.SELF],
    "script-src": [
        CSP.SELF,
        CSP.NONCE,
        "https://static.cloudflareinsights.com/"
    ],
    "style-src": [
        CSP.SELF,
        "https://fonts.googleapis.com",
        "https://unpkg.com",
         CSP.UNSAFE_INLINE,
    ],
    "font-src": [
        CSP.SELF,
        "https://fonts.gstatic.com",
        "https://unpkg.com",   
    ],
    "img-src": [
        CSP.SELF,

    ]
}

ROOT_URLCONF = 'project.urls'

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

AUTH_USER_MODEL = "accounts.CustomUser"
PHONENUMBER_DB_FORMAT = "INTERNATIONAL"
PHONENUMBER_DEFAULT_FORMAT = "INTERNATIONAL"
