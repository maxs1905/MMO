from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView
from  . import views


urlpatterns = [
    path('signup/',
         BaseRegisterView.as_view(template_name = 'sign/signup.html'),
         name='signup'),
]