from django.shortcuts import render, redirect
from django.contrib.auth.models import User

import order.models
from .models import Cart, ContactInfo, PaymentInfo
from product.models import Product
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import ContactInfoForm, PaymentForm
from django_countries.fields import CountryField


# Create your views here.


def get_user_id(request):
    return User.objects.get(username=request.user).id

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        decoding = request.body.decode('utf-8')
        body = json.loads(decoding)

        if request.user.is_authenticated:
            decoding = request.body.decode('utf-8')
            body = json.loads(decoding)

            p_id = Product.objects.get(id=body['product']).id
            u_id = get_user_id(request)
            amt = body['volume']

            if Cart.objects.filter(user_id=u_id, product_id = p_id):
                row = Cart.objects.filter(user_id=u_id, product_id=p_id).get()
                row.amount += amt
                row.save()
            else:
                c = Cart(user_id=u_id, product_id=p_id, amount=amt)
                c.save()

            return HttpResponse(status=201)


def update_cart(request):
    if request.method == 'POST':
        decoding = request.body.decode('utf-8')
        body = json.loads(decoding)

        if request.user.is_authenticated:
            decoding = request.body.decode('utf-8')
            body = json.loads(decoding)

            p_id = Product.objects.get(id=body['product']).id
            u_id = get_user_id(request)
            amt = body['volume']

            if Cart.objects.filter(user_id=u_id, product_id = p_id):
                row = Cart.objects.filter(user_id=u_id, product_id=p_id).get()
                row.amount = amt
                row.save()
            else:
                c = Cart(user_id=u_id, product_id=p_id, amount=amt)
                c.save()
            return HttpResponse(status=201)

@csrf_exempt
def delete_from_cart(request):
    print("1")
    if request.method == 'POST':
        print(request.body)
        decoding = request.body.decode('utf-8')
        body = json.loads(decoding)

        if request.user.is_authenticated:
            decoding = request.body.decode('utf-8')
            body = json.loads(decoding)

            p_id = body['id']
            u_id = get_user_id(request)
            Cart.objects.get(user_id=u_id, product_id=p_id).delete()

            return HttpResponse(status=201)




def items_in_cart(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            u_id = get_user_id(request)

            amount = Cart.objects.filter(user_id=u_id).aggregate(Sum('amount'))['amount__sum']

            return HttpResponse(amount)
        else:
            print('Hæ þú ert í cart count')
            cart = json.loads(request.COOKIES['cart'])
            total = 0
            for _item, amt in cart.items():
                total += amt
            print(total)
            return HttpResponse(total)



def view_cart(request):
    u_id = get_user_id(request)
    print(u_id)
    context = {
        'cart': list(Cart.objects.filter(user_id=u_id).values()),
    }
    for item in context['cart']:
        item['product'] = Product.objects.get(pk=item['product_id'])
        item['price'] = item['product'].price * item['amount']
    context['total'] = get_user_total(u_id)

    return render(request, 'order/cart.html', context)


def get_cart_total(request):
    return HttpResponse(get_user_total(get_user_id(request)))

def get_user_total(u_id):
    cart = list(Cart.objects.filter(user_id=u_id).values())
    total = 0
    for item in cart:
        item['product'] = Product.objects.get(pk=item['product_id'])
        item['price'] = item['product'].price * item['amount']
        total += item['price']
    return total


def contact_step(request):


    if request.method == 'POST':
        form = ContactInfoForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            user = User.objects.get(username=request.user)
            contact.user = user
            contact.save()
            return redirect('order/payment.html')




    form = ContactInfoForm()
    return render(request, 'order/contact_information.html', {'form': form})


def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            user = User.objects.get(username=request.user)
            payment.user = user
            payment.save()



    form  = PaymentForm()
    return render(request,'order/payment.html', {'form': form})

def review(request):
    u = User.objects.get(username=request.user)
    context = {
        'customer': ContactInfo.objects.filter(archived=False).get(user=u),
        'payment': PaymentInfo.objects.filter(archived=False).get(user=u),
        'cart': Cart.objects.filter(user=u),
        'total': get_user_total(u.id)
    }
    return render(request, 'order/review_order.html', context)