from django.db import models
from django.utils.translation import gettext_lazy as _

class TimeStampedModel(models.Model):
    """
    Model dasar dengan pencatatan waktu otomatis.

    Menyediakan kolom 'created_at' dan 'updated_at' untuk mencatat kapan
    data dibuat dan terakhir kali diperbarui.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(TimeStampedModel):
    """
    Kategori untuk pengelompokan produk Dawet Ayu.

    Digunakan untuk mengelompokkan berbagai menu produk, seperti minuman utama,
    makanan ringan, atau menu musiman.
    """
    name = models.CharField(_('nama kategori'), max_length=100, unique=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """
        Mengembalikan nama dari kategori produk.

        Returns:
            str: Nama kategori.
        """
        return self.name
    
class Product(TimeStampedModel):
    """
    Informasi produk menu Dawet Ayu yang ditawarkan.

    Menyimpan seluruh data detail menu, termasuk nama produk, deskripsi,
    harga jual, jumlah stok, dan foto produk.
    """
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
        """
        Mengembalikan gabungan nama produk dan informasi harganya.

        Returns:
            str: Nama produk disertai format harga rupiah.
        """
        return f"{self.name} - Rp{self.price}"