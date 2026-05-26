from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from core.views import HealthCheckView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/v1/health/', HealthCheckView.as_view(), name='health_check'),

    path('api/v1/', include('users.urls')),
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]