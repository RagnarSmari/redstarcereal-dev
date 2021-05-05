from django.urls import include, path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('home/contact', views.contact,name='contact')
]