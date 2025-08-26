from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Device, DeviceCommand
from .serializers import DeviceSerializer, DeviceCommandSerializer

class DeviceListCreateView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name', 'ip_address', 'location', 'vendor', 'model']
    ordering_fields = ['name', 'created_at', 'last_seen']

class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

class DeviceCommandListCreateView(generics.ListCreateAPIView):
    serializer_class = DeviceCommandSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        device_id = self.kwargs.get('device_id')
        return DeviceCommand.objects.filter(device_id=device_id)

    def perform_create(self, serializer):
        device_id = self.kwargs.get('device_id')
        device = get_object_or_404(Device, id=device_id)
        
        command_obj = serializer.save(device=device, status='completed')
        
        # شبیه‌سازی اجرای دستور (برای demo)
        command_obj.output = f"Mock output for command: {command_obj.command}\nDevice: {device.name}\nIP: {device.ip_address}\nVendor: {device.vendor}\nModel: {device.model}\nStatus: Command executed successfully\nTimestamp: {timezone.now()}"
        command_obj.completed_at = timezone.now()
        command_obj.save()

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def device_statistics(request):
    total_devices = Device.objects.count()
    online_devices = Device.objects.filter(status='online').count()
    offline_devices = Device.objects.filter(status='offline').count()
    maintenance_devices = Device.objects.filter(status='maintenance').count()
    error_devices = Device.objects.filter(status='error').count()
    
    device_types = {}
    for device in Device.objects.all():
        device_type = device.device_type
        if device_type in device_types:
            device_types[device_type] += 1
        else:
            device_types[device_type] = 1
    
    vendors = {}
    for device in Device.objects.all():
        vendor = device.vendor
        if vendor in vendors:
            vendors[vendor] += 1
        else:
            vendors[vendor] = 1
    
    return Response({
        'total_devices': total_devices,
        'online_devices': online_devices,
        'offline_devices': offline_devices,
        'maintenance_devices': maintenance_devices,
        'error_devices': error_devices,
        'device_types': device_types,
        'vendors': vendors,
        'uptime_percentage': round((online_devices / total_devices * 100), 2) if total_devices > 0 else 0
    })
