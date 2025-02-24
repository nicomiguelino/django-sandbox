from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.conf import settings
from django.urls import reverse
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
from .google_calendar import list_upcoming_events
from django.contrib.auth import get_user_model, login, logout
from core.models import GoogleCredentials
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

class IntegrationsView(TemplateView):
    template_name = 'core/integrations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if user has connected Google account
        google_connected = False
        google_email = None

        if self.request.session.get('google_credentials'):
            try:
                credentials = Credentials(**json.loads(self.request.session['google_credentials']))
                service = build('oauth2', 'v2', credentials=credentials)
                user_info = service.userinfo().get().execute()
                google_email = user_info.get('email')
                google_connected = True
            except Exception:
                # If there's any error with the credentials, clear them and treat as disconnected
                if 'google_credentials' in self.request.session:
                    del self.request.session['google_credentials']
                google_connected = False
                google_email = None

        context.update({
            'google_connected': google_connected,
            'google_email': google_email,
        })
        return context


def google_oauth_init(request):
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE,
        scopes=[
            'openid',
            'https://www.googleapis.com/auth/calendar.readonly',
            'https://www.googleapis.com/auth/userinfo.email'
        ],
        redirect_uri=request.build_absolute_uri(reverse('core:google_oauth_callback'))
    )

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )

    request.session['google_oauth_state'] = state
    return redirect(authorization_url)


def google_oauth_callback(request):
    state = request.session['google_oauth_state']
    # Get the authorization code from the request
    auth_code = request.GET.get('code')

    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CLIENT_SECRETS_FILE,
        scopes=[
            'openid',
            'https://www.googleapis.com/auth/calendar.readonly',
            'https://www.googleapis.com/auth/userinfo.email'
        ],
        state=state,
        redirect_uri=request.build_absolute_uri(reverse('core:google_oauth_callback'))
    )

    # Store the authorization code in the session if needed
    request.session['google_auth_code'] = auth_code

    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials

    # Get user info from Google
    service = build('oauth2', 'v2', credentials=credentials)
    user_info = service.userinfo().get().execute()
    email = user_info['email']

    # Create user if doesn't exist
    User = get_user_model()
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'username': email,
            'is_active': True
        }
    )

    # Store or update credentials in database
    creds_data = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    google_creds, _ = GoogleCredentials.objects.update_or_create(
        user=user,
        defaults=creds_data
    )

    # Also store in session for immediate use if needed
    request.session['google_credentials'] = json.dumps(creds_data)

    # Log in the user
    login(request, user, backend='core.auth.GoogleOAuthBackend')

    return redirect('core:integrations')


def disconnect_google(request):
    if request.method == 'POST':
        if 'google_credentials' in request.session:
            del request.session['google_credentials']
            logout(request)
    return redirect('core:integrations')


def calendar_view(request):
    if 'google_credentials' not in request.session:
        return redirect('core:google_oauth_init')

    events = list_upcoming_events(request)
    return render(request, 'core/calendar.html', {'events': events})


@method_decorator(login_required, name='dispatch')
class SettingsView(TemplateView):
    template_name = 'core/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add API keys to context
        context['api_keys'] = self.request.user.api_keys.filter(is_active=True).order_by('-created_at')

        # Check if user has connected Google account
        google_email = None
        if self.request.session.get('google_credentials'):
            try:
                credentials = Credentials(**json.loads(self.request.session['google_credentials']))
                service = build('oauth2', 'v2', credentials=credentials)
                user_info = service.userinfo().get().execute()
                google_email = user_info.get('email')
            except Exception:
                if 'google_credentials' in self.request.session:
                    del self.request.session['google_credentials']

        context['google_email'] = google_email
        return context
