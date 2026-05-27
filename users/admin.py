import contextlib
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth.models import Group
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from unfold.admin import ModelAdmin
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'role')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'role')

@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin, BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'name', 'role', 'is_staff', 'is_active')
    search_fields = ('email', 'name')
    list_filter = ('role', 'is_staff', 'is_active')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'role', 'password', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

models_to_hide = [Group, OutstandingToken, BlacklistedToken]

for model in models_to_hide:
    with contextlib.suppress(NotRegistered):
        admin.site.unregister(model)