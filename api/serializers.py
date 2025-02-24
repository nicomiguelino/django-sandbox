from rest_framework import serializers
from core.models import APIKey

class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = ['id', 'key', 'name', 'created_at']
        read_only_fields = ['id', 'key', 'created_at']
