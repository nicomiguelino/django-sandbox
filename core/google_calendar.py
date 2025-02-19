from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle
from django.conf import settings
import datetime
import json

def get_calendar_service(request):
    # Get credentials from session
    if 'google_credentials' not in request.session:
        return None

    credentials = Credentials(**json.loads(request.session['google_credentials']))
    return build('calendar', 'v3', credentials=credentials)

def list_upcoming_events(request, max_results=10):
    service = get_calendar_service(request)
    if not service:
        return []

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])
