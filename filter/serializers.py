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

class CategorySerializer(serializers.Serializer):
    #id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(allow_blank=True)

class OrderedProductSerializer(serializers.Serializer):
    id = serializers.CharField()
    user_id = serializers.CharField()
    product_id = serializers.CharField()
    number = serializers.IntegerField()
    price = serializers.FloatField()
    ordered_at = serializers.DateTimeField()

class CartSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    product_ids = serializers.ListField(child=serializers.CharField())
    numbers = serializers.ListField(child=serializers.IntegerField())
    total_price = serializers.FloatField()
    state = serializers.CharField()
    updated_at = serializers.DateTimeField()