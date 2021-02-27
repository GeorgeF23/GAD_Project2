from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import re

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

SUCCESS = 0
EMAIL_TAKEN_ERROR = 1
USERNAME_TAKEN_ERROR = 2
MISSING_FIELD_ERROR = 3
INVALID_EMAIL_ERROR = 4


def login_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'accounts/login.html')

    if request.method == 'POST':
        username = request.POST['login_username']
        password = request.POST['login_password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'accounts/login.html', {
                'login_error': 'Invalid username or password'
            })


def validate_register_input(username, password, first_name, last_name, email):
    if User.objects.filter(username=username).count() > 0:
        return USERNAME_TAKEN_ERROR
    if User.objects.filter(email=email).count() > 0:
        return EMAIL_TAKEN_ERROR

    if len(username) == 0 or len(password) == 0 or len(first_name) == 0 or len(last_name) == 0 or len(email) == 0:
        return MISSING_FIELD_ERROR

    if not re.match(EMAIL_REGEX, email):
        return INVALID_EMAIL_ERROR

    return SUCCESS


def send_register_email(user):
    subject = 'GAD Store account'
    message = f'Hello, {user.first_name}!\nThank you for registering an account to our store!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(
        subject,
        message,
        email_from,
        recipient_list,
        fail_silently=False
    )


def register_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'accounts/register.html')

    if request.method == 'POST':
        username = request.POST['register_username']
        password = request.POST['register_password']
        first_name = request.POST['register_first_name']
        last_name = request.POST['register_last_name']
        email = request.POST['register_email']

        valid = validate_register_input(username, password, first_name, last_name, email)
        error_msg = None

        if valid == EMAIL_TAKEN_ERROR:
            error_msg = "Email already in use!"
        elif valid == USERNAME_TAKEN_ERROR:
            error_msg = "Username already taken!"
        elif valid == MISSING_FIELD_ERROR:
            error_msg = "All fields are necessary!"
        elif valid == INVALID_EMAIL_ERROR:
            error_msg = "Email is not valid!"

        if valid != SUCCESS:
            return render(request, 'accounts/register.html', {
                'register_error': error_msg
            })

        user = User.objects.create_user(username, email, password)
        user.last_name = last_name
        user.first_name = first_name
        user.save()

        send_register_email(user)

        login(request, user)
        return redirect('/')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect("/")
