import json
import io
import urllib.parse
from datetime import datetime
from calendar import TextCalendar

from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count
from django.urls import reverse_lazy
from django.http import HttpResponse

import matplotlib
matplotlib.use('Agg')  # Использовать backend без GUI
import matplotlib.pyplot as plt
import numpy as np

from news.models import NewsArticle, Glossary, Vacancy, Contact, PrivacyPolicy
from reviews.models import Review
from api.models import Promocode
from properties.models import Property, PropertyCategory, Sale, Application
from .forms import ReviewForm
from django.db.models import Avg, Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class HomeView(TemplateView):
    template_name = 'agency/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['latest_news'] = NewsArticle.objects.order_by('-published_at')[:3]
        ctx['vacancies'] = Vacancy.objects.all()[:5]
        ctx['contacts'] = Contact.objects.all()
        return ctx

class AboutView(TemplateView):
    template_name = 'agency/about.html'

class NewsListView(ListView):
    model = NewsArticle
    template_name = 'agency/news_list.html'
    context_object_name = 'news_list'

class NewsDetailView(DetailView):
    model = NewsArticle
    template_name = 'agency/news_detail.html'

class GlossaryListView(ListView):
    model = Glossary
    template_name = 'agency/glossary_list.html'

class ContactsView(TemplateView):
    template_name = 'agency/contacts.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['contacts'] = Contact.objects.all()
        return ctx

class PrivacyView(TemplateView):
    template_name = 'agency/privacy.html'
    def get_context_data(self, **kwargs):
        obj = PrivacyPolicy.objects.first()
        if not obj:
            obj = PrivacyPolicy.objects.create(content='Страница в разработке')
        return {'content': obj.content}

class VacancyListView(ListView):
    model = Vacancy
    template_name = 'agency/vacancies.html'

class ReviewListView(ListView):
    model = Review
    template_name = 'agency/reviews.html'
    context_object_name = 'reviews'   # лучше явно задать имя

    def get_queryset(self):
        # Показываем только одобренные отзывы, сортируем по дате (сначала новые)
        return Review.objects.filter(is_moderated=True).order_by('-created_at')
    
class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'agency/review_form.html'
    success_url = reverse_lazy('agency:reviews_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.is_moderated = False   # ожидает модерации
        return super().form_valid(form)
    
class PromocodeListView(ListView):
    model = Promocode
    template_name = 'agency/promocodes.html'
    def get_queryset(self):
        from datetime import date
        today = date.today()
        return Promocode.objects.filter(valid_from__lte=today, valid_to__gte=today, is_active=True, archived=False)


# ---- ГРАФИКИ ЧЕРЕЗ MATPLOTLIB ----
def popular_properties_chart(request):
    """График: топ объектов по количеству заявок"""
    top_props = Property.objects.annotate(
        app_count=Count('applications')
    ).filter(app_count__gt=0).order_by('-app_count')[:8]

    if not top_props:
        # Создаём пустое изображение с сообщением
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.text(0.5, 0.5, 'Нет данных по заявкам', ha='center', va='center', fontsize=14)
        ax.axis('off')
    else:
        titles = [p.title[:30] + '...' if len(p.title) > 30 else p.title for p in top_props]
        counts = [p.app_count for p in top_props]
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(titles, counts, color='#8a6de9', edgecolor='#2b1b3e')
        ax.set_title('Самые популярные объекты по заявкам', fontsize=14, fontweight='bold')
        ax.set_xlabel('Объект')
        ax.set_ylabel('Количество заявок')
        plt.xticks(rotation=45, ha='right')
        for bar, count in zip(bars, counts):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(count), ha='center', va='bottom', fontsize=9)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    return HttpResponse(buf, content_type='image/png')


def price_distribution_chart(request):
    """Гистограмма распределения цен на недвижимость"""
    prices = list(Property.objects.filter(is_active=True).values_list('price', flat=True))
    fig, ax = plt.subplots(figsize=(10, 6))

    if not prices:
        ax.text(0.5, 0.5, 'Нет данных о ценах', ha='center', va='center', fontsize=14)
        ax.axis('off')
    else:
        ax.hist(prices, bins=10, color='#4a2c7a', edgecolor='#2b1b3e', alpha=0.7)
        ax.set_title('Распределение цен на недвижимость', fontsize=14, fontweight='bold')
        ax.set_xlabel('Цена (руб.)')
        ax.set_ylabel('Количество объектов')
        ax.grid(True, linestyle='--', alpha=0.5)

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    return HttpResponse(buf, content_type='image/png')


class StatisticsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'agency/statistics.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        # Основные статистические показатели
        avg_price = Property.objects.aggregate(Avg('price'))['price__avg']
        prices = list(Property.objects.filter(price__isnull=False).values_list('price', flat=True).order_by('price'))
        median = prices[len(prices)//2] if prices else 0
        popular_cat = PropertyCategory.objects.annotate(
            sold_count=Count('properties__sales')
        ).order_by('-sold_count').first()

        ctx['avg_price'] = avg_price
        ctx['median_price'] = median
        ctx['popular_category'] = popular_cat

        # Данные для диаграммы продаж по категориям (оставляем для возможного использования)
        chart_data = []
        for cat in PropertyCategory.objects.all():
            count = Sale.objects.filter(property__category=cat).count()
            chart_data.append({'category': cat.name, 'count': count})
        ctx['chart_data_json'] = json.dumps(chart_data)

        return ctx


class CalendarView(TemplateView):
    template_name = 'agency/calendar.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        now = datetime.now()
        cal = TextCalendar()
        ctx['calendar_text'] = cal.formatmonth(now.year, now.month)
        return ctx
    
def popular_categories_chart(request):
    """Круговая диаграмма популярности категорий (по заявкам или по объектам)"""
    from django.db.models import Q

    # Считаем количество заявок по каждой категории через стандартное обратное имя
    categories = PropertyCategory.objects.annotate(
        app_count=Count('application_set')   # используем application_set
    ).order_by('-app_count')

    # Если заявок нет, используем количество активных объектов в категории
    if not categories.filter(app_count__gt=0).exists():
        categories = PropertyCategory.objects.annotate(
            app_count=Count('properties', filter=Q(properties__is_active=True))
        ).order_by('-app_count')

    labels = [cat.name for cat in categories if cat.app_count > 0]
    counts = [cat.app_count for cat in categories if cat.app_count > 0]

    if not labels:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.text(0.5, 0.5, 'Нет данных для построения графика', ha='center', va='center', fontsize=14)
        ax.axis('off')
    else:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        ax.set_title('Популярность категорий недвижимости', fontsize=14, fontweight='bold')
        ax.axis('equal')

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    return HttpResponse(buf, content_type='image/png')