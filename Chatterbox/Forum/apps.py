from django.apps import AppConfig


class ForumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Forum'

    def ready(self):
        try:
            from .models import Category
            Category.create_default_categories()
        except:
            pass