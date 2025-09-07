from .settings import *
import environ

env = environ.Env()

DATABASES = {
    "default": env.db(
        "DATABASE_URL_TEST",
        default="postgres://test_user:test_pass@localhost:5432/test_db"
    )
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}
