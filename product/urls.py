from django.urls import include, path
from . import views
urlpatterns = [
    path('products/<int:id>', views.get_product_by_id, name='product_details'),
    path('manufacturers/', views.manufacturers, name='manufacturers'),
    path('manufacturers/<int:id>', views.get_product_by_manufacturer, name='product_my_manufacturer'),
    path('home', views.home, name='products')
]