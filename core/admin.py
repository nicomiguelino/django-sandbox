from django.contrib import admin
from .models import GoogleCredentials

@admin.register(GoogleCredentials)
class GoogleCredentialsAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        # Prevent manual creation through admin as credentials should only be created through OAuth
        return False
