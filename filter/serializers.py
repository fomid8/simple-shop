from rest_framework import serializers
from django.contrib.auth.models import User
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
# from django.utils import timezone
# from .documents import *
# from .models import *

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password',
                  'email', 'first_name', 'last_name']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
    category = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())
    created_at = serializers.DateTimeField()