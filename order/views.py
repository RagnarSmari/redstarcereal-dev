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
import ast

# Create your views here.


def get_user_id(request):
    print(request.user)
    return User.objects.get(username=request.user).id

@csrf_exempt
def add_to_cart(request):



    if request.method == 'POST':

        decodeing = request.body.decode('utf-8')
        body = json.loads(decodeing)

        if request.user.is_authenticated:
            decodeing = request.body.decode('utf-8')
            body = json.loads(decodeing)


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
    pass


def items_in_cart(request):
    if request.method == 'GET':
        u_id = get_user_id(request)

        amount = Cart.objects.filter(user_id=u_id).aggregate(Sum('amount'))['amount__sum']

        return HttpResponse(amount)



