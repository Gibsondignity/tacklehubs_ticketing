from django.urls import path, include
from . import views


urlpatterns = [
    path('account', views.account_login, name='login'),
    path('register', views.account_register, name='register'),
]