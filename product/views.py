from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from product.models import *
from .forms import ReviewForm
from django.http import HttpResponse, JsonResponse
from user_profile.models import Search
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
        'related_products': Product.objects.all()[:3],
        'reviews': Review.objects.filter(product_id=prod.id).order_by('-last_modified')
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

def search_products(request):
    keyword = request.GET['keyword']

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        _s, _created = Search.objects.update_or_create(keyword=keyword, user=user)
    if 'order_by' in request.GET:
        sort_param = request.GET['order_by']
    else:
        sort_param = 'id'
    if 'tag' in request.GET:
        tag = request.GET['tag']
        context = list(Product.objects.filter(name__icontains=keyword).filter(categories__category__icontains=tag).order_by(sort_param).values())
    else:
        context = list(Product.objects.filter(name__icontains=keyword).order_by(sort_param).values())

    for item in context:
        item['first_image'] = ProductGallery.objects.filter(product_id=item['id']).first().image
    return JsonResponse(context, safe=False)\

@login_required
def review_product(request, product_id):
        if request.method == 'POST':
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                rev = review_form.save(commit=False)
                rev.product_id = product_id
                rev.user_id = User.objects.get(username=request.user).id
                print(rev)
                rev.save()
                messages.success(request, 'Your review has been added')
                return redirect('home')
        else:
            review_form = ReviewForm()

        context = {
            'review_form': review_form,
            'product': Product.objects.get(pk=product_id)
        }

        return render(request, 'products/review.html', context)


