from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at', 'is_moderated')
    list_filter = ('rating', 'is_moderated')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_moderated=True)
    approve_reviews.short_description = "Одобрить отзывы"