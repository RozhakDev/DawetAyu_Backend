from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer

import logging

User = get_user_model()
logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info(f"Registrasi berhasil: Pengguna {user.email} (Role: {user.role}) baru saja mendaftar.")

class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
    
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

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