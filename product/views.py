from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from product.models import Product, ProductGallery, Manufacturer, NutritionalInfo, Category

from django.http import HttpResponse, JsonResponse

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
        'products': Product.objects.filter(manufacturer_id=man_id).order_by(sort_param),
        'categories': Category.objects.all()
    }
    if len(context['products']) > 0:
        return render(request, 'home/home.html', context)
    else:
        return HttpResponseNotFound("No products found")


def product_filter_and_manufacturer(request, id):
    man_id = id
    if 'order_by' in request.GET:
        sort_param = request.GET['order_by']
    else:
        sort_param = 'id'
    if 'tag' in request.GET:
        tag = request.GET['tag']
        context = list(Product.objects.filter(manufacturer_id=man_id).filter(categories__category__icontains=tag).order_by(sort_param).values())
    else:
        context = list(Product.objects.filter(manufacturer_id=man_id).order_by(sort_param).values())

    for item in context:
        item['first_image'] = ProductGallery.objects.filter(product_id=item['id']).first().image
    return JsonResponse(context, safe=False)

