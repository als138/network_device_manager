from rest_framework import serializers
from .models import Device, DeviceCommand

class DeviceSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Device
        fields = [
            'id', 'name', 'device_type', 'ip_address', 'mac_address', 
            'location', 'vendor', 'model', 'os_version', 'status', 
            'ssh_port', 'ssh_username', 'description', 'created_by', 
            'created_by_username', 'created_at', 'updated_at', 'last_seen'
        ]
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at', 'last_seen')
        extra_kwargs = {
            'ssh_password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class DeviceCommandSerializer(serializers.ModelSerializer):
    executed_by_username = serializers.CharField(source='executed_by.username', read_only=True)
    device_name = serializers.CharField(source='device.name', read_only=True)

    class Meta:
        model = DeviceCommand
        fields = [
            'id', 'device_name', 'command', 'output', 'status',
            'executed_by_username', 'executed_at', 'completed_at', 'error_message'
        ]
        read_only_fields = ('id', 'executed_by', 'executed_at', 'completed_at', 'output', 'status', 'error_message', 'device_name', 'executed_by_username')
