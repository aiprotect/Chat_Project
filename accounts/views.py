import requests
from cloudinit.sources.DataSourceOVF import read_ovf_environment
from django.conf import settings
from django.contrib.auth import get_user, login, logout
from django.shortcuts import render, redirect,reverse
from django.views import View
from django.http import HttpRequest
from accounts.forms import LoginForm, RegisterForm
from accounts.models import User

class RegisterView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            form = RegisterForm
            return render(request, 'accounts/register_page.html', {'form' : form})
        else:
            return redirect(reverse('index-name'))

    def post(self, requests):
        if not requests.user.is_authenticated:
            form = RegisterForm(requests.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse('login-name'))
            return render(requests, 'accounts/register_page.html', {'form' : form})
        else:
            return redirect(reverse('login-name'))


class LoginView(View):
    def get(self, request: HttpRequest):
        if not request.user.is_authenticated:
            form = LoginForm()
            context = {
                'form': form,
                'HCAPTCHA_SITEKEY': settings.HCAPTCHA_SITEKEY
            }
            return render(request, 'accounts/login_page.html', context)
        else:
            return redirect(reverse('index-name'))

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)

        # اعتبارسنجی hCaptcha
        hcaptcha_response = request.POST.get('h-captcha-response')
        if hcaptcha_response:
            data = {
                'secret': settings.HCAPTCHA_SECRET,
                'response': hcaptcha_response
            }
            response = requests.post('https://hcaptcha.com/siteverify', data=data)
            result = response.json()
            if not result['success']:
                login_form.add_error(None, 'لطفاً تأیید کنید که ربات نیستید.')

        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email_or_username')
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()

            if user is not None:
                if not user.is_active:
                    login_form.add_error('email_or_username', 'حساب کاربری شما فعال نشده است')
                else:
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('index-name'))
                    else:
                        login_form.add_error('email_or_username', 'کلمه عبور اشتباه است')
            else:
                login_form.add_error('email_or_username', 'کاربری با مشخصات وارد شده یافت نشد')

        context = {
            'form': login_form,
            'HCAPTCHA_SITEKEY': settings.HCAPTCHA_SITEKEY
        }
        return render(request, 'accounts/login_page.html', context)
class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect(reverse('index-name'))
        else:
            return redirect(reverse('login-name'))