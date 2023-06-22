from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('events', views.events, name='events'),
    path('events/<int:id>/<str:slug>', views.event, name='event'),
    
    path('user_information', views.initiate_payment, name='initiate_payment'),
    path('<str:ref>/', views.verify_payment, name='verify_payment'),
]
