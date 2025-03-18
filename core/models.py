from django.conf import settings
from django.db import models

class GoogleCredentials(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='google_credentials'
    )
    token = models.TextField()
    expiry = models.DateTimeField(null=True, blank=True)
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

class APIKey(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='api_keys'
    )
    key = models.CharField(max_length=64, unique=True, db_index=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'API Key'
        verbose_name_plural = 'API Keys'

    def __str__(self):
        return f'{self.name} ({self.key[:8]}...)'

    @classmethod
    def generate_key(cls):
        import secrets
        while True:
            key = secrets.token_hex(32)  # 64 character hex string
            if not cls.objects.filter(key=key).exists():
                return key
