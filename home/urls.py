from django.urls import include, path
from . import views
from users import views as user_view
urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('home/contact', views.contact,name='contact'),
    path('home/register', user_view.register, name='register'),
    path('home/login', user_view.user_login, name='login'),
    path('home/filter/', views.products, name='filter')
]