from django.shortcuts import render

from django.http import *
from .models import *
from .documents import *
from .serializers import *
from .services import *
from django.views import *
from rest_framework import viewsets, views, status, generics, permissions, filters
from rest_framework.response import Response
from django.contrib.auth.models import User


# Create your views here.

def hell(requst):
    return HttpResponse('hello')

class UserView(generics.ListAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']

class ProductListView(views.APIView):
    def get(self, request):
        filters = {
            'category': request.query_params.get('category'),
            'min_price': request.query_params.get('min_price'),
            "max_price": request.query_params.get("max_price"),
            "name": request.query_params.get("name"),
            "description": request.query_params.get("description"),
        }

        sort_by = request.query_params.get("sort_by")          # price, created_at, name
        sort_order = request.query_params.get("sort_order", "asc") 

        products = search_products(filters, sort_by, sort_order)
        return Response(products)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                product = create_product(serializer.validated_data)
                return Response(product, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductView(views.APIView):
    def get_object(self, id):
        try:
            return ProductDocument.get(id=id)
        except Exception:
            return None

    def get(self, request, id):
        product = self.get_object(id)
        if product:
            return Response(product.to_dict())
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product.to_dict(), data=request.data, partial=True)
        if serializer.is_valid():
            for field, value in serializer.validated_data.items():
                setattr(product, field, value)
            product.save()
            return Response(product.to_dict())
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        product = self.get_object(id)
        if not product:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({"message": f"Product with id {id} deleted"}, status=status.HTTP_204_NO_CONTENT)
    