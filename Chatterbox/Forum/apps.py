from django.apps import AppConfig


class ForumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Forum'

    def ready(self):
        # Подключаем сигналы
        from . import signals

        # Создаем категории по умолчанию
        try:
            from .models import Category
            Category.create_default_categories()
        except:
            # Игнорируем ошибки при миграциях
            pass