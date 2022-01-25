from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["litigiosos.com","localhost", "127.0.0.1"]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
        
#         'USER': 'root',
#         'NAME': 'litigiosos',
#         'PASSWORD': 'derder25',

#         #'NAME': 'consult3',
#         #'PASSWORD': 'root',
#         'HOST': 'localhost',
#         #'PORT': '8000',
#         'OPTIONS': {
#             'sql_mode': 'traditional',
#                 "init_command": "SET foreign_key_checks = 0;",
#         }
#     }
# }

THIRD_PARTY_APPS = (
    'debug_toolbar',
)

INSTALLED_APPS += THIRD_PARTY_APPS

# django debug toolbar

INTERNAL_IPS = ('127.0.0.1',)

MIDDLEWARE_CUSTOM = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

MIDDLEWARE+=MIDDLEWARE_CUSTOM

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    BASE_DIR / "static",
)

LOGIN_REDIRECT_URL = 'land'

LOGIN_URL = 'view_login'

LOGOUT_REDIRECT_URL = 'view_login'
