from django.apps import AppConfig

class ForumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Forum'

    def ready(self):
        from . import signals

        from .models import Category
        try:
            Category.create_default_categories()
        except:
            pass