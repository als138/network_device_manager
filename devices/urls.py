from django.urls import path
from . import views

urlpatterns = [
    path('', views.DeviceListCreateView.as_view(), name='device-list-create'),
    path('<int:pk>/', views.DeviceDetailView.as_view(), name='device-detail'),
    path('<int:device_id>/commands/', views.DeviceCommandListCreateView.as_view(), name='device-commands'),
    path('statistics/', views.device_statistics, name='device-statistics'),
]
