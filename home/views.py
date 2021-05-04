from django.shortcuts import render

import product.models
from product import models
from django.http import HttpResponse
# Create your views here.

def index(request):
    products = {
        'product': product.models.Product.all()
    }
    return render(request, 'base.html', products)

def home(request):
    return render(request, 'home/home.html')