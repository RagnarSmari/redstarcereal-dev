from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound

import product.models
from product.models import Product, ProductGallery, Manufacturer, NutritionalInfo, Category

from django.http import HttpResponse

# Create your views here.
def home(request):
    if request.GET
    context = {
        'products': Product.objects.all().order_by(sort_param)
    }
    return render(request, 'home/home.html', context)


def get_product_by_id(request, id):
    gallery = ProductGallery.objects.filter(product_id=id)
    tags = Category.objects.filter(product = id)
    prod = get_object_or_404(Product, pk=id)

    context = {
        'product': prod,
        'images': [photo.image for photo in gallery],
        'nutrition': get_object_or_404(NutritionalInfo, pk=id),
        'manufacturer': get_object_or_404(Manufacturer, pk = prod.manufacturer_id_id),
        'categories': [tag.category for tag in tags],
        'related_products': Product.objects.all()[:3]
    }

    return render(request, 'products/product_details.html', context)

def manufacturers(request):
    context = {
        'manufacturers': Manufacturer.objects.all().order_by('id')
    }
    return render(request, 'products/manufacturers.html', context)

def get_product_by_manufacturer(request, id):
    man_id = id
    sort_param = 'price'
    context = {
        'products': Product.objects.filter(manufacturer_id=man_id).order_by(sort_param)
    }
    if len(context['products']) > 0:
        return render(request, 'home/home.html', context)
    else:
        return HttpResponseNotFound("No product found")