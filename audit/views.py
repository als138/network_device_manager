from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import AuditLog
from .serializers import AuditLogSerializer

class AuditLogListView(generics.ListAPIView):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['action', 'user', 'content_type']
    search_fields = ['object_repr', 'user__username', 'ip_address']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']

    def get_queryset(self):
        # Regular users can only see their own audit logs
        # Admins can see all audit logs
        if self.request.user.role == 'admin':
            return AuditLog.objects.all()
        else:
            return AuditLog.objects.filter(user=self.request.user)
