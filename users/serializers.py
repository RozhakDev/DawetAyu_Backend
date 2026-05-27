from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer untuk mengelola data profil pengguna.

    Mengubah objek pengguna menjadi format JSON untuk menampilkan informasi profil
    seperti nama, email, role, dan tanggal registrasi.
    """
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'role', 'created_at')
        read_only_fields = ('email', 'role', 'created_at')

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer untuk pendaftaran akun pelanggan baru.

    Memvalidasi informasi pendaftaran seperti nama, email, dan kata sandi,
    serta menangani pembuatan akun pelanggan baru.
    """
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password')

    def create(self, validated_data):
        """
        Membuat record pengguna baru sebagai pelanggan.

        Args:
            validated_data (dict): Data input pendaftaran yang telah tervalidasi.

        Returns:
            CustomUser: Objek pengguna baru yang berhasil terdaftar.
        """
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            role='customer'
        )
        return user