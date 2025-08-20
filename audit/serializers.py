from rest_framework import serializers
from .models import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'username', 'user_role', 'action', 
            'object_repr', 'changes', 'ip_address', 'user_agent', 
            'timestamp', 'additional_data'
        ]
        read_only_fields = ['__all__']
