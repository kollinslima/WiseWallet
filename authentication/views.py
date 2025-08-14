from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = "authentication/signup.html"
    success_url = reverse_lazy('authentication:index')

class LogoutView(LogoutView):
    template_name = "authentication/logout.html"

class LoginView(LoginView):
    template_name = "authentication/login.html"


