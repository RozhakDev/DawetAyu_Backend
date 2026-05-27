import logging
import json
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.types import OpenApiTypes
from django.db import transaction
from django.conf import settings
from .services import PaymenkuService
from .serializers import CreatePaymentSerializer, PaymentSerializer
from .models import Payment
from orders.models import Order

logger = logging.getLogger(__name__)

@extend_schema_view(
    get=extend_schema(
        summary="Daftar Channel Pembayaran",
        description="Mengambil daftar saluran pembayaran (payment channels) yang didukung oleh Paymenku (misal: VA BCA, QRIS, dll).",
        tags=["Pembayaran Digital"],
        responses={200: OpenApiTypes.OBJECT}
    )
)
class PaymentChannelListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        service = PaymenkuService()
        channels = service.get_payment_channels()
        return Response({"status": "success", "data": channels})
    
@extend_schema_view(
    post=extend_schema(
        summary="Buat Link Pembayaran",
        description="Membuat transaksi pembayaran di Paymenku berdasarkan ID pesanan dan channel pembayaran yang dipilih.",
        tags=["Pembayaran Digital"]
    )
)
class CreatePaymentView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreatePaymentSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data['order_id']
        channel_code = serializer.validated_data['channel_code']
        
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            logger.warning(f"Pembuatan payment gagal (User: {request.user.email}): Pesanan ID {order_id} tidak ditemukan.")
            return Response({"detail": "Pesanan tidak ditemukan."}, status=status.HTTP_404_NOT_FOUND)
        
        if order.payment_status == 'paid':
            logger.info(f"Pembuatan payment dibatalkan (User: {request.user.email}): Pesanan ID {order_id} sudah lunas.")
            return Response({"detail": "Pesanan ini sudah dibayar."}, status=status.HTTP_400_BAD_REQUEST)
        
        return_url = f"{settings.FRONTEND_RETURN_URL}?order_id={order.id}"
        
        service = PaymenkuService()
        trx_data = service.create_transaction(order, channel_code, return_url)

        logger.info(f"Link pembayaran berhasil dibuat (Order ID: {order.id}, Trx ID: {trx_data['trx_id']}, Channel: {channel_code})")

        payment = Payment.objects.create(
            order=order,
            transaction_id=trx_data['trx_id'],
            payment_channel=channel_code,
            payment_status=trx_data['status'],
            payment_url=trx_data['pay_url']
        )

        order.payment_status = 'pending'
        order.save()

        response_serializer = PaymentSerializer(payment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
@extend_schema_view(
    post=extend_schema(
        summary="Webhook Callback (Paymenku)",
        description="*Endpoint internal* yang digunakan oleh server Paymenku untuk mengirim notifikasi status pembayaran (sukses/gagal). Tidak memerlukan Bearer Token.",
        tags=["Pembayaran Digital"],
        request=OpenApiTypes.OBJECT,
        responses={200: OpenApiTypes.OBJECT, 401: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT}
    )
)
class PaymenkuWebhookView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        signature = request.headers.get('X-PaymenKu-Signature')
        timestamp = request.headers.get('X-PaymenKu-Timestamp')
        raw_body = request.body.decode('utf-8')

        if not PaymenkuService.verify_webhook_signature(signature, timestamp, raw_body):
            logger.warning(f"Webhook Paymenku ditolak: Signature tidak valid! (Trx ID potensial: {json.loads(raw_body).get('trx_id', 'Unknown')})")
            return Response({"detail": "Invalid signature"}, status=status.HTTP_401_UNAUTHORIZED)
        
        payload = json.loads(raw_body)
        event = payload.get('event')
        trx_id = payload.get('trx_id')
        payment_status = payload.get('status')

        if event != 'payment.status_updated':
            logger.info(f"Webhook Paymenku diabaikan: Event '{event}' tidak relevan.")
            return Response({"detail": "Event diabaikan"}, status=status.HTTP_200_OK)
        
        with transaction.atomic():
            try:
                payment = Payment.objects.select_for_update().get(transaction_id=trx_id)
                order = Order.objects.select_for_update().get(id=payment.order.id)
                
                payment.payment_status = payment_status
                payment.save()
                
                order.payment_status = payment_status
                if payment_status == 'paid':
                    order.order_status = 'processing'
                elif payment_status in ['expired', 'failed', 'cancelled']:
                    order.order_status = 'cancelled'
                    
                order.save()
                logger.info(f"Webhook sukses: Transaksi {trx_id} diupdate ke status '{payment_status}'.")

            except Payment.DoesNotExist:
                logger.error(f"Webhook error: Transaksi {trx_id} tidak ditemukan di database!")
                return Response({"detail": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"status": "success"}, status=status.HTTP_200_OK)