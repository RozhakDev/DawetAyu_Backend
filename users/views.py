import logging
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()
logger = logging.getLogger(__name__)

@extend_schema_view(
    post=extend_schema(
        summary="Registrasi Pelanggan Baru",
        description="Mendaftarkan akun baru untuk pelanggan aplikasi AyuPay.",
        tags=["Autentikasi"]
    )
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info(f"Registrasi berhasil: Pengguna {user.email} (Role: {user.role}) baru saja mendaftar.")

@extend_schema_view(
    get=extend_schema(
        summary="Lihat Profil Pengguna",
        description="Mengambil data profil pengguna yang sedang login.",
        tags=["Profil Pengguna"]
    ),
    put=extend_schema(
        summary="Perbarui Profil (Keseluruhan)",
        description="Memperbarui seluruh data profil pengguna yang sedang login.",
        tags=["Profil Pengguna"]
    ),
    patch=extend_schema(
        summary="Perbarui Profil (Sebagian)",
        description="Memperbarui sebagian data profil pengguna yang sedang login.",
        tags=["Profil Pengguna"]
    )
)
class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

@extend_schema_view(
    post=extend_schema(
        summary="Login / Masuk Akun",
        description="Melakukan autentikasi menggunakan kredensial (email & password) untuk mendapatkan Access Token dan Refresh Token JWT.",
        tags=["Autentikasi"]
    )
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema_view(
    post=extend_schema(
        summary="Perbarui Access Token (Refresh)",
        description="Mendapatkan Access Token baru menggunakan Refresh Token yang masih berlaku.",
        tags=["Autentikasi"]
    )
)
class CustomTokenRefreshView(TokenRefreshView):
    pass

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Logout / Keluar Akun",
        description="Mengakhiri sesi pengguna dengan melakukan blacklist pada refresh token JWT.",
        tags=["Autentikasi"],
        request=OpenApiTypes.OBJECT,
        responses={205: OpenApiTypes.OBJECT, 400: OpenApiTypes.OBJECT}
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                logger.warning(f"Logout gagal: Refresh token tidak dikirim (User: {request.user.email}).")
                return Response({"detail": "Refresh token wajib dikirim."}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"Logout berhasil: Pengguna {request.user.email} telah keluar.")
            return Response({"detail": "Logout berhasil."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.warning(f"Logout gagal (User: {request.user.email}): Token invalid atau expired. Error: {str(e)}")
            return Response({"detail": "Token tidak valid atau sudah expired."}, status=status.HTTP_400_BAD_REQUEST)