from django.shortcuts import render

import product.models
from product import models
from django.http import HttpResponse
# Create your views here.

def index(request):
    context = {
        'products': product.models.Product.all()
    }
    return render(request, 'base.html', context)

def home(request):
    return render(request, 'home/home.html')