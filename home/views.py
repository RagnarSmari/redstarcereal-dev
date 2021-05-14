from product.models import Product, ProductGallery, Manufacturer, NutritionalInfo, Category
from .forms import ContactForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail, BadHeaderError

# Create your views here.


def home(request):
    context = {
        'products': Product.objects.all(),
        'categories': Category.objects.all()
        }
    return render(request, 'home/home.html', context)


def index(request):
    return render(request, 'base.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = 'Website Inquiry'
            body = {
                'full_name': form.cleaned_data['full_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message']
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject,message,'admin@example.com', ['redstarcereal@gmail.com'])
            except BadHeaderError:
                return HttpResponse('invalid header found')

            name = form.cleaned_data.get('full_name')

            messages.success(request, f'Thank you {name}. We will contact you as soon as possible!')
            return redirect('/home')
        messages.error(request, "Error. Message not sent.")

    form = ContactForm()
    return render(request, 'home/contact.html', {'form': form})


def products(request):
    if 'order_by' in request.GET:
        sort_param = request.GET['order_by']
    else:
        sort_param = 'id'
    if 'tag' in request.GET:
        tag = request.GET['tag']
        context = list(Product.objects.filter(categories__category__icontains=tag).order_by(sort_param).values())
    else:
        context = list(Product.objects.all().order_by(sort_param).values())

    for item in context:
        item['first_image'] = ProductGallery.objects.filter(product_id=item['id']).first().image
    return JsonResponse(context, safe=False)




