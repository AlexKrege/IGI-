from django.urls import path
from agency.views import ReviewListView, ReviewCreateView

app_name = 'reviews'

urlpatterns = [
    path('', ReviewListView.as_view(), name='list'),
    path('create/', ReviewCreateView.as_view(), name='create'),
]