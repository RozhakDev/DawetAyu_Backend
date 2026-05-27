from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = ('transaction_id', 'order', 'payment_channel', 'payment_status', 'created_at')
    search_fields = ('transaction_id', 'order__id', 'order__user__name')
    list_filter = ('payment_status', 'payment_channel', 'created_at')
    
    readonly_fields = ('order', 'transaction_id', 'payment_channel', 'payment_status', 'payment_url')