from django.urls import re_path
from . import views

app_name = 'properties'

urlpatterns = [
    re_path(r'^$', views.PropertyListView.as_view(), name='list'),
    re_path(r'^(?P<pk>\d+)/$', views.PropertyDetailView.as_view(), name='detail'),
    re_path(r'^create/$', views.PropertyCreateView.as_view(), name='create'),
    re_path(r'^(?P<pk>\d+)/update/$', views.PropertyUpdateView.as_view(), name='update'),
    re_path(r'^(?P<pk>\d+)/delete/$', views.PropertyDeleteView.as_view(), name='delete'),

    # Заявки
    re_path(r'^apply/$', views.CreateApplicationView.as_view(), name='apply'),
    re_path(r'^applications/$', views.ApplicationListView.as_view(), name='application_list'),
    re_path(r'^applications/(?P<pk>\d+)/$', views.ApplicationDetailView.as_view(), name='application_detail'),
    re_path(r'^applications/(?P<pk>\d+)/update/$', views.ApplicationUpdateView.as_view(), name='application_update'),
    re_path(r'^applications/(?P<pk>\d+)/delete/$', views.ApplicationDeleteView.as_view(), name='application_delete'),
]