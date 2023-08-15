from django.urls import path
from . import views


urlpatterns = [
    # main views
    path('dashboard', views.dashboard, name='dashboard'),
    path('categories', views.categories, name='categories'),
    path('events', views.events, name='dashboard_events'),
    path('ussd-request', views.ussd, name='dashboard_ussd'),
    
    # Get Views
    path('getEvents', views.getEvents, name='getEvents'),
    path('getCategories', views.getCategories, name='getCategories'),
    
    # Upadate
    path('updateEvent', views.updateEvent, name='updateEvent'),
    path('updateCategory', views.updateCategory, name='updateCategory'),
    
    
    # delete
    path('deleteEvents', views.deleteEvents, name='deleteEvents'),
    path('deleteCategory', views.deleteCategory, name='deleteCategory'),
    
    
    path('ticket_reservations', views.ticket_reservations, name='ticket_reservations'),
    path('TicketsReportById', views.TicketsReportById, name='TicketsReportById'),
]
