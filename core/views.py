from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json


class IndexView(TemplateView):
    template_name = 'core/index.html'


class IntegrationsView(TemplateView):
    template_name = 'core/integrations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if user has connected Google account
        google_connected = False
        google_email = None

        if self.request.session.get('google_credentials'):
            google_connected = True
            # Get user email using Google People API
            credentials = Credentials(**json.loads(self.request.session['google_credentials']))
            service = build('oauth2', 'v2', credentials=credentials)
            user_info = service.userinfo().get().execute()
            google_email = user_info.get('email')

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
        include_granted_scopes='true'
    )

    request.session['google_oauth_state'] = state
    return redirect(authorization_url)


def google_oauth_callback(request):
    state = request.session['google_oauth_state']

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

    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials

    # Store credentials in session
    request.session['google_credentials'] = json.dumps({
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    })

    return redirect('core:integrations')


def disconnect_google(request):
    if request.method == 'POST':
        if 'google_credentials' in request.session:
            del request.session['google_credentials']
    return redirect('core:integrations')
