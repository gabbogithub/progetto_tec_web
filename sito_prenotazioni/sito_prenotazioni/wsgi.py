import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sito_prenotazioni.settings')

application = get_wsgi_application()
