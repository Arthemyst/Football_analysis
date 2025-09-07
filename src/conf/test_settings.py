import os
from .settings import *
import environ

env = environ.Env()

if os.getenv("CI"):
    SECRET_KEY = env("TEST_SECRET_KEY")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env("TEST_POSTGRES_DB"),
            'USER': env("TEST_POSTGRES_USER"),
            'PASSWORD': env("TEST_POSTGRES_PASSWORD"),
            'HOST': env("TEST_DB_HOST", "db"),
            'PORT': env("TEST_DB_PORT", "5432"),
        }
    }
    ALLOWED_HOSTS = env.list("TEST_ALLOWED_HOSTS", default=["*"])
else:
    environ.Env.read_env(".env-test")
    environ.Env.read_env(".env-db-test")

    SECRET_KEY = env("SECRET_KEY")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env("POSTGRES_DB"),
            'USER': env("POSTGRES_USER"),
            'PASSWORD': env("POSTGRES_PASSWORD"),
            'HOST': env("DB_HOST", "db"),
            'PORT': env("DB_PORT", "5432"),
        }
    }
    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
