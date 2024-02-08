from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-puglan2fzxyy0029ei6*4z3&h^=d^w$vw*4ou4#2%nso0hvs4*"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS = ["debug_toolbar"] + INSTALLED_APPS

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

INTERNAL_IPS = ("127.0.0.1", "127.17.0.1")

try:
    from .local import *
except ImportError:
    pass
