from django.db import models

class NewsArticle(models.Model):
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=300)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True)
    published_at = models.DateTimeField(auto_now_add=True)

class Glossary(models.Model):
    term = models.CharField(max_length=100)
    definition = models.TextField()
    added_at = models.DateField(auto_now_add=True)

class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.CharField(max_length=100, blank=True)

class Contact(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    photo = models.ImageField(upload_to='contacts/', blank=True)

class PrivacyPolicy(models.Model):
    content = models.TextField(default='Страница политики конфиденциальности')
    updated_at = models.DateField(auto_now=True)