from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock')
    search_fields = ('name', 'description')
    list_filter = ('category',)