"""
WSGI config for peyem project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

# Add your project directory to the sys.path
project_home = '/home/your-username/peyem_project'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable to tell django where your settings.py is
os.environ['DJANGO_SETTINGS_MODULE'] = 'peyem.settings'

# Set the PYTHONPATH
sys.path.append('/home/your-username/peyem_project')
sys.path.append('/home/your-username/peyem_project/peyem')

# Import django
import django
from django.core.wsgi import get_wsgi_application

# Initialize Django
django.setup()

# Get the WSGI application
application = get_wsgi_application()
