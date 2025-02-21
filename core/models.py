from django.conf import settings
from django.db import models

class GoogleCredentials(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='google_credentials'
    )
    token = models.TextField()
    refresh_token = models.TextField(null=True, blank=True)
    token_uri = models.TextField()
    client_id = models.TextField()
    client_secret = models.TextField()
    scopes = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Google Credential'
        verbose_name_plural = 'Google Credentials'

    def __str__(self):
        return f'Google credentials for {self.user.email}'
