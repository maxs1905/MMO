from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
import string
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


class OneTimeCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    attempts = models.PositiveSmallIntegerField(default=0)

    def str(self):
        return f"{self.user.username}: {self.code}"

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=15)

    def generate_code(self):
        self.code = ''.join(random.choices(string.digits, k=6))
        self.save()
        return self.code

    def send_confirmation_email(self):
        send_mail(
            'Код подтверждения для MMORPG',
            f'Ваш код подтверждения: {self.code}\n\n'
            f'Введите его на странице: {settings.SITE_URL}/sign/confirm-code/',
            settings.DEFAULT_FROM_EMAIL,
            [self.user.email],
            fail_silently=False,
        )

    def increment_attempts(self):
        self.attempts += 1
        self.save()
        return self.attempts