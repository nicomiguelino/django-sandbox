from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.models import APIKey, GoogleCredentials
from core.google_calendar import list_upcoming_events
from google.oauth2.credentials import Credentials
from django.conf import settings
from .serializers import APIKeySerializer
import json
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime


class IndexView(APIView):
    def get(self, request):
        return Response({'message': 'Hello, World!'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_calendar_events(request):
    # Get credentials for a specific user
    google_creds = GoogleCredentials.objects.filter(user__email=request.user.email).first()

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

    # Check if credentials are expired and refresh if needed
    if not credentials.valid:
        try:
            credentials.refresh(Request())

            # Update stored credentials in database only
            google_creds.token = credentials.token
            google_creds.refresh_token = credentials.refresh_token
            google_creds.token_uri = credentials.token_uri
            google_creds.client_id = credentials.client_id
            google_creds.client_secret = credentials.client_secret
            google_creds.scopes = credentials.scopes

            google_creds.save()
        except Exception as e:
            return Response({'error': 'Failed to refresh token'}, status=401)

    calendar_service = build('calendar', 'v3', credentials=credentials)
    events_result = calendar_service.events().list(
        calendarId='primary',
        timeMin=datetime.now().isoformat() + 'Z',
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return Response({'events': events_result})


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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_google_token(request):
    """Get a valid Google access token, refreshing if necessary."""

    google_creds = GoogleCredentials.objects.filter(user=request.user).first()

    if not google_creds:
        return Response(
            {'error': 'No Google credentials found. Please connect your Google account first.'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Create credentials object
    credentials = Credentials(
        token=google_creds.token,
        refresh_token=google_creds.refresh_token,
        token_uri=google_creds.token_uri,
        client_id=google_creds.client_id,
        client_secret=google_creds.client_secret,
        scopes=google_creds.scopes,
        # Convert expiry to naive datetime if it's timezone-aware
        expiry=google_creds.expiry.replace(tzinfo=None) if google_creds.expiry else None,
    )

    # Always try to refresh the token to ensure it's valid
    if not credentials.refresh_token:
        return Response(
            {'error': 'No refresh token available. Please reconnect your Google account.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        if not credentials.valid:
            credentials.refresh(Request())

            # Update stored credentials
            google_creds.token = credentials.token
            google_creds.refresh_token = credentials.refresh_token
            google_creds.token_uri = credentials.token_uri
            google_creds.client_id = credentials.client_id
            google_creds.client_secret = credentials.client_secret
            google_creds.scopes = credentials.scopes
            google_creds.expiry = credentials.expiry
            google_creds.save()

    except Exception as e:
        return Response(
            {'error': f'Failed to refresh token: {str(e)}'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Verify the token by making a test API call
    try:
        service = build('oauth2', 'v2', credentials=credentials)
        service.userinfo().get().execute()  # Test API call
    except Exception as e:
        return Response(
            {'error': f'Token verification failed: {str(e)}'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    return Response({
        'access_token': credentials.token,
        'expires_at': credentials.expiry.isoformat() if credentials.expiry else None
    })
