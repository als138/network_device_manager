from rest_framework import generics, permissions
from .models import AuditLog
from .serializers import AuditLogSerializer

class AuditLogListView(generics.ListAPIView):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    ordering = ['-timestamp']

    def get_queryset(self):
        queryset = AuditLog.objects.all()
        
        # ساده filtering برای admin
        if self.request.user.role == 'admin':
            return queryset
        else:
            # کاربران عادی فقط لاگ‌های خودشان را می‌بینند
            return queryset.filter(user=self.request.user)
