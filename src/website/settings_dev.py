from .settings_base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# silk configuration
INSTALLED_APPS.append('silk')
MIDDLEWARE.append('silk.middleware.SilkyMiddleware')
