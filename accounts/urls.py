from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('account', views.account_login, name='login'),
    path('register', views.account_register, name='register'),
    path('logout', views.account_logout, name='logout'),
    
    # reset_password
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path("password_reset", views.password_reset_request, name="password_reset"),
]