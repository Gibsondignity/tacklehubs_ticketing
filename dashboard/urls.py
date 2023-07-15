from django.urls import path
from . import views


urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('categories', views.categories, name='categories'),
    path('events', views.events, name='events'),
    #path('about/',views.about
]
