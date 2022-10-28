from dataclasses import field
from rest_framework import serializers

from products.models import Product
from users.serializers import AccountSerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "description",
            "price",
            "quantity",
            "is_active",
            "seller_id",
        ]
        read_only_fields = [
            "description",
            "price",
            "quantity",
            "is_active",
            "seller_id",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    seller = AccountSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "seller",
            "description",
            "price",
            "quantity",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "seller",
            "is_active",
        ]
