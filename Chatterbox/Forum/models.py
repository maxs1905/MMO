from django.db import models
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
    content = RichTextUploadingField('Содержание')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ads',
        verbose_name='Автор'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ads',
        verbose_name='Категория'
    )
    create_time = models.DateTimeField('Дата создания', auto_now_add=True)
    update_time = models.DateTimeField('Дата обновления', auto_now=True)
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

    def save(self, *args, **kwargs):
        print("Saving Ads instance...")  # Отладочный вывод
        try:
            super().save(*args, **kwargs)
            print("Ads instance saved successfully")
        except Exception as e:
            print("Error saving Ads instance:", str(e))
            raise



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
        """Отправляет уведомление автору объявления о новом отклике"""
        subject = f'Новый отклик на ваше объявление "{self.ad.title}"'
        html_message = render_to_string('new_response.html', {
            'response': self,
            'ad': self.ad,
            'site_url': settings.SITE_URL
        })
        plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [self.ad.user.email],
            html_message=html_message
        )

    def send_accept_notification(self):
        """Отправляет уведомление автору отклика о его принятии"""
        subject = f'Ваш отклик на "{self.ad.title}" принят!'
        html_message = render_to_string('response_accepted.html', {
            'response': self,
            'ad': self.ad,
            'site_url': settings.SITE_URL
        })
        plain_message = strip_tags(html_message)

        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [self.user.email],
            html_message=html_message
        )
class Newsletter(models.Model):
    subject = models.CharField('Тема', max_length=200)
    message = models.TextField('Сообщение')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    sent_at = models.DateTimeField('Дата отправки', null=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Автор'
    )

    def str(self):
        return self.subject

    def send(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        recipients = User.objects.filter(is_active=True)
        for user in recipients:
            send_mail(
                self.subject,
                self.message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        self.sent_at = timezone.now()
        self.save()