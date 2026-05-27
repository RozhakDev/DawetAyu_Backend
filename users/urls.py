from django.urls import path
from .views import RegisterView, ProfileView, LogoutView, CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    
    path('profile/', ProfileView.as_view(), name='profile'),
]