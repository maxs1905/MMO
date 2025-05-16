from django.urls import path
from .views import BaseRegisterView, login_with_code_view, resend_code, confirm_code

urlpatterns = [
    path('signup/', BaseRegisterView.as_view(), name='signup'),
    path('login/code/', login_with_code_view, name='login_with_code'),
    path('resend-code/', resend_code, name='resend_code'),
    path('confirm-code/', confirm_code, name='confirm_code'),
]