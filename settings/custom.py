# Django settings for edesia project.
from os import path
from settings.common import PROJECT_PATH

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SERVE_STATIC_FILES = True

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = path.join(PROJECT_PATH, 'data/data.db')         # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

import logging
#NOTE that the directory is not created automatically!
LOG_FILE = path.join(PROJECT_PATH, 'logs/django.log')
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'

logging.basicConfig(
        level=LOG_LEVEL,
        filename=LOG_FILE,
        format=LOG_FORMAT)
