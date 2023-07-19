from django.urls import path
from . import views


urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('categories', views.categories, name='categories'),
    path('events', views.events, name='dashboard_events'),
    
    
    path('getEvents', views.getEvents, name='getEvents'),
    path('getCategories', views.getCategories, name='getCategories'),
    
    
    path('updateEvent', views.updateEvent, name='updateEvent'),
    path('deleteEvents', views.deleteEvents, name='deleteEvents'),
    #path('about/',views.about
]
