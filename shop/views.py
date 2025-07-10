from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Product, Cart
from .serializers import ProductSerializer, CartSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]  # Только админ может создавать
        return [permissions.AllowAny()]  # Все могут просматривать

class CartListCreateView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]