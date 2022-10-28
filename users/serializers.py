from rest_framework import serializers

from users.models import User


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser",
        ]
        read_only_fields = [
            "date_joined",
            "is_active",
            "is_superuser",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
        ]
        read_only_fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
        ]
