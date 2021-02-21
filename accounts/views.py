from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login


# Create your views here.

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
