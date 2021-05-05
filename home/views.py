from django.shortcuts import render, get_object_or_404

import product.models
from product.models import Product, ProductGallery, Manufacturer, NutritionalInfo, Category
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, 'base.html')

def home(request):
    context = {
        'products': Product.objects.all().order_by('name')
    }
    return render(request, 'home/home.html', context)




