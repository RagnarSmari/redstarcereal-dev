from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .forms import *
from .models import Image, Search
from django.contrib.auth.models import User
from .forms import UserUpdateForm, UpdateProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.

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
        if not request.user.is_authenticated:
            messages.warning(request, ' you need to be logged in to view that!')
            return redirect('login')
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.image)


    context = {
        'user_form': user_form,
        'profile_from': profile_form
    }


    return render(request, 'home/profile_page.html', context)


def success(request):
    return HttpResponse('successfully uploaded')

def search_history(request):
    user = User.objects.get(username=request.user)
    history = list(Search.objects.filter(user=user).order_by('-timestamp').values('keyword', 'id'))
    print(history)
    return JsonResponse(history, safe=False)

