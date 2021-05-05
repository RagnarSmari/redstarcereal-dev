from django.shortcuts import render, get_object_or_404

import product.models
from product.models import Product, ProductGallery, Manufacturer, NutritionalInfo, Category
from django.http import HttpResponse

# Create your views here.
def get_product_by_id(request, id):
    gallery = ProductGallery.objects.filter(product_id=id)
    tags = Category.objects.filter(product = id)
    prod = get_object_or_404(Product, pk=id)
    context = {
        'product': prod,
        'images': [photo.image for photo in gallery],
        'nutrition': get_object_or_404(NutritionalInfo, pk=id),
        'manufacturer': get_object_or_404(Manufacturer, pk = prod.manufacturer_id_id),
        'categories': [tag.category for tag in tags]
    }
    print(context['product'].name)
    print(context['nutrition'].calories)
    print(context['categories'])
    print(context['manufacturer'].name)
    return render(request, 'products/product_details.html', context)