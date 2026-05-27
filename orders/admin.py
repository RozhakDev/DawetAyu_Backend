from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Order, OrderItem

class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'subtotal')
    can_delete = False

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'payment_status', 'order_status', 'created_at')
    search_fields = ('id', 'user__name', 'user__email')
    list_filter = ('payment_status', 'order_status', 'created_at')
    readonly_fields = ('user', 'total_price')
    inlines = [OrderItemInline]