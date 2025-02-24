from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('calendar/events/', views.get_calendar_events, name='get_calendar_events'),
    path('keys/generate/', views.GenerateAPIKeyView.as_view(), name='generate_key'),
    path('keys/<int:key_id>/delete/', views.DeleteAPIKeyView.as_view(), name='delete_key'),
    path('protected/', views.protected_endpoint, name='protected_endpoint'),
    path('google/token/', views.get_google_token, name='get-google-token'),
]
