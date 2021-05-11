from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Cart
from product.models import Product
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
import ast

# Create your views here.


def get_user_id(request):
    print(request.user)
    return User.objects.get(username=request.user).id

@csrf_exempt
def add_to_cart(request):
    print('Hæ')
    if request.method == 'POST':
        print('Bæng')
        if request.user.is_authenticated:
            p_id = Product.objects.get(id=request.body.id)
            u_id = get_user_id(request)
            amt = request.body.amt
            c = Cart(user_id=u_id, product=p_id, amount=amt)
            c.save()

            #messages.success(request, f'{Product.object.get(id=p_id).name} was succsessfuly added to your cart')
            return HttpResponse("nice")
        else:
            messages.error(request, 'You need to be logged in to add to cart')
            return render(request, 'home/login.html')


def update_cart(request):
    pass


def items_in_cart(request):
    if request.method == 'GET':
        u_id = get_user_id(request)

        amount = Cart.objects.filter(user_id=u_id).aggregate(Sum('amount'))['amount__sum']

        return HttpResponse(amount)



