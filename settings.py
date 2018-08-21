# -*- coding: utf-8 -*-
# minimize django settings
from __future__ import unicode_literals
import django


SECRET_KEY = b"0123456789"

DATABASES = {
    'default' : {
        "ENGINE" : 'django.db.backends.sqlite3',
        "NAME": 'sqlite.db',
    }
}

INSTALLED_APPS = (
    'ormapp',
)

try:
    django.setup()
except AttributeError:
    pass
