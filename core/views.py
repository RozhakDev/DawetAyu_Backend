from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db import connection
from django.utils import timezone

class HealthCheckView(APIView):
    permission_classes = (AllowAny,)

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