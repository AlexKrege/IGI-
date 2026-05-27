from django.contrib import admin
from .models import PropertyCategory, Property, Sale, ClientInterest, Application

@admin.register(PropertyCategory)
class PropertyCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'address', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'address')
    raw_id_fields = ('owner',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('property', 'buyer', 'seller', 'sale_price', 'sale_date')

@admin.register(ClientInterest)
class ClientInterestAdmin(admin.ModelAdmin):
    list_display = ('client', 'property', 'created_at')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'property_type', 'budget', 'rooms', 'status', 'created_at')  # исправлено
    list_filter = ('status', 'property_type')
    search_fields = ('user__username', 'property_type__name')
    actions = ['approve_applications', 'reject_applications']

    def approve_applications(self, request, queryset):
        queryset.update(status='approved')
    approve_applications.short_description = "Одобрить выбранные заявки"

    def reject_applications(self, request, queryset):
        queryset.update(status='rejected')
    reject_applications.short_description = "Отклонить выбранные заявки"