from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel, Product

class Order(TimeStampedModel):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    ORDER_STATUS_CHOICES = (
        ('waiting', 'Menunggu Pembayaran'),
        ('processing', 'Diproses'),
        ('ready', 'Siap Diambil'),
        ('completed', 'Selesai'),
        ('cancelled', 'Dibatalkan'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='orders',
        verbose_name=_('customer')
    )
    total_price = models.PositiveIntegerField(_('total pembayaran'), default=0)
    payment_status = models.CharField(
        max_length=20, 
        choices=PAYMENT_STATUS_CHOICES, 
        default='pending',
        db_index=True
    )
    order_status = models.CharField(
        max_length=20, 
        choices=ORDER_STATUS_CHOICES, 
        default='waiting',
        db_index=True
    )

    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.name} ({self.get_order_status_display()})"
    
class OrderItem(TimeStampedModel):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.RESTRICT, 
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(_('jumlah'))
    subtotal = models.PositiveIntegerField(_('subtotal'))

    class Meta:
        db_table = 'order_items'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Order #{self.order.id})"