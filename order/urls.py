from django.urls import include, path
from . import views

urlpatterns = [
    path('orders/cart/count', views.items_in_cart , name='items_in_cart'),
    path('orders/cart', views.add_to_cart, name='add_to_cart')
]