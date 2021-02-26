from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from random import randint

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            request.session.set_expiry(300)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials, Please try again')
            return redirect('login')
    else:
        return render(request, 'user/login.html')


def user_logout(request):
    logout(request)
    return render(request, 'user/logout.html')


@login_required
def profile(request):
    return render(request, 'user/profile.html')
