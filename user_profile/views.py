from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from .models import Image
from django.contrib.auth.models import User


# Create your views here.
def profile_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                user = User.objects.get(username=request.user)
                image = Image.objects.get(user_id=user.id)
                image.update(image=form.image)
                return redirect('success')
        else:
            print(request.user)
            form = ProfileForm()
        return render(request, 'home/profile_page.html', {'form': form})
    else:
        return redirect('login')

def success(request):
    return HttpResponse('successfully uploaded')
