from rest_framework import authentication
from rest_framework import exceptions
from django.utils import timezone
from core.models import APIKey

class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')

        if not auth_header:
            return None

        try:
            # Check if header has the correct format "Token <api_key>"
            auth_parts = auth_header.split()
            if len(auth_parts) != 2 or auth_parts[0].lower() != 'token':
                return None

            api_key = auth_parts[1]

            api_key_obj = APIKey.objects.select_related('user').get(
                key=api_key,
                is_active=True
            )

            # Update last used timestamp
            api_key_obj.last_used = timezone.now()
            api_key_obj.save(update_fields=['last_used'])

            return (api_key_obj.user, api_key_obj)

        except APIKey.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid API key')
