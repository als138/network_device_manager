import json
from django.utils.deprecation import MiddlewareMixin
from django.contrib.contenttypes.models import ContentType
from .models import AuditLog

class AuditMiddleware(MiddlewareMixin):
    """
    Middleware to log user actions for auditing purposes.
    """

    def process_request(self, request):
        # Store request data for later use in response processing
        request._audit_data = {
            'ip_address': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        }

    def process_response(self, request, response):
        # Log specific actions based on the request
        if hasattr(request, 'user') and request.user.is_authenticated:
            self.log_action(request, response)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def log_action(self, request, response):
        # Only log successful API calls
        if response.status_code < 400 and request.path.startswith('/api/'):
            
            action = None
            object_repr = ""
            changes = None
            additional_data = {}

            # Determine action type based on HTTP method and path
            if request.method == 'POST':
                if 'login' in request.path:
                    action = 'LOGIN'
                elif 'logout' in request.path:
                    action = 'LOGOUT'
                elif 'commands' in request.path or 'execute' in request.path:
                    action = 'EXECUTE'
                else:
                    action = 'CREATE'
            elif request.method in ['PUT', 'PATCH']:
                action = 'UPDATE'
            elif request.method == 'DELETE':
                action = 'DELETE'

            # Create audit log entry
            if action:
                try:
                    # Try to parse response data for object information
                    if hasattr(response, 'data') and response.data:
                        if isinstance(response.data, dict):
                            object_repr = str(response.data.get('name', response.data.get('id', '')))
                            additional_data = {
                                'endpoint': request.path,
                                'method': request.method,
                                'status_code': response.status_code
                            }

                    AuditLog.objects.create(
                        user=request.user,
                        action=action,
                        object_repr=object_repr,
                        changes=changes,
                        ip_address=request._audit_data['ip_address'],
                        user_agent=request._audit_data['user_agent'],
                        additional_data=additional_data
                    )
                except Exception:
                    # Don't let audit logging break the application
                    pass
