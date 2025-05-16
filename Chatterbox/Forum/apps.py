from django.apps import AppConfig


class ForumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Forum'

    def ready(self):
        from .models import Category
        categories = [
            'Танки', 'Хилы', 'ДД', 'Торговцы', 'Гилдмастеры',
            'Квестгиверы', 'Кузнецы', 'Кожевники', 'Зельевары', 'Мастера заклинаний'
        ]
        for cat in categories:
            Category.objects.get_or_create(name=cat)