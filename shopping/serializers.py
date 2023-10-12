from rest_framework import serializers
from .models import Cart, OrderDetailsModel, OrderModel
from customer.serializers import CustomerSerializer
from product.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    customer = CustomerSerializer()

    class Meta:
        model = Cart
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer

    class Meta:
        model = OrderModel
        fields = "__all__"


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetailsModel
        fields = "__all__"
