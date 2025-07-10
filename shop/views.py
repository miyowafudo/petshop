from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Product, Cart
from .serializers import ProductSerializer, CartSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, Product
from rest_framework.permissions import IsAuthenticated

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

class BuyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"detail": "Корзина пуста."}, status=status.HTTP_400_BAD_REQUEST)

        errors = []

        for item in cart_items:
            if item.quantity > item.product.quantity:
                errors.append(f"Недостаточно товара: {item.product.name}")

        if errors:
            return Response({"detail": "Проблемы с покупкой", "errors": errors},
                            status=status.HTTP_400_BAD_REQUEST)

        for item in cart_items:
            product = item.product
            product.quantity -= item.quantity
            product.save()

        cart_items.delete()

        return Response({"detail": "Покупка прошла успешно!"}, status=status.HTTP_200_OK)