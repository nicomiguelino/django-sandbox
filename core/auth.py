from django.contrib.auth import get_user_model
from core.models import GoogleCredentials

User = get_user_model()

class GoogleOAuthBackend:
    def authenticate(self, request, google_email=None):
        if not google_email:
            return None

        try:
            # Try to get user by email
            user = User.objects.get(email=google_email)
            # Verify user has valid Google credentials
            GoogleCredentials.objects.get(user=user)
            return user
        except (User.DoesNotExist, GoogleCredentials.DoesNotExist):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
