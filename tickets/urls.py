from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('events', views.events, name='events'),
    path('events/<int:id>/<str:slug>', views.event, name='event'),
]
