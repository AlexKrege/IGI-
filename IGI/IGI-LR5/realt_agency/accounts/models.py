from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from datetime import date
from django.core.exceptions import ValidationError

phone_regex = RegexValidator(
    regex=r'^\+375 \(29\) \d{3}-\d{2}-\d{2}$',
    message='Телефон должен быть в формате +375 (29) XXX-XX-XX'
)
phone = models.CharField(validators=[phone_regex], max_length=20, blank=True)

class User(AbstractUser):
    phone = models.CharField(validators=[phone_regex], max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    # Явные related_name для избежания конфликтов
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='accounts_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='accounts_user_set',
        blank=True,
    )

    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None

    def clean(self):
        if self.age is not None and self.age < 18:
            raise ValidationError('Возраст должен быть 18+')

    def __str__(self):
        return self.username

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    position = models.CharField(max_length=100)
    hired_date = models.DateField()

    def clean(self):
        if self.user.age is not None and self.user.age < 18:
            raise ValidationError('Сотрудник должен быть 18+')