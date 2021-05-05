from django.urls import include, path
from . import views
urlpatterns = [
    path('products/<int:id>', views.get_product_by_id, name='product_details')
]