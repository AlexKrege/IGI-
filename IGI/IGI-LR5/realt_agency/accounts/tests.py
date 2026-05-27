from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user_with_valid_data(self):
        user = User.objects.create_user(
            username='testuser',
            password='pass123',
            phone='+375 (29) 123-45-67',
            birth_date=date(1990, 1, 1)
        )
        self.assertEqual(user.age, date.today().year - 1990)
        self.assertTrue(user.check_password('pass123'))

    def test_user_age_validation(self):
        user = User(username='young', birth_date=date(2010, 1, 1))
        with self.assertRaises(Exception):
            user.full_clean()

class AuthViewsTest(TestCase):
    def test_register_view_get(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')