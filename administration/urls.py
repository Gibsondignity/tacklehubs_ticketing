from django.urls import path
from . import views


urlpatterns = [
    # main views
    path('administration/dashboard', views.admin_dashboard, name='administration'),
    path('administration/categories', views.admin_categories, name='admin_categories'),
    path('administration/events', views.admin_events, name='admin_dashboard_events'),
    path('administration/ussd-request', views.admin_ussd, name='admin_dashboard_ussd'),
    # path('administration/profile', views.admin_profile, name='admin_profile'),
    # path('administration/UserInformation', views.admin_UserInformation, name='admin_UserInformation'),
    
    # Get Views
    path('administration/getEvents', views.admin_getEvents, name='admin_getEvents'),
    path('administration/getCategories', views.admin_getCategories, name='admin_getCategories'),
    
    # Upadate
    path('administration/updateEvent', views.admin_updateEvent, name='admin_updateEvent'),
    path('administration/updateCategory', views.admin_updateCategory, name='admin_updateCategory'),
    path('administration/change_event_status', views.change_event_status, name='change_event_status'),
    path('administration/reject_event', views.reject_event, name='reject_event'),
    
    
    # delete
    path('administration/deleteEvents', views.admin_deleteEvents, name='admin_deleteEvents'),
    path('administration/deleteCategory', views.admin_deleteCategory, name='admin_deleteCategory'),
    
    
    path('administration/ticket_reservations', views.admin_ticket_reservations, name='admin_ticket_reservations'),
    path('administration/TicketsReportById', views.admin_TicketsReportById, name='admin_TicketsReportById'),
    
    path('administration/events/<str:slug>/<int:id>', views.view_event_tickets, name='event_details'),
]
