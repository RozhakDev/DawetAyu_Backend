
from rest_framework import generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.db import connection
from django.utils import timezone
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class HealthCheckView(APIView):
    """
    Pemeriksaan status kesehatan sistem.

    Digunakan oleh layanan monitoring untuk memantau apakah server backend
    dan basis data terhubung dengan normal.
    """
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="Cek Status Server",
        description="Mengecek status kesehatan server dan konektivitas database (diakses publik).",
        tags=["Sistem"],
        responses={200: OpenApiTypes.OBJECT, 503: OpenApiTypes.OBJECT}
    )
    def get(self, request):
        """
        Endpoint health check untuk memvalidasi ketersediaan layanan API
        dan koneksi database.

        Args:
            request (Request): Request HTTP dari klien.

        Returns:
            Response: Status kesehatan sistem dan database.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
            db_ok = True
        except Exception:
            db_ok = False

        return Response(
            {
                "status": "healthy" if db_ok else "unhealthy",
                "details": {
                    "database": "connected" if db_ok else "disconnected"
                },
                "timestamp": timezone.now().isoformat()
            },
            status=status.HTTP_200_OK if db_ok else status.HTTP_503_SERVICE_UNAVAILABLE
        )

@extend_schema_view(
    get=extend_schema(
        summary="Daftar Kategori",
        description="Mengambil semua kategori menu Dawet Ayu yang tersedia. Endpoint ini dapat diakses publik.",
        tags=["Katalog Dawet Ayu"]
    )
)
class CategoryListView(generics.ListAPIView):
    """
    Layanan untuk melihat daftar kategori produk.

    Menampilkan seluruh pengelompokan menu Dawet Ayu yang tersedia dalam sistem.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)

@extend_schema_view(
    get=extend_schema(
        summary="Katalog Produk",
        description="Mengambil seluruh menu produk Dawet Ayu. Mendukung pencarian (search) dan filter berdasarkan kategori (category_id).",
        tags=["Katalog Dawet Ayu"],
        parameters=[
            OpenApiParameter(name='category', description='Filter berdasarkan ID Kategori', required=False, type=int),
            OpenApiParameter(name='search', description='Cari berdasarkan nama atau deskripsi produk', required=False, type=str)
        ]
    )
)
class ProductListView(generics.ListAPIView):
    """
    Layanan katalog produk Dawet Ayu.

    Menyediakan daftar menu Dawet Ayu dengan dukungan pencarian kata kunci
    serta filter kategori produk.
    """
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_queryset(self):
        """
        Mengambil query produk yang aktif dan sesuai filter.

        Returns:
            QuerySet: Daftar produk terfilter sesuai parameter request.
        """
        queryset = Product.objects.select_related('category').all()

        category_id = self.request.query_params.get('category', None)
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)

        return queryset
    
@extend_schema_view(
    get=extend_schema(
        summary="Detail Produk",
        description="Mengambil detail spesifik dari satu produk Dawet Ayu berdasarkan ID.",
        tags=["Katalog Dawet Ayu"]
    )
)
class ProductDetailView(generics.RetrieveAPIView):
    """
    Layanan pencarian detail produk.

    Menyajikan informasi mendalam untuk satu produk Dawet Ayu berdasarkan parameter ID.
    """
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)