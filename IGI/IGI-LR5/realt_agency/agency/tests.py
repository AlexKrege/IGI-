from django.test import TestCase
from django.urls import reverse
from news.models import NewsArticle

class HomeViewTest(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('agency:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'agency/home.html')

    def test_statistics_view(self):
        response = self.client.get(reverse('agency:statistics'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Статистика агентства')