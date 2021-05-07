from django.urls import include, path
from . import views
urlpatterns = [
    path('profile', views.profile_page, name='profile')
]