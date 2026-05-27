from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    """
    Pengaturan tampilan panel admin untuk kategori.

    Menentukan kolom yang tampil serta fitur pencarian untuk model kategori
    pada halaman panel admin.
    """
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    """
    Pengaturan tampilan panel admin untuk produk.

    Mengelola tampilan daftar produk, fitur pencarian, dan penyaringan produk
    berdasarkan kategori pada halaman panel admin.
    """
    list_display = ('name', 'category', 'price', 'stock')
    search_fields = ('name', 'description')
    list_filter = ('category',)