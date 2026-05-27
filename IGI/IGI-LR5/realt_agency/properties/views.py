from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .models import Property, Application
from .forms import ApplicationForm
from api.utils import get_usd_rate

# === Недвижимость ===
class PropertyListView(ListView):
    model = Property
    template_name = 'properties/list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().filter(is_active=True)
        search = self.request.GET.get('search')
        sort = self.request.GET.get('sort', 'price')
        if search:
            qs = qs.filter(title__icontains=search) | qs.filter(address__icontains=search)
        if sort in ['price', '-price', 'area', '-area', 'rooms']:
            qs = qs.order_by(sort)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['current_sort'] = self.request.GET.get('sort', 'price')
        ctx['search_term'] = self.request.GET.get('search', '')
        return ctx

class PropertyDetailView(DetailView):
    model = Property
    template_name = 'properties/detail.html'

class PropertyCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Property
    fields = ['title', 'category', 'address', 'price', 'area', 'rooms', 'description', 'image']
    template_name = 'properties/form.html'
    success_url = reverse_lazy('properties:list')
    def test_func(self):
        return self.request.user.is_staff
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class PropertyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Property
    fields = ['title', 'category', 'address', 'price', 'area', 'rooms', 'description', 'image', 'is_active']
    template_name = 'properties/form.html'
    success_url = reverse_lazy('properties:list')
    def test_func(self):
        return self.request.user.is_staff

class PropertyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Property
    template_name = 'properties/confirm_delete.html'
    success_url = reverse_lazy('properties:list')
    def test_func(self):
        return self.request.user.is_staff

# === Заявки ===
class CreateApplicationView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'properties/application_form.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            return HttpResponseForbidden("Администраторы не могут подавать заявки.")
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('properties:application_list')

class ApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'properties/application_list.html'
    context_object_name = 'applications'
    paginate_by = 10
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_choices'] = Application.STATUS_CHOICES
        ctx['current_status'] = self.request.GET.get('status', '')
        return ctx

class ApplicationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Application
    template_name = 'properties/application_detail.html'
    def test_func(self):
        obj = self.get_object()
        return self.request.user.is_staff or obj.user == self.request.user

class ApplicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Application
    fields = ['status']
    template_name = 'properties/application_form.html'
    success_url = reverse_lazy('properties:application_list')
    def test_func(self):
        return self.request.user.is_staff
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Изменение статуса заявки'
        return ctx

class ApplicationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Application
    template_name = 'properties/application_confirm_delete.html'
    success_url = reverse_lazy('properties:application_list')

    def test_func(self):
        obj = self.get_object()
        if self.request.user.is_staff:
            return True
        return obj.user == self.request.user and obj.status == 'pending'
    

class PropertyDetailView(DetailView):
    model = Property
    template_name = 'properties/detail.html'

    def get_context_data(self, **kwargs):
        print("Курс USD:", get_usd_rate())
        ctx = super().get_context_data(**kwargs)
        usd_rate = get_usd_rate()
        if usd_rate:
            ctx['price_usd'] = round(float(ctx['object'].price) / usd_rate) if usd_rate else None
        else:
            ctx['price_usd'] = None
        return ctx