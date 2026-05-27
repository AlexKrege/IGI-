from django.urls import path
from . import views

app_name = 'agency'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('glossary/', views.GlossaryListView.as_view(), name='glossary'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('vacancies/', views.VacancyListView.as_view(), name='vacancies'),
    path('reviews/', views.ReviewListView.as_view(), name='reviews_list'),
    path('reviews/create/', views.ReviewCreateView.as_view(), name='review_create'),
    path('promocodes/', views.PromocodeListView.as_view(), name='promocodes'),
    path('statistics/', views.StatisticsView.as_view(), name='statistics'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('statistics/popular-chart/', views.popular_properties_chart, name='popular_chart'),
    path('statistics/price-chart/', views.price_distribution_chart, name='price_chart'),
    path('reviews/', views.ReviewListView.as_view(), name='reviews_list'),
    path('reviews/create/', views.ReviewCreateView.as_view(), name='review_create'),    
    path('statistics/categories-chart/', views.popular_categories_chart, name='categories_chart'),
]