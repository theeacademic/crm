from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication paths
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('accounts/register/', views.register, name='register'),

    # Client-related paths
    path('clients/', views.client_list, name='client_list'),
    path('clients/create/', views.client_create, name='client_create'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('saved_list/', views.saved_list, name='saved_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_customer/<int:client_id>/', views.add_customer, name='add_customer'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('delete_customer/<int:id>/', views.delete_customer, name='delete_customer'),

    # Housemaid paths
    path('housemaid/', views.housemaid_form_list, name='housemaid_form_list'),
    path('housemaid/delete/<int:housemaid_id>/', views.delete_housemaid, name='delete_housemaid'),
   path('housemaid/edit/<int:housemaid_id>/', views.edit_housemaid, name='edit_housemaid'),
   path('add-housemaid/', views.add_housemaid, name='add_housemaid'),
]
