from rest_framework import serializers
from .models import User, Product, Cart

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'quantity']
        read_only_fields = ['user']

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']

        if quantity > product.quantity:
            raise serializers.ValidationError("Недостаточно товара на складе.")

        return data
