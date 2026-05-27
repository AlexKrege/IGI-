from django.db import models
from accounts.models import User

property_type = models.ForeignKey('PropertyCategory', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Тип недвижимости', related_name='applications')

class PropertyCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Property(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(PropertyCategory, on_delete=models.CASCADE, related_name='properties')
    address = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    area = models.DecimalField(max_digits=8, decimal_places=2)
    rooms = models.IntegerField()
    description = models.TextField()
    # Только сотрудники (администраторы) могут быть владельцами
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='owned_properties', 
        limit_choices_to={'is_staff': True}
    )
    image = models.ImageField(upload_to='properties/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Sale(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='sales')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_properties')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sold_properties')
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='agent_sales')
    sale_price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_date = models.DateField()
    contract_date = models.DateField()

class ClientInterest(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interests')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='interested_clients')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('client', 'property')

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрена'),
        ('rejected', 'Отклонена'),
    ]
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='applications')
    property_type = models.ForeignKey('PropertyCategory', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Тип недвижимости')
    budget = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Бюджет (руб.)')
    rooms = models.IntegerField(verbose_name='Количество комнат')
    floor = models.IntegerField(null=True, blank=True, verbose_name='Этаж')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.property_type} - {self.budget} руб."