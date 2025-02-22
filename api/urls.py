from django.urls import path
from . import views

app_name = 'api'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('calendar/events/', views.get_calendar_events, name='get_calendar_events'),
]
