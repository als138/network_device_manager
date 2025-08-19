from django.urls import path
from . import views

urlpatterns = [
    path('', views.DeviceListCreateView.as_view(), name='device-list-create'),
    path('<int:pk>/', views.DeviceDetailView.as_view(), name='device-detail'),
    path('<int:device_id>/configurations/', views.DeviceConfigurationListCreateView.as_view(), name='device-config'),
    path('<int:device_id>/commands/', views.DeviceCommandListCreateView.as_view(), name='device-commands'),
    path('execute-bulk-command/', views.execute_bulk_command, name='execute-bulk-command'),
    path('ping/', views.ping_device_view, name='ping-device'),
    path('update-status/', views.update_all_device_status, name='update-device-status'),
    path('statistics/', views.device_statistics, name='device-statistics'),
]
