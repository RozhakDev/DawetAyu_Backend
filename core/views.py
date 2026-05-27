
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
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="Cek Status Server",
        description="Mengecek status kesehatan server dan konektivitas database (diakses publik).",
        tags=["Sistem"],
        responses={200: OpenApiTypes.OBJECT, 503: OpenApiTypes.OBJECT}
    )
    def get(self, request):
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
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_queryset(self):
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
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)