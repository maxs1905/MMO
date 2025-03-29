from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from .models import OneTimeCode
from .models import BaseRegisterForm
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    template_name = 'sign/signup.html'
    success_url = reverse_lazy('login_with_code')
    def usual_login_view(request):
        username = request.POST["username"]
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            otp_code_obj = OneTimeCode.objects.create(user=user)
            otp_code = otp_code_obj.generate_code()
            send_mail(
                'Ваш одноразовый код для подтверждения',
                f'Ваш одноразовый код для подтверждения: {otp_code}',
                'Maxs.defmail@yandex.com',
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Проверьте вашу почту для одноразового кода.')
            return redirect('login_with_code')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
            return redirect('usual_login_view')
    def login_with_code(request):

        username = request.POST['username']
        code = request.POST['code']
        try:
            otp_code_obj = OneTimeCode.objects.get(code=code, user__username=username)
            if otp_code_obj.is_expired():
              messages.error(request, 'Код истек. Попробуйте снова.')
              return redirect('login_with_code')

            login(request, otp_code_obj.user)
            otp_code_obj.delete()
            return redirect('home')

        except OneTimeCode.DoesNotExist:
            messages.error(request, 'Неверный код. Попробуйте снова.')
            return redirect('login_with_code')