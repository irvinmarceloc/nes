# -*- coding: utf-8 -*-

"""
WSGI config for qdc project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/usr/local/nes-system/lib/python3.5/site-packages')

# Add the paths according to your installation
paths = ['/usr/local', '/usr/local/nes-system', '/usr/local/nes-system/nes', '/usr/local/nes-system/nes/patientregistrationsystem', '/usr/local/nes-system/nes/patientregistrationsystem/qdc',]

for path in paths:
    if path not in sys.path:
        sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qdc.settings")

# Activate virtual env
activate_env=os.path.expanduser("/usr/local/nes-system/bin/activate_this.py")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
