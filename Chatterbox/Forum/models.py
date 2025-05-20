from django.db import models
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from ckeditor.fields import RichTextField

User = get_user_model()


class Category(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    description = models.TextField('Описание', blank=True, default='')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def str(self):
        return self.name

    @classmethod
    def create_default_categories(cls):
        categories = [
            'Танки', 'Хилы', 'ДД', 'Торговцы', 'Гилдмастеры',
            'Квестгиверы', 'Кузнецы', 'Кожевники', 'Зельевары', 'Мастера заклинаний'
        ]
        for name in categories:
            cls.objects.get_or_create(
                name=name,
                defaults={'description': f'Категория для {name}'}
            )


class Ads(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    description = RichTextField('Описание')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ads',
        verbose_name='Автор'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='ads',
        verbose_name='Категория'
    )
    create_time = models.DateTimeField('Дата создания', auto_now_add=True)
    update_time = models.DateTimeField('Дата обновления', auto_now=True)
    image = models.ImageField(
        'Изображение',
        upload_to='ads_images/',
        null=True,
        blank=True
    )
    is_active = models.BooleanField('Активно', default=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-create_time']

    def str(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('ads_detail', kwargs={'pk': self.pk})


class Response(models.Model):
    ad = models.ForeignKey(
        Ads,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name='Объявление'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name='Автор отклика'
    )
    text = models.TextField('Текст отклика')
    created_time = models.DateTimeField('Дата создания', auto_now_add=True)
    is_accepted = models.BooleanField('Принято', default=False)

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
        ordering = ['-created_time']

    def str(self):
        return f'Отклик от {self.user.username} на "{self.ad.title}"'

    def send_notification(self):
        subject = f'Новый отклик на ваше объявление "{self.ad.title}"'
        message = f'''Пользователь {self.user.username} оставил отклик:

{self.text}

Просмотреть: {settings.SITE_URL}{self.ad.get_absolute_url()}
'''
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.ad.user.email],
            fail_silently=False,
        )

    def send_accept_notification(self):
        subject = f'Ваш отклик на "{self.ad.title}" принят!'
        message = f'''Ваш отклик был принят:

{self.text}

Свяжитесь с автором: {self.ad.user.email}
'''
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.user.email],
            fail_silently=False,
        )