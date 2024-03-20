from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View

from .models import User


class SignupView(View):
    template_name = 'auth/signup.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return render(request, self.template_name, {'credentials_taken': True})

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        login(request, user)
        return redirect('/')


class LoginView(View):
    template_name = 'auth/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, self.template_name, {'invalid_credentials': True})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')
