from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer untuk memformat data pembayaran.

    Mengubah data transaksi pembayaran digital menjadi format JSON untuk disajikan
    ke klien (berisi channel pembayaran, status, dan url pembayaran).
    """
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('payment_status', 'transaction_id', 'payment_url')

class CreatePaymentSerializer(serializers.Serializer):
    """
    Serializer untuk parameter pembuatan invoice pembayaran.

    Memvalidasi kecukupan parameter input, yaitu ID pesanan pelanggan
    serta kode metode pembayaran (channel_code) yang dipilih.
    """
    order_id = serializers.IntegerField()
    channel_code = serializers.CharField(max_length=50)