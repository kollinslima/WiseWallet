from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = "authentication/signup.html"
    success_url = reverse_lazy('authentication:index')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard:index'))
        return super().get(request, *args, **kwargs)

class LogoutView(LogoutView):
    template_name = "authentication/logout.html"

class LoginView(LoginView):
    template_name = "authentication/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard:index'))
        return super().get(request, *args, **kwargs)


