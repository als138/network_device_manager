from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Device(models.Model):
    DEVICE_TYPES = [
        ('router', 'Router'),
        ('switch', 'Switch'),
        ('firewall', 'Firewall'),
        ('access_point', 'Access Point'),
        ('load_balancer', 'Load Balancer'),
    ]
    
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('maintenance', 'Maintenance'),
        ('error', 'Error'),
    ]

    name = models.CharField(max_length=100, unique=True)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=17, blank=True)
    location = models.CharField(max_length=200)
    vendor = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    os_version = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offline')
    ssh_port = models.IntegerField(default=22)
    ssh_username = models.CharField(max_length=50, blank=True)
    ssh_password = models.CharField(max_length=100, blank=True)  # In production, use encrypted storage
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_devices')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.ip_address})"

class DeviceConfiguration(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='configurations')
    config_name = models.CharField(max_length=100)
    config_content = models.TextField()
    applied_by = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    backup_config = models.TextField(blank=True)

    class Meta:
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.device.name} - {self.config_name}"

class DeviceCommand(models.Model):
    COMMAND_STATUS = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='commands')
    command = models.TextField()
    output = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=COMMAND_STATUS, default='pending')
    executed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    executed_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ['-executed_at']

    def __str__(self):
        return f"{self.device.name} - {self.command[:50]}..."
