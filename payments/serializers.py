from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('payment_status', 'transaction_id', 'payment_url')

class CreatePaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    channel_code = serializers.CharField(max_length=50)
    return_url = serializers.URLField(default="https://ayupay.com/success")