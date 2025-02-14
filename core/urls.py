from django.urls import path
from .views import IndexView, IntegrationsView
from . import views

app_name = 'core'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('integrations/', IntegrationsView.as_view(), name='integrations'),
    path('google/init/', views.google_oauth_init, name='google_oauth_init'),
    path('google/callback/', views.google_oauth_callback, name='google_oauth_callback'),
    path('google/disconnect/', views.disconnect_google, name='disconnect_google'),
]
