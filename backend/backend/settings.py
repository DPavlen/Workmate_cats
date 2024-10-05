import os
from datetime import timedelta
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


# sqlite3 или postgresql
DB_ENGINE = os.getenv("DB_ENGINE", "sqlite3")

SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(" ")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "djoser",

    "drf_spectacular",
    "drf_spectacular_sidecar",
    "django_filters",

    # "api.apps.ApiConfig",
    "cats.apps.CatsConfig",
    "users.apps.UsersConfig",
    "colorfield"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "querycount.middleware.QueryCountMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "backend.wsgi.application"

# --------------------------------------------
#     Подключение к БД sqlite3 или postgresql
# --------------------------------------------
if DB_ENGINE == "sqlite3":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

if DB_ENGINE == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", default="django"),
            "USER": os.getenv("POSTGRES_USER", default="django_user"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", default="django"),
            "HOST": os.getenv("DB_HOST", default="db"),
            "PORT": os.getenv("DB_PORT", default=5432),
        }
    }


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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# --------------------------------------------
#    Настройка Статики и Медиа backenda
# --------------------------------------------
STATIC_URL = "/backend_static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "/backend_media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.CustUser"

# --------------------------------------------
#    Настройка REST_FRAMEWORK
# --------------------------------------------
REST_FRAMEWORK = {
    "DATETIME_FORMAT": "%d.%m.%Y %H:%M:%S",

    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",

    "DATE_INPUT_FORMATS": ["%d.%m.%Y"],
    # "DEFAULT_PAGINATION_CLASS":
    #     "rest_framework.pagination.LimitOffsetPagination",
    # "PAGE_SIZE": int(os.getenv("PAGE_SIZE", 10)),
}

# --------------------------------------------
#    Настройка SIMPLE_JWT
#    Когда Access токен истекает, Refresh-токен
#    его реанимирует и сам умирает
# --------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=4),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# --------------------------------------------
#    Настройка DJOSER
# --------------------------------------------
DJOSER = {
    "SERIALIZERS": {
        "user_create": "users.serializers.CustomUserSerializer",
        "user": "users.serializers.CustomUserSerializer",
        # "current_user": "users.serializers.CustomUserSerializer",
        # "token_destroy": "users.serializers.CustomTokenDestroySerializer",
    },
    "PERMISSIONS": {
        "user": ["djoser.permissions.CurrentUserOrAdminOrReadOnly"],
        "user_list": ["rest_framework.permissions.IsAuthenticatedOrReadOnly"],
    },
}
HIDE_USERS = True

# ------------------------------------------------
#    Настройка SPECTACULAR_SETTINGS для SWAGGERA
# ------------------------------------------------
SPECTACULAR_SETTINGS = {
    "TITLE": "Workmate_cats",
    "VERSION": "1.0.0",
    "DESCRIPTION": "Workmate_cats: Backend",
    "CONTACT": {
        "name": "Workmate_cats",
        "url": "https://github.com/DPavlen/Workmate_cats",
        "email": "jobpavlenko@yandex.ru",
    },
    "COMPONENT_SPLIT_REQUEST": True,
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_COERCE_PATH_PK_SUFFIX": True,
    "SORT_OPERATIONS": True,
    "SCHEMA_PATH_PREFIX": r"/api/",
}

# ------------------------------------------------
#    Настройка Логирования только ошибок
# ------------------------------------------------
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "console": {
#             "level": "ERROR",
#             "class": "logging.StreamHandler",
#         },
#         "file": {
#             "level": "ERROR",
#             "class": "logging.FileHandler",
#             "filename": "error.log",
#         },
#     },
#     "loggers": {
#         "django.db.backends": {
#             "handlers": ["console", "file"],
#             "level": "ERROR",
#         },
#     },
# }
