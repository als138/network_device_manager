# 🌐 Network Device Manager API

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.14-orange.svg)](https://django-rest-framework.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](Dockerfile)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive REST API for managing network devices with automated SSH command execution, role-based access control, and comprehensive audit logging.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Crisis Scenario: TechCorp Network Outage](#crisis-scenario-techcorp-network-outage)
- [Usage Examples](#usage-examples)
- [Deployment](#deployment)
- [Contributing](#contributing)

## ✨ Features

### Core Functionality
- **Device Management**: Complete CRUD operations for network devices
- **SSH Command Execution**: Execute commands remotely on network devices
- **Configuration Management**: Deploy and backup device configurations
- **Real-time Monitoring**: Device status tracking and health monitoring

### Security & Access Control
- **JWT Authentication**: Secure token-based authentication
- **Role-based Permissions**: Admin, Engineer, and Viewer roles
- **Audit Logging**: Comprehensive activity tracking
- **Input Validation**: Secure API endpoints

### Enterprise Features
- **RESTful API**: Full REST compliance with proper HTTP methods
- **API Documentation**: Interactive Swagger/OpenAPI documentation
- **Bulk Operations**: Execute commands on multiple devices
- **Pagination & Filtering**: Efficient data handling
- **Docker Support**: Containerized deployment

## 🛠 Tech Stack

### Backend
- **Framework**: Django 4.2 + Django REST Framework 3.14
- **Database**: PostgreSQL 15
- **Authentication**: JWT (Simple JWT)
- **API Documentation**: drf-yasg (Swagger/OpenAPI)

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Web Server**: Nginx (Production)
- **WSGI**: Gunicorn
- **Caching**: Redis (Optional)

### Network Libraries
- **SSH Client**: Paramiko
- **Network Utils**: Custom utilities for device communication

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git
- Terminal/Command Line

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/network-device-manager.git
cd network-device-manager

# Start the application with Docker
docker-compose up -d --build

# Wait for containers to initialize (30-60 seconds)
sleep 30

# Run database migrations
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Create a superuser account
docker-compose exec web python manage.py createsuperuser

# Access the application
open http://localhost:8000/swagger/
```

### Verify Installation

Test the API endpoints:

```bash
# 1. Register a new user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123",
    "password_confirm": "TestPass123",
    "email": "test@example.com",
    "role": "admin"
  }'

# 2. Login and get token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123"
  }'

# 3. Test API access (use token from login response)
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/api/devices/
```

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **Django Admin**: http://localhost:8000/admin/

### Core Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/auth/register/` | POST | User registration | ❌ |
| `/api/auth/login/` | POST | User login | ❌ |
| `/api/devices/` | GET, POST | Device management | ✅ |
| `/api/devices/{id}/` | GET, PUT, DELETE | Device details | ✅ |
| `/api/devices/{id}/commands/` | GET, POST | Command execution | ✅ |
| `/api/devices/statistics/` | GET | Network statistics | ✅ |
| `/api/audit/logs/` | GET | Audit logs | ✅ |

### User Roles & Permissions

| Role | Permissions |
|------|-------------|
| **Admin** | Full access to all resources |
| **Engineer** | Read, Create, Update devices; Execute commands |
| **Viewer** | Read-only access to devices and logs |

## 🚨 Crisis Scenario: TechCorp Network Outage

This section demonstrates the API's capabilities through a realistic network crisis scenario.

### Company Background

**TechCorp** - Software development company with 200 employees across 3 floors:
- **Floor 1**: Development Team (80 employees)
- **Floor 2**: Sales & Marketing (60 employees)
- **Floor 3**: Management & IT (60 employees)

### The Crisis: Monday Morning Network Outage

**9:00 AM Monday**: Floor 2 employees cannot access internet or internal servers. Sales team is in the middle of an important client demo. CRM and email systems are down. Management is under extreme pressure!

**You are the Senior Network Engineer - solve this crisis quickly!**

---

### Step 1: Crisis Team Formation

#### 1.1 Senior Network Engineer (You) - Admin Role
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alex_senior",
    "email": "alex@techcorp.com",
    "password": "SecureNet2024",
    "password_confirm": "SecureNet2024",
    "role": "admin",
    "department": "Network Operations"
  }'

# Login and get token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alex_senior",
    "password": "SecureNet2024"
  }'

# Save the access token
ADMIN_TOKEN="YOUR_ACCESS_TOKEN_HERE"
```

#### 1.2 Junior Engineer (Support)
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "sara_junior",
    "email": "sara@techcorp.com",
    "password": "JuniorNet123",
    "password_confirm": "JuniorNet123",
    "role": "engineer",
    "department": "Network Support"
  }'
```

