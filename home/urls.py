from django.urls import include, path
from . import views
from users import views as user_view
from django.contrib.auth import  views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('home/contact', views.contact,name='contact'),
    path('home/register', user_view.register, name='register'),
    path('home/filter', views.products, name='filter'),
    path('filter', views.products, name='filter'),
    path('home/login', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    path('home/logout', auth_views.LogoutView.as_view(template_name='home/logout.html'), name='logout'),
]