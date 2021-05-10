from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from .models import Image
from django.contrib.auth.models import User
from .forms import UserUpdateForm, UpdateProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# Create your views here.
@login_required
def profile_page(request):

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST,
                                         request.FILES,
                                         instance=request.user.image)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,f'Your account has been updated')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.image)


    context = {
        'user_form': user_form,
        'profile_from': profile_form
    }


    return render(request, 'home/profile_page.html', context)


def success(request):
    return HttpResponse('successfully uploaded')
