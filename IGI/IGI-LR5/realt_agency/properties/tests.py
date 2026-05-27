from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from properties.models import PropertyCategory, Property

class PropertyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='123', birth_date='1980-01-01')
        self.cat = PropertyCategory.objects.create(name='Квартира')

    def test_property_creation(self):
        prop = Property.objects.create(
            title='Тест', category=self.cat, price=1000, address='ул. Тест',
            area=50, rooms=2, owner=self.user
        )
        self.assertEqual(prop.title, 'Тест')
        self.assertTrue(prop.is_active)

    def test_list_view(self):
        Property.objects.create(title='Квартира', category=self.cat, price=50000,
                                address='ул. Ленина', area=60, rooms=3, owner=self.user)
        response = self.client.get(reverse('properties:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Квартира')