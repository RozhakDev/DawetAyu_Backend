from rest_framework import serializers
from django.db import transaction
from .models import Order, OrderItem
from core.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'quantity', 'subtotal')
        read_only_fields = ('subtotal',)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'total_price', 'payment_status', 'order_status', 'created_at', 'items')
        read_only_fields = ('user', 'total_price', 'payment_status', 'order_status')

class CreateOrderItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class CreateOrderSerializer(serializers.Serializer):
    items = CreateOrderItemSerializer(many=True)

    def create(self, validated_data):
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
                    raise serializers.ValidationError(f"Stok untuk '{product.name}' tidak mencukupi. Sisa stok: {product.stock}")
                
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