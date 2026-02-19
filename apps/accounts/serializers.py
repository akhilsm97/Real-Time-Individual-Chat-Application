from accounts.models import CustomUser
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers


class CustomUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
