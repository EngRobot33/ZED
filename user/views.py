from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.views import View

from .models import User


class SignupView(View):
    template_name = 'auth/signup.html'

    def get(self, request):
        request.session.pop('user_email', None)
        request.session.pop('user_username', None)
        request.session.pop('user_logged_in', None)

        data = {
            'invalid_credentials': False,
            'credentials_taken': False,
            'contains_space_in_credentials': False,
        }
        return render(request, self.template_name, data)

    def post(self, request):
        invalid_credentials = False
        credentials_taken = False

        email = request.POST.get('email')
        password = request.POST.get('password')
        password_again = request.POST.get('password_again')
        username = request.POST.get('username')

        contains_space_in_credentials = any(char.isspace() for char in (email + password + username))

        if not contains_space_in_credentials:
            if not all(request.POST.get(field) for field in ['email', 'password', 'password_again', 'username']):
                invalid_credentials = True
            else:
                if username == password or password != password_again:
                    invalid_credentials = True
                else:
                    try:
                        existing_username = User.objects.get(username=username)
                    except ObjectDoesNotExist:
                        existing_username = None

                    try:
                        existing_email = User.objects.get(email=email)
                    except ObjectDoesNotExist:
                        existing_email = None

                    if existing_username or existing_email:
                        credentials_taken = True
                    else:
                        if len(password) < 8 or not any(char.isdigit() for char in password):
                            invalid_credentials = True
                        else:
                            new_user = User.objects.create_user(
                                username=username,
                                email=email,
                                password=password
                            )
                            request.session['user_email'] = new_user.email
                            request.session['user_username'] = new_user.username
                            request.session['user_logged_in'] = True
                            return HttpResponseRedirect('/')

        data = {
            'invalid_credentials': invalid_credentials,
            'credentials_taken': credentials_taken,
            'contains_space_in_credentials': contains_space_in_credentials,
        }
        return render(request, self.template_name, data)


class LoginView(View):
    template_name = 'auth/login.html'

    def get(self, request):
        request.session.pop('user_email', None)
        request.session.pop('user_username', None)
        request.session.pop('user_logged_in', None)

        data = {
            'invalid_credentials': False,
        }
        return render(request, self.template_name, data)

    def post(self, request):
        invalid_credentials = False

        username = request.POST.get('username')
        password = request.POST.get('password')

        if not (username and password):
            invalid_credentials = True
        else:
            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                user = None

            if not user or not user.check_password(password):
                invalid_credentials = True
            else:
                request.session['user_email'] = user.email
                request.session['user_username'] = user.username
                request.session['user_logged_in'] = True
                return HttpResponseRedirect('/')

        data = {
            'invalid_credentials': invalid_credentials,
        }
        return render(request, self.template_name, data)


class LogoutView(View):
    def get(self, request):
        if 'user_email' in request.session:
            del request.session['user_email']
            del request.session['user_username']
            del request.session['user_logged_in']

        return HttpResponseRedirect('/')
