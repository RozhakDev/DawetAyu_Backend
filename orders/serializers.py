import logging
from rest_framework import serializers
from django.db import transaction
from .models import Order, OrderItem
from core.models import Product

logger = logging.getLogger(__name__)

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer untuk menampilkan daftar produk yang dipesan.

    Mengubah data detail item pesanan menjadi format JSON yang memuat informasi
    nama produk, kuantitas, dan nilai subtotal.
    """
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'quantity', 'subtotal')
        read_only_fields = ('subtotal',)

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer untuk membaca ringkasan pesanan.

    Menampilkan informasi status pembayaran, status pengerjaan pesanan,
    total harga belanja, serta seluruh daftar item pesanan.
    """
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'total_price', 'payment_status', 'order_status', 'created_at', 'items')
        read_only_fields = ('user', 'total_price', 'payment_status', 'order_status')

class CreateOrderItemSerializer(serializers.Serializer):
    """
    Serializer masukan untuk detail item yang dibeli.

    Memvalidasi parameter ID produk dan jumlah kuantitas produk yang dipesan
    oleh pelanggan.
    """
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class CreateOrderSerializer(serializers.Serializer):
    """
    Serializer untuk pembuatan transaksi pesanan baru (checkout).

    Mengelola validasi produk, perhitungan total harga, pembuatan record transaksi,
    dan pengurangan stok secara aman dalam satu transaksi database (atomic).
    """
    items = CreateOrderItemSerializer(many=True)

    def create(self, validated_data):
        """
        Menangani logika pembuatan pesanan dan penyesuaian stok produk.

        Args:
            validated_data (dict): Data item belanjaan yang telah tervalidasi.

        Returns:
            Order: Objek transaksi pesanan yang berhasil dibuat.

        Raises:
            ValidationError: Jika produk tidak ditemukan atau stok tidak mencukupi.
        """
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        with transaction.atomic():
            order = Order.objects.create(user=user, total_price=0)
            total_price = 0

            for item_data in items_data:
                try:
                    product = Product.objects.select_for_update().get(id=item_data['product_id'])
                except Product.DoesNotExist:
                    raise serializers.ValidationError(f"Produk dengan ID {item_data['product_id']} tidak ditemukan.")
                
                if product.stock < item_data['quantity']:
                    logger.warning(f"Pesanan ditolak (User: {user.email}): Stok produk '{product.name}' (ID: {product.id}) tidak mencukupi. Diminta: {item_data['quantity']}, Tersedia: {product.stock}")
                    raise serializers.ValidationError(f"Stok untuk '{product.name}' tidak mencukupi.")
                
                subtotal = product.price * item_data['quantity']
                total_price += subtotal

                product.stock -= item_data['quantity']
                product.save()

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item_data['quantity'],
                    subtotal=subtotal
                )

            order.total_price = total_price
            order.save()

        return order