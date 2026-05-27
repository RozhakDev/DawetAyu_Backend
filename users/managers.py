from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Manajer kustom untuk model data CustomUser.

    Menyediakan method bantuan untuk membuat akun pelanggan biasa maupun
    akun superuser (administrator) sistem.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Membuat dan menyimpan akun pengguna (pelanggan) baru.

        Args:
            email (str): Alamat email unik pengguna.
            password (str): Kata sandi untuk login.
            **extra_fields: Data tambahan opsional lainnya.

        Returns:
            CustomUser: Objek user yang berhasil disimpan ke database.

        Raises:
            ValueError: Jika email kosong atau tidak diberikan.
        """
        if not email:
            raise ValueError(_('Email wajib diisi'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Membuat dan menyimpan akun administrator (superuser) baru.

        Args:
            email (str): Alamat email unik administrator.
            password (str): Kata sandi untuk login.
            **extra_fields: Data tambahan opsional lainnya.

        Returns:
            CustomUser: Objek user administrator yang berhasil disimpan.

        Raises:
            ValueError: Jika is_staff atau is_superuser tidak bernilai True.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser harus memiliki is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser harus memiliki is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)