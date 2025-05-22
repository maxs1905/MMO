from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
from .models import OneTimeCode


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email", required=True)
    first_name = forms.CharField(label="Имя", max_length=30, required=True)
    last_name = forms.CharField(label="Фамилия", max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username",
                 "first_name",
                 "last_name",
                 "email",
                 "password1",
                 "password2")

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже зарегистрирован")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='Имя')
    last_name = forms.CharField(max_length=30, label='Фамилия')

    def save(self, request):
        user = super().save(request)
        user.is_active = False
        user.save()


        code = OneTimeCode.objects.create(user=user)
        code.generate_code()
        code.send_confirmation_email()

        return user