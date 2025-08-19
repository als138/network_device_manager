
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Device, DeviceConfiguration, DeviceCommand
from .serializers import (
    DeviceSerializer, DeviceConfigurationSerializer, 
    DeviceCommandSerializer, ExecuteCommandSerializer, PingDeviceSerializer
)
from .permissions import DevicePermission, CommandPermission
from .utils import ping_device, execute_ssh_command, backup_device_config, update_device_status

class DeviceListCreateView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [DevicePermission]
    filterset_fields = ['device_type', 'status', 'vendor', 'location']
    search_fields = ['name', 'ip_address', 'location', 'vendor', 'model']
    ordering_fields = ['name', 'created_at', 'last_seen']

class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [DevicePermission]

class DeviceConfigurationListCreateView(generics.ListCreateAPIView):
    serializer_class = DeviceConfigurationSerializer
    permission_classes = [CommandPermission]

    def get_queryset(self):
        device_id = self.kwargs.get('device_id')
        return DeviceConfiguration.objects.filter(device_id=device_id)

    def perform_create(self, serializer):
        device_id = self.kwargs.get('device_id')
        device = get_object_or_404(Device, id=device_id)
        
        # Backup current configuration before applying new one
        backup_config = backup_device_config(device)
        
        serializer.save(
            device=device,
            backup_config=backup_config or ""
        )

class DeviceCommandListCreateView(generics.ListCreateAPIView):
    serializer_class = DeviceCommandSerializer
    permission_classes = [CommandPermission]

    def get_queryset(self):
        device_id = self.kwargs.get('device_id')
        return DeviceCommand.objects.filter(device_id=device_id)

    def perform_create(self, serializer):
        device_id = self.kwargs.get('device_id')
        device = get_object_or_404(Device, id=device_id)
        
        command_obj = serializer.save(device=device, status='running')
        
        # Execute command
        success, output = execute_ssh_command(device, command_obj.command)
        
        if success:
            command_obj.status = 'completed'
            command_obj.output = output
        else:
            command_obj.status = 'failed'
            command_obj.error_message = output
        
        command_obj.completed_at = timezone.now()
        command_obj.save()

@api_view(['POST'])
@permission_classes([CommandPermission])
def execute_bulk_command(request):
    """
    Execute a command on multiple devices.
    """
    serializer = ExecuteCommandSerializer(data=request.data)
    if serializer.is_valid():
        command = serializer.validated_data['command']
        device_ids = serializer.validated_data['device_ids']
        
        devices = Device.objects.filter(id__in=device_ids)
        results = []
        
        for device in devices:
            command_obj = DeviceCommand.objects.create(
                device=device,
                command=command,
                executed_by=request.user,
                status='running'
            )
            
            success, output = execute_ssh_command(device, command)
            
            if success:
                command_obj.status = 'completed'
                command_obj.output = output
            else:
                command_obj.status = 'failed'
                command_obj.error_message = output
            
            command_obj.completed_at = timezone.now()
            command_obj.save()
            
            results.append({
                'device_id': device.id,
                'device_name': device.name,
                'command_id': command_obj.id,
                'status': command_obj.status,
                'output': command_obj.output if success else command_obj.error_message
            })
        
        return Response({'results': results}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def ping_device_view(request):
    """
    Ping a specific device.
    """
    serializer = PingDeviceSerializer(data=request.data)
    if serializer.is_valid():
        device_id = serializer.validated_data['device_id']
        device = get_object_or_404(Device, id=device_id)
        
        is_reachable = ping_device(device.ip_address)
        
        if is_reachable:
            device.status = 'online'
            device.last_seen = timezone.now()
            device.save()
        
        return Response({
            'device_id': device.id,
            'device_name': device.name,
            'ip_address': device.ip_address,
            'is_reachable': is_reachable,
            'timestamp': timezone.now()
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_all_device_status(request):
    """
    Update status of all devices.
    """
    try:
        update_device_status()
        return Response({
            'message': 'Device statuses updated successfully',
            'timestamp': timezone.now()
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def device_statistics(request):
    """
    Get device statistics.
    """
    total_devices = Device.objects.count()
    online_devices = Device.objects.filter(status='online').count()
    offline_devices = Device.objects.filter(status='offline').count()
    maintenance_devices = Device.objects.filter(status='maintenance').count()
    error_devices = Device.objects.filter(status='error').count()
    
    device_types = Device.objects.values('device_type').distinct().count()
    vendors = Device.objects.values('vendor').distinct().count()
    
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
