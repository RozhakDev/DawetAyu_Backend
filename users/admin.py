from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display = ('email', 'name', 'role', 'is_staff', 'is_active')
    search_fields = ('email', 'name')
    list_filter = ('role', 'is_staff', 'is_active')
    ordering = ('-created_at',)