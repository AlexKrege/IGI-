from django.contrib import admin
from .models import NewsArticle, Glossary, Vacancy, Contact, PrivacyPolicy

admin.site.register(NewsArticle)
admin.site.register(Glossary)
admin.site.register(Vacancy)
admin.site.register(Contact)
admin.site.register(PrivacyPolicy)