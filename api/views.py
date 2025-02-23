from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import APIKey
from .serializers import APIKeySerializer

class IndexView(APIView):
    def get(self, request):
        return Response({'message': 'Hello, World!'})

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
