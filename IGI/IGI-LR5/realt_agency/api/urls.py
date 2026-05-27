from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('async-rates/', views.AsyncRatesView.as_view(), name='async_rates'),
    path('sync-rates/', views.SyncRatesView.as_view(), name='sync_rates'),
]