from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('profile', views.profile_page, name='profile'),

    path('password_reset',
         auth_views.PasswordResetView.as_view(
             template_name='home/password_reset.html'), name = 'password_reset'),

    path('password_reset/done',
             auth_views.PasswordResetDoneView.as_view(
                 template_name='home/password_reset_done.html'), name = 'password_reset_done'),

    path('password_reset-confirm/<uidb64>/<token>/',
                 auth_views.PasswordResetConfirmView.as_view(
                     template_name='home/password_reset_confirm.html'), name = 'password_reset_confirm'),

    path('password_reset_complete',
                 auth_views.PasswordResetCompleteView.as_view(
                     template_name='home/password_reset_complete.html'), name = 'password_reset_complete'),
]


