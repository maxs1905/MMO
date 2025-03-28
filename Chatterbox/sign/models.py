from django.db import models
from django.utils import timezone
from datetime import timedelta
import random
import string
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )

class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user


# Форма для ввода одноразового кода
class OneTimeCodeForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=100)
    code = forms.CharField(label='Код подтверждения', max_length=8)
class OneTimeCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def generate_code(self):
        """Генерация случайного одноразового кода"""
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))  # 8-значный код
        self.code = code
        self.expired_at = timezone.now() + timedelta(minutes=10)  # Код действует 10 минут
        self.save()
        return code

    def is_expired(self):
        """Проверка истечения срока действия кода"""
        return timezone.now() > self.expired_at

    def __str__(self):
        return f"Код для {self.user.username}: {self.code}"