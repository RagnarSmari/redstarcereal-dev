from django.shortcuts import render, redirect
from django.contrib.auth.models import User

import order.models
from .models import Cart, ContactInfo, PaymentInfo, Order, OrderRow
from product.models import Product
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import ContactInfoForm, PaymentForm
from redstarcereal.mail_service import MailService
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

            if Cart.objects.filter(user_id=u_id, product_id=p_id):
                row = Cart.objects.filter(user_id=u_id, product_id=p_id).get()
                row.amount += amt
                if row.amount <= 0:
                    row.delete()
                else:
                    row.save()
            else:
                c = Cart(user_id=u_id, product_id=p_id, amount=amt)
                c.save()

            if ContactInfo.objects.filter(user_id=u_id, archived=False):
                reset_order(request)

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

            if ContactInfo.objects.filter(user_id=u_id, archived=False):
                reset_order(request)

            return HttpResponse(status=201)




def items_in_cart(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            u_id = get_user_id(request)

            amount = Cart.objects.filter(user_id=u_id).aggregate(Sum('amount'))['amount__sum']
            print("say whay")
            return HttpResponse(amount)




def view_cart(request):

    if request.user.is_authenticated:
        u_id = get_user_id(request)
        context = {
            'cart': list(Cart.objects.filter(user_id=u_id).values()),
        }
        for item in context['cart']:
            item['product'] = Product.objects.get(pk=item['product_id'])
            item['price'] = item['product'].price * item['amount']
        context['total'] = get_user_total(u_id)

        return render(request, 'order/cart.html', context)
    return redirect('login')


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

    if not request.user.is_authenticated:
        return redirect('login')

    id = get_user_id(request)

    if not Cart.objects.filter(user_id=id):
        messages.warning(request,'Your cart is empty. You can not go to checkout an empty cart.')
        return redirect('home')


    if request.method == 'POST':

        if ContactInfo.objects.filter(user_id=id, archived=False):

            info = ContactInfo.objects.filter(user_id=id, archived=False).get()

            form = ContactInfoForm(request.POST, instance=info)
            form.save()
            return redirect('payment')

        else:
            form = ContactInfoForm(request.POST)
            if form.is_valid():
                contact = form.save(commit=False)
                user = User.objects.get(username=request.user)
                contact.user = user
                contact.save()
                return redirect('payment')

    if ContactInfo.objects.filter(user_id=id, archived=False):
        info = ContactInfo.objects.filter(user_id=id, archived=False).get()
        form = ContactInfoForm(initial={
            'first_name': info.first_name,
            'last_name': info.last_name,
            'email': info.email,
            'street': info.street,
            'house_number': info.house_number,
            'city': info.city,
            'country': info.country,
            'postal_code': info.postal_code
        })
        return render(request, 'order/contact_information.html', {'form': form})



    form = ContactInfoForm()
    return render(request, 'order/contact_information.html', {'form': form})


def payment(request):
    if not request.user.is_authenticated:
        return redirect('login')

    id = get_user_id(request)

    if not ContactInfo.objects.filter(user_id=id, archived=False):
        return HttpResponseForbidden()

    if PaymentInfo.objects.filter(user_id=id, archived=False):
        payment = PaymentInfo.objects.filter(user_id=id, archived=False).get()
        form = PaymentForm(initial={
            'card_holder': payment.card_holder,
            'cc_number': payment.cc_number,
            'cc_expiry': payment.cc_expiry,
            
        })
        return render(request,'order/payment.html', {'form': form})


    if request.method == 'POST':
        if PaymentInfo.objects.filter(user_id=id, archived=False):

            payment = PaymentInfo.objects.filter(user_id=id, archived=False).get()

            form = PaymentForm(request.POST, instance=payment)
            form.save()
            return redirect('review')

        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            user = User.objects.get(username=request.user)
            payment.user = user
            payment.save()
            return redirect('review')

    form  = PaymentForm()
    return render(request,'order/payment.html', {'form': form})



def review(request):

    if not request.user.is_authenticated:
        return redirect('login')


    u = User.objects.get(username=request.user)

    if not PaymentInfo.objects.filter(user_id=u, archived=False):
        messages.warning(request, 'This is not allowed. Go to your cart and start the checkout from there.')
        return redirect('home')

    context = {
        'customer': ContactInfo.objects.filter(archived=False).get(user=u),
        'payment': PaymentInfo.objects.filter(archived=False).get(user=u),
        'cart': Cart.objects.filter(user=u),
        'total': get_user_total(u.id)
    }
    return render(request, 'order/review_order.html', context)

@csrf_exempt
def confirm(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        u = User.objects.get(username=request.user)
        if Cart.objects.filter(user_id=u.id) and ContactInfo.objects.filter(archived=False).get(user=u):
            if PaymentInfo.objects.filter(archived=False).get(user=u):
                if cart_to_order(u):
                    MailService().order_completed(u.id)
                    return HttpResponse(status=201)
    return HttpResponse(status=402)


def gratz(request):
    return render(request, 'order/order_complete.html')


def cart_to_order(user):
    contact_model = ContactInfo.objects.filter(user=user, archived=False).get()
    payment_model = PaymentInfo.objects.filter(user=user, archived=False).get()
    total = get_user_total(user.id)
    order_model = Order(contact_info=contact_model, payment_info=payment_model, total_price=total)

    order_model.save()
    cart = Cart.objects.filter(user_id=user.id)

    for item in cart:
        price = Product.objects.get(pk=item.product.id).price * item.amount
        row = OrderRow(order=order_model, product=item.product, amount=item.amount, row_price=price)

        item.product.stock -= item.amount
        item.product.save()

        row.save()


        Cart.objects.get(pk=item.id).delete()

    contact_model.archived = True
    contact_model.save()
    payment_model.archived = True
    payment_model.save()

    return True


def reset_order(req):
    id = get_user_id(req)
    c_row = ContactInfo.objects.filter(user_id=id, archived=False).get()
    c_row.delete()
    if PaymentInfo.objects.filter(user_id=id, archived=False):
        p_row = PaymentInfo.objects.filter(user_id=id, archived=False).get()
        p_row.delete()




#TODO setja hlekki til að fara fram og til baka

#TODO Tjékka hvort allt sé til áður en þú setur í cart B-KRAFA



