from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from core.models import APIKey, GoogleCredentials
from core.google_calendar import list_upcoming_events
from google.oauth2.credentials import Credentials
from django.conf import settings
from .serializers import APIKeySerializer


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


class GenerateAPIKeyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get('name', '').strip()
        if not name:
            return Response(
                {'error': 'Key name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        api_key = APIKey.objects.create(
            user=request.user,
            key=APIKey.generate_key(),
            name=name
        )

        serializer = APIKeySerializer(api_key)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DeleteAPIKeyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, key_id):
        try:
            api_key = APIKey.objects.get(
                id=key_id,
                user=request.user,
                is_active=True
            )
            api_key.is_active = False
            api_key.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except APIKey.DoesNotExist:
            return Response(
                {'error': 'API key not found'},
                status=status.HTTP_404_NOT_FOUND
            )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_endpoint(request):
    return Response({
        'message': f'Hello {request.user.email}!',
        'api_key_name': request.auth.name  # request.auth contains the APIKey instance
    })
