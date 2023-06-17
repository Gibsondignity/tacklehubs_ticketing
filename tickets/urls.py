from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('events', views.events, name='events'),
]
