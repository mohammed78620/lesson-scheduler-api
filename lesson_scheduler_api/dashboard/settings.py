"""
Django settings for dashboard project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
# import logging
import os
from pathlib import Path

# import django
import environ
from django.core.exceptions import ImproperlyConfigured

# import json_log_formatter

environment = environ.FileAwareEnv(
    DEBUG=(bool, True),
    SECRET_KEY=(str, "django-insecure-68g))^hu8*1eq01406e--+ujzmdalf=so_($s40v_!q3&ccg^+"),
    ALLOWED_HOSTS=(list, ""),
    DATABASE_NAME=(str, None),
    DATABASE_USER=(str, None),
    DATABASE_PASSWORD=(str, None),
    DATABASE_HOST=(str, None),
    DATABASE_PORT=(int, None),
    SERVERS=(list, [{"url": "http://localhost:8000", "description": "The lesson scheduler API"}]),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = environment("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = environment("DEBUG")

ALLOWED_HOSTS = environment.list("ALLOWED_HOSTS")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "rest_framework",
    "knox",
    "rest_auth.registration",
    "drf_spectacular",
    "django_filters",
    "corsheaders",
    "core",
    # "user",
]

DEFAULT_RENDERER_CLASSES = ("rest_framework.renderers.JSONRenderer",)

if DEBUG:
    DEFAULT_RENDERER_CLASSES = DEFAULT_RENDERER_CLASSES + ("rest_framework.renderers.BrowsableAPIRenderer",)


REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "knox.auth.TokenAuthentication",
    ],
}

AUTH_USER_MODEL = "core.User"

SERVERS = environment("SERVERS")

if DEBUG:
    SERVERS += [{"url": "http://localhost:8000"}]

# Docs: https://drf-spectacular.readthedocs.io/en/latest/settings.html
# Uncomment POSTPROCESSING_HOOKS if you need to generate an aws compliant swagger doc
SPECTACULAR_SETTINGS = {
    "TITLE": "Lesson Scheduler API",
    "DESCRIPTION": "Welcome to the Lesson Scheduler REST API documentation.",
    "VERSION": "1.0.1",
    "SERVE_INCLUDE_SCHEMA": False,
    # "AUTHENTICATION_WHITELIST": ["rest_framework.authentication.TokenAuthentication"],
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
    },
    # "POSTPROCESSING_HOOKS": ["dashboard.utils.openapi.aws_compliant_swagger"],
    "SERVERS": SERVERS,
    "SORT_OPERATIONS": False,
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.SimpleMiddleware",
]

# DOCS: https://stackoverflow.com/questions/22355540/access-control-allow-origin-in-django-app
CORS_ALLOW_HEADERS = "*"
CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = "dashboard.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "core.templates")],
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

WSGI_APPLICATION = "dashboard.wsgi.application"

DATABASE_PASSWORD = environment("DATABASE_PASSWORD")
DATABASE_USER = environment("DATABASE_USER")
DATABASE_NAME = environment("DATABASE_NAME")
DATABASE_HOST = environment("DATABASE_HOST")
DATABASE_PORT = environment("DATABASE_PORT")

if DATABASE_USER and DATABASE_PASSWORD and DATABASE_NAME and DATABASE_HOST and DATABASE_PORT:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DATABASE_NAME,
            "USER": DATABASE_USER,
            "PASSWORD": DATABASE_PASSWORD,
            "HOST": DATABASE_HOST,
            "PORT": DATABASE_PORT,
        }
    }
else:
    raise ImproperlyConfigured("You must specify a database to connect to.")

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static/"),)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# SILK
if not DEBUG:
    SILKY_PYTHON_PROFILER = True
    SILKY_AUTHENTICATION = False  # User must login
    SILKY_AUTHORISATION = False  # User must have permissions
    SILKY_ANALYZE_QUERIES = True
    SILKY_SENSITIVE_KEYS = {"username", "api", "token", "key", "secret", "password", "signature"}


# Enable extra security for production
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = "Strict"
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_HSTS_SECONDS = 300  # set low, but when site is ready for deployment, set to at least 15768000 (6 months)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
