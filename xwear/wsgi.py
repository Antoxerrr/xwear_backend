import os
import sys

from django.core.wsgi import get_wsgi_application

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(CURRENT_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xwear.settings')

application = get_wsgi_application()
