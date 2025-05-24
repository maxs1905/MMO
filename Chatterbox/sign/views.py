from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy
from .models import OneTimeCode
from .forms import BaseRegisterForm

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    template_name = 'sign/signup.html'
    success_url = reverse_lazy('confirm_code')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()

        # Создаем и отправляем код
        code = OneTimeCode.objects.create(user=user)
        code.generate_code()
        code.send_confirmation_email()

        messages.info(self.request, 'Код подтверждения отправлен на ваш email.')
        return redirect('confirm_code')


def login_with_code_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        code_input = request.POST.get('code')

        try:
            user = User.objects.get(username=username)
            otp = OneTimeCode.objects.get(user=user)

            if otp.attempts >= 3:
                otp.delete()
                messages.error(request, 'Превышено количество попыток. Зарегистрируйтесь снова.')
                return redirect('signup')

            if otp.is_expired():
                otp.delete()
                messages.error(request, 'Код истёк. Зарегистрируйтесь снова.')
                return redirect('signup')


            if otp.code == code_input:
                user.is_active = True
                user.save()

                # Логиним пользователя
                login(request, user)
                otp.delete()

                messages.success(request, 'Регистрация завершена успешно!')
                return redirect('home')
            else:
                attempts_left = 3 - otp.increment_attempts()
                messages.error(request, f'Неверный код. Осталось попыток: {attempts_left}')

        except (User.DoesNotExist, OneTimeCode.DoesNotExist):
            messages.error(request, 'Неверное имя пользователя или код. Попробуйте снова.')

    return render(request, 'sign/login_with_code.html')


def resend_code(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username, is_active=False)
            OneTimeCode.objects.filter(user=user).delete()

            code = OneTimeCode.objects.create(user=user)
            code.generate_code()
            code.send_confirmation_email()

            messages.success(request, 'Новый код подтверждения отправлен на ваш email.')
            return redirect('login_with_code')
        except User.DoesNotExist:
            messages.error(request, 'Пользователь не найден или уже активирован.')

    return render(request, 'sign/resend_code.html')


def confirm_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            otp = OneTimeCode.objects.get(code=code)
            if not otp.is_expired():
                user = otp.user
                user.is_active = True
                user.save()

                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                otp.delete()
                return redirect('home')
            else:
                messages.error(request, 'Срок действия кода истек')
        except OneTimeCode.DoesNotExist:
            messages.error(request, 'Неверный код подтверждения')

    return render(request, 'sign/confirm_code.html')
