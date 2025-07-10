from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import ProductListCreateView
from .views import CartListCreateView
from .views import ProductDeleteView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('cart/', CartListCreateView.as_view(), name='cart'),
    path('products/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),]