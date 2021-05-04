from django.shortcuts import render

import product.models
from product.models import Product
from django.http import HttpResponse
# Create your views here.

def index(request):

    return render(request, 'base.html')

def home(request):

    context = {
        'products': Product.objects.all()

    }
    for product in context['products']:
        print(product.first_image)

    return render(request, 'home/home.html', context)

