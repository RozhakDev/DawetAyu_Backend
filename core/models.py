from django.db import models
from django.utils.translation import gettext_lazy as _

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(TimeStampedModel):
    name = models.CharField(_('nama kategori'), max_length=100, unique=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Product(TimeStampedModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT,
        related_name='products',
        verbose_name=_('kategori')
    )
    name = models.CharField(_('nama produk'), max_length=200)
    description = models.TextField(_('deskripsi produk'), blank=True)
    price = models.PositiveIntegerField(_('harga'))
    stock = models.PositiveIntegerField(_('stok'), default=0)
    image = models.ImageField(_('gambar produk'), upload_to='products/', null=True, blank=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} - Rp{self.price}"