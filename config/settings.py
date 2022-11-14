"""Contain root settings for Django Application."""

import os
from pathlib import Path

import sentry_sdk
from django.core.management.utils import get_random_secret_key
from sentry_sdk.integrations.django import DjangoIntegration

SENTRY_DSN_1 = os.getenv("SENTRY_DSN_1", None)
SENTRY_DSN_2 = os.getenv("SENTRY_DSN_2", None)
SENTRY_SAMPLE_RATE = os.getenv("SENTRY_SAMPLE_RATE", "0.5")

if SENTRY_DSN_1 is not None and SENTRY_DSN_2 is not None:
    sentry_sdk.init(
        dsn=f"https://{SENTRY_DSN_1}.ingest.sentry.io/{SENTRY_DSN_2}",
        integrations=[DjangoIntegration()],
        traces_sample_rate=float(SENTRY_SAMPLE_RATE),
        send_default_pii=True,
    )


BASE_DIR = Path(__file__).resolve().parent.parent

SITE_ID = 1

SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())
HASHID_FIELD_SALT = os.getenv("HASHID_FIELD_SALT", get_random_secret_key())

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Application definition

INSTALLED_APPS = [
    # defaults
    "grappelli",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    # custom
    "users",
    "project",
    # third party
    "django_extensions",
    "softdelete",
    "guardian",
    "django_simple_bulma",
    "django_htmx",
    "debug_toolbar",
    "sorl.thumbnail",
    "django_celery_results",
    "django_celery_beat",
    "mptt",
    "nested_admin",
    # allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]

AUTH_USER_MODEL = "users.CustomUser"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_NAME"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "PORT": 5432,
        "HOST": os.getenv("POSTGRES_HOST"),
    }
}

# Cached Database - Redis

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://cache:6379",
    }
}

# Celery Settings

CELERY_TIMEZONE = "New Zealand"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_RESULT_BACKEND = "default"
CELERY_CACHE_BACKEND = "default"

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Authentication

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "guardian.backends.ObjectPermissionBackend",
]

ACCOUNT_FORMS = {
    "login": "users.forms.CustomLoginForm",
    "signup": "users.forms.CustomSignupForm",
    "add_email": "users.forms.CustomAddEmailForm",
    "change_password": "users.forms.CustomSetForm",
    "reset_password": "users.forms.CustomResetPasswordForm",
    "reset_password_key": "users.forms.CustomResetPasswordKeyForm",
    "disconnect": "users.forms.CustomDisconnectForm",
}

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_SESSION_REMEMBER = True

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.getenv("GOOGLE_OAUTH2_KEY", ""),
            "secret": os.getenv("GOOGLE_OAUTH2_SECRET", ""),
        },
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}


LOGIN_REDIRECT_URL = "project:index"
LOGOUT_REDIRECT_URL = "project:index"

# Email

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "send_emails"

# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "NZ"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"
STATICFILES_DIRS = (str(BASE_DIR.joinpath("static")),)
STATIC_ROOT = str(BASE_DIR.joinpath("staticfiles"))
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django_simple_bulma.finders.SimpleBulmaFinder",
]

# Media (Images)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Custom settings for django-simple-bulma

BULMA_SETTINGS = {
    "extensions": ["all"],
    "variables": {
        "primary": "hsl(0, 0%, 14%)",
    },
    "output_style": "compressed",
}

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "debug.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "propagate": True,
        },
    },
    "root": {
        "handlers": ["file"],
        "level": "WARNING",
    },
}

# Producution settings
DEBUG = False
ALLOWED_HOSTS = [
    "training.shivan.xyz",
]
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Development settings
if os.getenv("DJANGO_DEVELOPMENT", 0) == "1":
    DEBUG = True
    ALLOWED_HOSTS = ["*"]
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
    del SECURE_PROXY_SSL_HEADER
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2 ",
    ]
    LOGGING["root"]["level"] = "DEBUG"

# Email Service

# Set up sendgrid
