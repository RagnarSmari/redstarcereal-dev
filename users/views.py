from django.shortcuts import render, redirect
from .froms import UserRegisterForm, LoginForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from user_profile.models import Image
from redstarcereal.mail_service import MailService

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
            #image = Image(user=User.objects.get(email=input_email))
            #image.save()
            messages.success(request,f'Account created for {username}, please Login.')
            MailService().welcome_mail(input_email,username)
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'home/register.html', {'form': form})


