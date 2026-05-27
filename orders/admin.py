from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Order, OrderItem

class OrderItemInline(TabularInline):
    """
    Tampilan detail item belanja secara inline di panel admin.

    Menampilkan informasi produk, jumlah, dan subtotal item belanjaan
    secara langsung di dalam halaman edit pesanan utama.
    """
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'subtotal')
    can_delete = False

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    """
    Pengaturan tampilan panel admin untuk model Order.

    Mengatur tampilan ringkasan daftar transaksi pesanan, kolom filter status,
    dan penyertaan tabel detail item belanjaan.
    """
    list_display = ('id', 'user', 'total_price', 'payment_status', 'order_status', 'created_at')
    search_fields = ('id', 'user__name', 'user__email')
    list_filter = ('payment_status', 'order_status', 'created_at')
    readonly_fields = ('user', 'total_price')
    inlines = [OrderItemInline]