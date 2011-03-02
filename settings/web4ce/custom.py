# Django settings for edesia project.
from os import path
from settings.common import PROJECT_PATH

DEBUG = False
TEMPLATE_DEBUG = DEBUG

#If True, static files will be served by Django
SERVE_STATIC_FILES = False

ADMINS = (
     ('Karel Stastny', 'errors@edesia.cz'),
)

MANAGERS = ADMINS

SERVER_EMAIL = 'info@edesia.cz'

#email settings
EMAIL_HOST = 'mail.edesia.cz'
#EMAIL_PORT = 465
EMAIL_HOST_PASSWORD = 'lZFHJBNeYP'
EMAIL_HOST_USER = 'info@edesia.cz'
EMAIL_SUBJECT_PREFIX = '[Edesia]'
EMAIL_USE_TLS = False #with True, the sending fails


DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'edesia_cz'             # Or path to database file if using sqlite3.
DATABASE_USER = 'u6993'             # Not used with sqlite3.
DATABASE_PASSWORD = 'lZFHJBNeYP'         # Not used with sqlite3.
DATABASE_HOST = 'sql.edesia.cz'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '3306'             # Set to empty string for default. Not used with sqlite3.


ADMIN_MEDIA_PREFIX = '/site_media/admin/'


import logging
LOG_FILE = path.join(PROJECT_PATH, '../logs/django.log')
LOG_LEVEL = logging.WARN
LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'


logging.basicConfig(
        level=LOG_LEVEL,
        filename=LOG_FILE,
        format=LOG_FORMAT)

#ADS.RANKY.CZ SETTINGS
ADS_CACHE_FILE = path.join(PROJECT_PATH, '../cache/ads_ranky_cz.json')
