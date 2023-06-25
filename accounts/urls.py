from django.urls import path, include
from . import views


urlpatterns = [
    path('login', views.account_login, name='login'),
    path('register', views.account_register, name='register'),
]