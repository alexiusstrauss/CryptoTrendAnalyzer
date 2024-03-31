from .development import *

DEBUG = False

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ["*"]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Especifica os esquemas permitidos no ambiente de desenvolvimento
REST_FRAMEWORK_SCHEMAS = ["http", "https"]
