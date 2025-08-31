import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        """App is ready. DO NOT put database operations here."""
        # EMPTY - no database operations during startup
        pass