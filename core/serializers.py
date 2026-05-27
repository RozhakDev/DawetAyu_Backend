from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer untuk konversi data kategori.

    Mengubah objek kategori Dawet Ayu menjadi representasi JSON yang memuat
    informasi ID dan nama kategori.
    """
    class Meta:
        model = Category
        fields = ('id', 'name')

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer untuk konversi data produk.

    Mengubah objek produk Dawet Ayu ke format JSON lengkap dengan informasi
    detail dan kategori relasinya.
    """
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'category', 'name', 'description', 'price', 'stock', 'image')