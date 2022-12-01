from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView

from authapp.models import User


# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'authapp/login.html'
    extra_context = {
        'title': 'Вход пользователя'
    }

    def form_valid(self, form):
        ret = super().form_valid(form)

        message = "Login success!<br>Hi, %(username)s" % {
            "username": self.request.user.get_full_name()
            if self.request.user.get_full_name()
            else self.request.user.get_username()
        }
        messages.add_message(self.request, messages.INFO, mark_safe(message))
        return ret


class RegisterView(TemplateView):
    template_name = 'authapp/register.html'

    extra_context = {
        'title': 'Регистрация пользователя'
    }

    def post(self, request, *args, **kwargs):
        try:
            if all(
                    (
                        request.POST.get('username'),
                        request.POST.get('password1'),
                        request.POST.get('password2'),
                        request.POST.get('first_name'),
                        request.POST.get('password1') == request.POST.get('password2'),
                    )
            ):
                new_user = User.objects.create(
                    username=request.POST.get('username'),
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    email=request.POST.get('email'),
                    age=request.POST.get('age') if request.POST.get('age') else 0,
                    avatar=request.FILES.get('avatar')
                )
                new_user.set_password(request.POST.get('password1'))
                new_user.save()
                messages.add_message(request, messages.INFO, 'Регистрация прошла успешно')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                messages.add_message(request, messages.WARNING, 'Что-то пошло не так')
                return HttpResponseRedirect(reverse('authapp:register'))
        except Exception as ex:
            messages.add_message(request, messages.WARNING, mark_safe(f'Что-то пошло не так:<br>{ex}'))
            return HttpResponseRedirect(reverse('authapp:register'))


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.INFO, "See you later!")
        return super().dispatch(request, *args, **kwargs)


class EditView(LoginRequiredMixin, TemplateView):
    template_name = 'authapp/edit.html'

    extra_context = {
        'title': 'Регистрация пользователя'
    }

    def post(self, request, *args, **kwargs):
        if request.POST.get('username'):
            request.user.username = request.POST.get('username')

        if request.POST.get('first_name'):
            request.user.first_name = request.POST.get('first_name')

        if request.POST.get('last_name'):
            request.user.last_name = request.POST.get('last_name')

        if request.POST.get('age'):
            request.user.age = request.POST.get('age')

        if request.POST.get('email'):
            request.user.email = request.POST.get('email')

        if request.POST.get('password'):
            request.user.set_password(request.POST.get('password'))

        request.user.save()
        return HttpResponseRedirect(reverse('authapp:edit'))
