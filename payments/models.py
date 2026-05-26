from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel
from orders.models import Order

class Payment(TimeStampedModel):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('expired', 'Expired'),
        ('failed', 'Failed'),
    )

    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE,
        related_name='payments'
    )
    transaction_id = models.CharField(
        _('transaction ID Paymenku'), 
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        db_index=True
    )
    payment_channel = models.CharField(_('metode pembayaran'), max_length=50, blank=True)
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    payment_url = models.URLField(_('URL pembayaran'), max_length=500, blank=True)

    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.transaction_id} - Order #{self.order.id} ({self.get_payment_status_display()})"