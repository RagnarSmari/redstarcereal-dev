from django.shortcuts import render, redirect
from django.contrib.auth.models import User

import order.models
from .models import Cart
from product.models import Product
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
import json


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
        u_id = get_user_id(request)

        amount = Cart.objects.filter(user_id=u_id).aggregate(Sum('amount'))['amount__sum']

        return HttpResponse(amount)



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



