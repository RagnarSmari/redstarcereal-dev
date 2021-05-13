from django.urls import include, path
from . import views

urlpatterns = [
    path('orders/cart/count', views.items_in_cart , name='items_in_cart'),
    path('orders/cart', views.add_to_cart, name='add_to_cart'),
    path('orders/view_cart', views.view_cart, name='view_cart'),
    path('orders/cart/remove', views.delete_from_cart, name='delete_from_cart'),
    path('orders/cart/total', views.get_cart_total, name='get_cart_total'),
    path('orders/contact', views.contact_step, name='contact_step'),
    path('orders/payment', views.payment, name='payment'),
    path('orders/review', views.review, name='review')
]