import socket
import subprocess
import paramiko
from django.utils import timezone
from .models import Device, DeviceCommand

def ping_device(ip_address):
    """
    Ping a device to check if it's reachable.
    """
    try:
        # For Unix/Linux/MacOS
        result = subprocess.run(['ping', '-c', '1', ip_address], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def check_port_open(ip_address, port, timeout=5):
    """
    Check if a specific port is open on a device.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip_address, port))
        sock.close()
        return result == 0
    except:
        return False

def execute_ssh_command(device, command):
    """
    Execute a command on a device via SSH.
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh.connect(
            hostname=device.ip_address,
            port=device.ssh_port,
            username=device.ssh_username,
            password=device.ssh_password,
            timeout=10
        )
        
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        ssh.close()
        
        if error:
            return False, error
        
        return True, output
        
    except Exception as e:
        return False, str(e)

def update_device_status():
    """
    Update the status of all devices based on connectivity.
    """
    devices = Device.objects.all()
    
    for device in devices:
        if ping_device(device.ip_address):
            if check_port_open(device.ip_address, device.ssh_port):
                device.status = 'online'
            else:
                device.status = 'offline'
        else:
            device.status = 'offline'
        
        device.last_seen = timezone.now()
        device.save()

def backup_device_config(device):
    """
    Backup current configuration of a device.
    """
    # This would depend on the device type and vendor
    # Example for Cisco devices
    commands = {
        'cisco': 'show running-config',
        'juniper': 'show configuration',
        'hp': 'show running-config',
    }
    
    vendor_lower = device.vendor.lower()
    command = commands.get(vendor_lower, 'show running-config')
    
    success, output = execute_ssh_command(device, command)
    
    if success:
        return output
    else:
        return None
