import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')

def pytest_configure():
    if not settings.configured:
        django.setup()