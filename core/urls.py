from django.urls import path
from core.views import HealthCheckView
from .views import CategoryListView, ProductListView, ProductDetailView

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health_check'),
    
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]