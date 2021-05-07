from django.shortcuts import render, redirect
from product.models import Product
from django.http import HttpResponse
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
# Create your views here.
def home(request):
    if 'order_by' in request.GET:
        sort_param = request.GET['order_by']
    else:
        sort_param = 'id'
    if 'search_param' in request.GET:
        search = request.GET['search_param']
        if 'tag' in request.GET:
            tag = request.GET['tag']
            context = {
                'products': Product.objects.filter(name__icontains=search).filter(categories__category__icontains=tag).order_by(sort_param)
            }
        else:
            context = {
                'products': Product.objects.filter(name__icontains=search).order_by(sort_param)
            }
    else:
        if 'tag' in request.GET:
            tag = request.GET['tag']
            context = {
                'products': Product.objects.filter(categories__category__icontains=tag).order_by(sort_param)
            }
        else:
            context = {
                'products': Product.objects.all().order_by(sort_param)
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
                send_mail(subject,message,'admin@example.com', ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('invalid header found')

            name = form.cleaned_data.get('full_name')

            messages.success(request, f'Thank you {name}. We will contact you as soon as possible!')
            return redirect('/home')
        messages.error(request, "Error. Message not sent.")

    form = ContactForm()
    return render(request, 'home/contact.html', {'form':form})



