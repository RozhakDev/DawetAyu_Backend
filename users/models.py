from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Model data pengguna kustom untuk sistem AyuPay.

    Menggunakan alamat email sebagai identitas utama login (autentikasi) dan
    membedakan akses berdasarkan peran (admin atau customer).
    """
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
    )

    name = models.CharField(_('nama'), max_length=255)
    email = models.EmailField(_('alamat email'), unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        """
        Mengembalikan nama dan alamat email pengguna.

        Returns:
            str: Nama pengguna disertai email dalam tanda kurung.
        """
        return f"{self.name} ({self.email})"