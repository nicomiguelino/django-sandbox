from django.contrib import admin
from .models import APIKey, GoogleCredentials

@admin.register(GoogleCredentials)
class GoogleCredentialsAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        # Prevent manual creation through admin as credentials should only be created through OAuth
        return False

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'name', 'created_at', 'last_used', 'is_active')
    list_filter = ('created_at', 'last_used', 'is_active')
    search_fields = ('user__email', 'user__username', 'name')
    readonly_fields = ('created_at', 'last_used')

