from django.contrib import admin
from django.urls import path, include
from crm_app.views import home
from crm_app.views import home, zyb_tracker_statistics_action
from crm_app import views
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', lambda request: redirect('accounts/login/')),
    path('', home, name='home'),  # Homepage
    path('', include('crm_app.urls')),  # This removes the 'clients/' prefix for all routes
    path('hybridaction/zybTrackerStatisticsAction', zyb_tracker_statistics_action, name='zyb_tracker_statistics_action'),
    path('signup/', views.signup_view, name='signup'),
    path('add_customer/', views.client_create, name='add_customer'),
]