#### 1.3 NOC Operator (Monitoring)
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "mike_noc",
    "email": "mike@techcorp.com",
    "password": "NocView2024",
    "password_confirm": "NocView2024",
    "role": "viewer",
    "department": "NOC"
  }'
```

### Step 2: Network Infrastructure Registration

#### 2.1 Core Router (Network Heart)
```bash
curl -X POST http://localhost:8000/api/devices/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "name": "CORE-RTR-MAIN",
    "device_type": "router",
    "ip_address": "192.168.1.1",
    "mac_address": "00:1A:2B:3C:4D:01",
    "location": "Server Room - Rack 1",
    "vendor": "Cisco",
    "model": "ISR4331",
    "os_version": "IOS 15.7",
    "ssh_username": "admin",
    "ssh_password": "TechCorp2024!",
    "description": "Main core router - connects all floors and internet"
  }'
```

#### 2.2 Floor 1 Switch (Development)
```bash
curl -X POST http://localhost:8000/api/devices/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "name": "SW-FLOOR1-DEV",
    "device_type": "switch",
    "ip_address": "192.168.1.10",
    "location": "Floor 1 - Development Area",
    "vendor": "Cisco",
    "model": "Catalyst 2960X",
    "os_version": "IOS 15.2",
    "ssh_username": "admin",
    "ssh_password": "TechCorp2024!",
    "description": "48-port switch for development team"
  }'
```

#### 2.3 Floor 2 Switch (Sales) - Problematic Device
```bash
curl -X POST http://localhost:8000/api/devices/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "name": "SW-FLOOR2-SALES",
    "device_type": "switch",
    "ip_address": "192.168.1.20",
    "location": "Floor 2 - Sales Department",
    "vendor": "HP",
    "model": "ProCurve 2824",
    "os_version": "K.15.18.0014",
    "status": "error",
    "ssh_username": "admin",
    "ssh_password": "TechCorp2024!",
    "description": "24-port switch for sales team - CURRENTLY DOWN!"
  }'
```

#### 2.4 Floor 3 Switch (Management)
```bash
curl -X POST http://localhost:8000/api/devices/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "name": "SW-FLOOR3-MGMT",
    "device_type": "switch",
    "ip_address": "192.168.1.30",
    "location": "Floor 3 - Management Floor",
    "vendor": "Cisco",
    "model": "Catalyst 2960",
    "ssh_username": "admin",
    "ssh_password": "TechCorp2024!",
    "description": "24-port switch for management and IT"
  }'
```

#### 2.5 Perimeter Firewall
```bash
curl -X POST http://localhost:8000/api/devices/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "name": "FW-PERIMETER",
    "device_type": "firewall",
    "ip_address": "192.168.1.2",
    "location": "Server Room - DMZ",
    "vendor": "Fortinet",
    "model": "FortiGate 60E",
    "os_version": "FortiOS 6.4.8",
    "ssh_username": "admin",
    "ssh_password": "TechCorp2024!",
    "description": "Perimeter firewall protecting corporate network"
  }'
```

### Step 3: Initial Problem Diagnosis

#### 3.1 Network Overview
```bash
curl -H "Authorization: Bearer $ADMIN_TOKEN" \
  "http://localhost:8000/api/devices/statistics/"

# Result shows: 4 devices online, 1 device error
```

#### 3.2 Core Router Check
```bash
curl -X POST http://localhost:8000/api/devices/1/commands/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "command": "show ip interface brief"
  }'

# Output: All interfaces are up
```

#### 3.3 Test Connectivity to Problematic Switch
```bash
curl -X POST http://localhost:8000/api/devices/1/commands/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "command": "ping 192.168.1.20"
  }'

# Output: Request timeout - Floor 2 switch not responding!
```

### Step 4: Deep Troubleshooting

#### 4.1 Check Router Logs
```bash
curl -X POST http://localhost:8000/api/devices/1/commands/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "command": "show logging | include Floor2"
  }'

# Observation: Interface GigabitEthernet0/2 is down
```

#### 4.2 Interface Details
```bash
curl -X POST http://localhost:8000/api/devices/1/commands/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "command": "show interface GigabitEthernet0/2"
  }'

# Observation: Interface administratively down
```

#### 4.3 VLAN Check
```bash
curl -X POST http://localhost:8000/api/devices/1/commands/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "command": "show vlan brief"
  }'

# Observation: VLAN 20 (Sales) missing!
```

### Step 5: Emergency Fix

#### 5.1 Enable Interface
```bash
curl -X POST http://localhost:8000/api/devices/1/commands/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "command": "configure terminal; interface GigabitEthernet0/2; no shutdown; exit; exit"
  }'
