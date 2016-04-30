"""
WSGI config for subject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "subject.settings")

# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()
import os  
import sys  

os.environ['PYTHON_EGG_CACHE'] = '/tmp/.python-eggs' 
path = '/var/www/workspace/subject'  
if path not in sys.path:  
    sys.path.append(path)  
os.environ['DJANGO_SETTINGS_MODULE'] = 'subject.settings'  
  
import django.core.handlers.wsgi  
application = django.core.handlers.wsgi.WSGIHandler()  