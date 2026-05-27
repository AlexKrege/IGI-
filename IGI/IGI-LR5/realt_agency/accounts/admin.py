from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, EmployeeProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'birth_date', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Доп. информация', {'fields': ('phone', 'birth_date')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(EmployeeProfile)