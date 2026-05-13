from django.urls import path

from .views import *



urlpatterns = [
    path('login_/',login_,name='login_'),
    path('',register,name='register'),
    path('profile/',profile,name='profile'),
    path('forget_pass/',forget_pass,name='forget_pass'),
    path('new_pass/',new_pass,name='new_pass'),
    path('logout_/',logout_,name='logout_'),
    path('reset_pass/',reset_pass,name='reset_pass')
]