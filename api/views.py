from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from core.models import GoogleCredentials
from core.google_calendar import list_upcoming_events
from google.oauth2.credentials import Credentials
from django.conf import settings

class IndexView(APIView):
    def get(self, request):
        return Response({'message': 'Hello, World!'})

@api_view(['GET'])
@permission_classes([AllowAny])
def get_calendar_events(request):
    # Get API key from request header
    api_key = request.headers.get('X-API-Key')

    # Validate API key (you should store this securely in settings)
    if api_key != settings.KIOSK_API_KEY:
        return Response({'error': 'Invalid API key'}, status=401)

    # Get credentials for a specific user (you'll need to decide which user's calendar to use)
    google_creds = GoogleCredentials.objects.filter(user__email='your-designated-user@example.com').first()

    if not google_creds:
        return Response({'error': 'No credentials found'}, status=404)

    # Create credentials object
    credentials = Credentials(
        token=google_creds.token,
        refresh_token=google_creds.refresh_token,
        token_uri=google_creds.token_uri,
        client_id=google_creds.client_id,
        client_secret=google_creds.client_secret,
        scopes=google_creds.scopes
    )

    # Get events using your existing function
    events = list_upcoming_events(credentials)

    return Response({'events': events})
