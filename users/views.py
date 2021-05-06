from django.shortcuts import render, redirect
from .froms import UserRegisterForm, LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from user_profile.models import Image


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():

            input_email = form.cleaned_data.get('email')
            if User.objects.filter(email=input_email).exists():
                messages.error(request, f'{input_email} already in use!')
                return redirect('register')

            username = form.cleaned_data.get('username')
            form.save()
            image = Image(user=User.objects.get(email=input_email))
            image.save()
            messages.success(request,f'Account created for {username}, you are now able to log in')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'home/register.html', {'form': form})


def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,f'You are now logged in, welcome {username}!')
            return redirect('home')
        else:
            messages.warning(request, f'invalid username or password')
            return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'home/login.html', {'form': form})