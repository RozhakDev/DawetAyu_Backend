import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Order
from .serializers import OrderSerializer, CreateOrderSerializer

logger = logging.getLogger(__name__)

@extend_schema_view(
    get=extend_schema(
        summary="Riwayat Pesanan",
        description="Melihat seluruh daftar riwayat pesanan (order) milik pengguna yang sedang login.",
        tags=["Manajemen Pesanan"]
    ),
    post=extend_schema(
        summary="Buat Pesanan Baru (Checkout)",
        description="Membuat pesanan baru berdasarkan daftar item produk (keranjang). Endpoint ini akan otomatis mengurangi stok produk.",
        tags=["Manajemen Pesanan"]
    )
)
class OrderListCreateView(generics.ListCreateAPIView):
    """
    Layanan pengelolaan transaksi pesanan pelanggan.

    Mengakomodasi pengambilan riwayat transaksi pesanan (GET) dan pembuatan
    transaksi pesanan belanja baru (POST) bagi pelanggan terautentikasi.
    """
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Mengambil daftar riwayat pesanan milik pelanggan yang sedang aktif.

        Returns:
            QuerySet: Daftar pesanan yang terhubung dengan produk yang dibeli.
        """
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')
    
    def get_serializer_class(self):
        """
        Menentukan kelas serializer berdasarkan metode HTTP.

        Returns:
            Serializer: CreateOrderSerializer untuk POST, atau OrderSerializer untuk GET.
        """
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Membuat transaksi pesanan baru dari input keranjang belanja.

        Args:
            request (Request): Objek request dari klien.

        Returns:
            Response: Data JSON detail pesanan yang berhasil dibuat.
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        logger.info(f"Pesanan berhasil dibuat (Order ID: {order.id}, User: {request.user.email}, Total: Rp {order.total_price})")

        response_serializer = OrderSerializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
@extend_schema_view(
    get=extend_schema(
        summary="Detail Pesanan",
        description="Melihat detail spesifik dari sebuah pesanan, termasuk daftar produk yang dibeli dan total harganya.",
        tags=["Manajemen Pesanan"]
    )
)
class OrderDetailView(generics.RetrieveAPIView):
    """
    Layanan tampilan rincian pesanan.

    Menyajikan rincian item belanjaan dan total biaya untuk satu nomor pesanan
    tertentu milik pelanggan aktif.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        """
        Mengambil filter data pesanan spesifik milik pelanggan aktif.

        Returns:
            QuerySet: Objek query pesanan terfilter.
        """
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')