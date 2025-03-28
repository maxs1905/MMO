from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from django.contrib import messages
from django.core.mail import send_mail
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import OneTimeCode
from .models import BaseRegisterForm, OneTimeCodeForm

# Представление для регистрации
class BaseRegisterView(CreateView):
    model = get_user_model()
    form_class = BaseRegisterForm
    template_name = 'sign/signup.html'
    success_url = reverse_lazy('login_with_code')  # После регистрации перенаправляем на страницу ввода кода

    def form_valid(self, form):
        # Сохраняем пользователя
        response = super().form_valid(form)

        # Генерация одноразового кода
        user = self.object
        otp_code_obj = OneTimeCode.objects.create(user=user)
        otp_code = otp_code_obj.generate_code()

        # Отправка одноразового кода на email
        send_mail(
            'Ваш одноразовый код для подтверждения',
            f'Ваш одноразовый код для подтверждения: {otp_code}',
            'no-reply@yourdomain.com',
            [user.email],
            fail_silently=False,
        )

        # Сообщение о том, что код отправлен
        messages.success(self.request, 'Проверьте вашу почту для одноразового кода.')

        return response


# Представление для ввода одноразового кода
def login_with_code(request):
    if request.method == 'POST':
        form = OneTimeCodeForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            code = form.cleaned_data['code']

            try:
                # Получаем одноразовый код для пользователя
                otp_code_obj = OneTimeCode.objects.get(code=code, user__username=username)

                # Проверяем, не истек ли код
                if otp_code_obj.is_expired():
                    messages.error(request, 'Код истек. Попробуйте снова.')
                    return redirect('login_with_code')

                # Вход пользователя
                login(request, otp_code_obj.user)

                # Удаляем использованный код
                otp_code_obj.delete()

                # Перенаправляем на главную страницу (или любую другую)
                return redirect('home')

            except OneTimeCode.DoesNotExist:
                messages.error(request, 'Неверный код. Попробуйте снова.')

    else:
        form = OneTimeCodeForm()

    return render(request, 'sign/login_with_code.html', {'form': form})