```

#### 5.2 Recreate VLAN
```bash
curl -X POST http://localhost:8000/api/devices/1/commands/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "command": "configure terminal; vlan 20; name Sales_Department; exit; interface GigabitEthernet0/2; switchport access vlan 20; exit; exit"
  }'
```

#### 5.3 Test Connectivity
```bash
curl -X POST http://localhost:8000/api/devices/1/commands/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "command": "ping 192.168.1.20"
  }'

# Result: Success! 5/5 packets received
```

### Step 6: Role-based Access Testing

#### 6.1 Junior Engineer Permissions Test
```bash
# Login as Junior Engineer
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "sara_junior",
    "password": "JuniorNet123"
  }'

ENG_TOKEN="ENGINEER_TOKEN_HERE"

# Attempt to delete device (should fail with 403)
curl -X DELETE http://localhost:8000/api/devices/1/ \
  -H "Authorization: Bearer $ENG_TOKEN"
```

#### 6.2 NOC Viewer Permissions Test
```bash
# Login as NOC Viewer
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "mike_noc",
    "password": "NocView2024"
  }'

VIEW_TOKEN="VIEWER_TOKEN_HERE"

# Attempt to execute command (should fail with 403)
curl -X POST http://localhost:8000/api/devices/1/commands/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VIEW_TOKEN" \
  -d '{"command": "show version"}'
```

### Step 7: Incident Documentation

#### 7.1 Update Device Status
```bash
curl -X PATCH http://localhost:8000/api/devices/3/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "status": "online",
    "description": "24-port switch for sales team - RESTORED at 09:45 AM"
  }'
```

#### 7.2 View Audit Log
```bash
curl -H "Authorization: Bearer $ADMIN_TOKEN" \
  "http://localhost:8000/api/audit/logs/"

# Review all actions taken during the crisis
```

#### 7.3 Final Statistics
```bash
curl -H "Authorization: Bearer $ADMIN_TOKEN" \
  "http://localhost:8000/api/devices/statistics/"

# Result: 5/5 devices online - 100% uptime restored
```

### Step 8: Crisis Resolution Success

#### 8.1 Full Network Test
```bash
curl -X POST http://localhost:8000/api/devices/execute-bulk-command/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "command": "show clock",
    "device_ids": [1, 2, 3, 4, 5]
  }'

# All devices respond successfully!
```

#### 8.2 Call Sales Team
📞 **"Network is restored. Your demo can continue!"**

### Crisis Resolution Report

#### Performance Metrics
- **🕐 Detection Time**: 5 minutes
- **🔧 Resolution Time**: 15 minutes
- **💰 Prevented Downtime Cost**: $50,000 (Client demo saved)
- **👥 Users Affected**: 60 employees
- **🎯 Success Rate**: 100%

#### Key Achievements
✅ **Rapid Identification**: Using Network Device Manager API  
✅ **Effective Resolution**: Interface and VLAN restoration  
✅ **Team Management**: Role-based access control worked perfectly  
✅ **Full Documentation**: Complete audit trail maintained  
✅ **Prevention**: Better monitoring implemented

## 💡 Usage Examples

### Authentication
```bash
# Register new user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "network_admin",
    "password": "SecurePass123",
    "password_confirm": "SecurePass123",
    "email": "admin@company.com",
    "role": "admin"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "network_admin",
    "password": "SecurePass123"
  }'
```

### Device Management
```bash
# Create device
curl -X POST http://localhost:8000/api/devices/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Router-01",
    "device_type": "router",
    "ip_address": "192.168.1.1",
    "vendor": "Cisco",
    "model": "ISR4331",
    "location": "Data Center"
  }'

# List devices
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/devices/

# Execute command
curl -X POST http://localhost:8000/api/devices/1/commands/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"command": "show version"}'
```

## 🚀 Deployment

### Production Docker Deployment
```bash
# Production environment
docker-compose -f docker-compose.prod.yml up -d

# With SSL/HTTPS (update nginx configuration)
# Configure SSL certificates and update nginx/nginx.conf
```

### Environment Variables
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,localhost
DB_NAME=network_devices
DB_USER=postgres
DB_PASSWORD=secure-password
DB_HOST=localhost
DB_PORT=5432
```

### Health Check
```bash
curl http://localhost:8000/swagger/
# Should return: 200 OK with Swagger UI
```

### Development Setup
```bash
# Local development without Docker
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Django REST Framework for the excellent API framework
- Paramiko for SSH connectivity
- Docker for containerization
- The network engineering community for inspiration

## 📞 Contact

- **Email**: alisalimi6205@yahoo.com
- **GitHub**: [@als138](https://github.com/als138)

---
