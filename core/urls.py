from django.urls import path
from .views import IndexView, IntegrationsView

app_name = 'core'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('integrations/', IntegrationsView.as_view(), name='integrations'),
]
