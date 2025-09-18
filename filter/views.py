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
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and (request.user.is_staff or str(obj) == str(request.user.id))


def hell(requst):
    return HttpResponse('hello')

class UserView(generics.ListAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']

class ProductListView(views.APIView):
    permission_classes = [IsAdminOrReadOnly]

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
    permission_classes = [IsAdminOrReadOnly]
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
    
class CategoryListView(views.APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        query = request.query_params.get('q')
        categories = search_categories(query)
        return Response(categories)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            cat = create_category(serializer.validated_data)
            return Response(cat, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryView(views.APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get_object(self, name):
        try:
            return CategoryDocument.get(id=name.lower())
        except Exception:
            return None

    def get(self, request, name):
        category = self.get_object(name)
        if category:
            return Response(category.to_dict())
        return Response({'error': 'Category not found'}, status=404)

    def put(self, request, name):
        category = self.get_object(name)
        if not category:
            return Response({'error': 'Category not found'}, status=404)

        serializer = CategorySerializer(category.to_dict(), data=request.data, partial=True)
        if serializer.is_valid():
            for field, value in serializer.validated_data.items():
                setattr(category, field, value)
            category.save()
            return Response(category.to_dict())
        return Response(serializer.errors, status=400)

    def delete(self, request, name):
        category = self.get_object(name)
        if not category:
            return Response({'error': 'Category not found'}, status=404)

        category.delete()
        return Response({"message": f"Category {name} deleted"}, status=status.HTTP_204_NO_CONTENT)

class CartListView(views.APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        filters = {
            'min_price': request.query_params.get('min_price'),
            "max_price": request.query_params.get("max_price"),
            "product": request.query_params.get("product"),
            'state': request.query_params.get('state'),
            "start_date": request.query_params.get("start_date"),
            "end_date": request.query_params.get("end_date"),
        }

        sort_by = request.query_params.get("sort_by")
        sort_cart = request.query_params.get("sort_cart", "asc") 

        carts = search_carts(filters, sort_by, sort_cart)
        return Response(carts)
    
class CartView(views.APIView):
    permission_classes = [IsOwnerOrAdmin]
    def get(self, request, user_id):
        self.check_object_permissions(request, user_id)
        cart = get_cart(user_id)
        if cart:
            return Response(cart.to_dict())
        return Response({"message": "Cart is empty"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id):
        self.check_object_permissions(request, user_id)
        cleared = clear_cart(user_id)
        if cleared:
            return Response({"message": "Cart cleared"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

class OrderListView(views.APIView):
    permission_classes = [IsOwnerOrAdmin]

    def get(self, request):
        filters = {
            'user': request.query_params.get('user'),
            'min_price': request.query_params.get('min_price'),
            "max_price": request.query_params.get("max_price"),
            "product": request.query_params.get("product"),
            "start_date": request.query_params.get("start_date"),
            "end_date": request.query_params.get("end_date"),
        }

        sort_by = request.query_params.get("sort_by") #number, price, product
        sort_order = request.query_params.get("sort_order", "asc") 
        allowed_orders = []
        orders = search_orders(filters, sort_by, sort_order)
        for order in orders:
            try:
                self.check_object_permissions(request, order)  # از IsOwnerOrAdmin استفاده می‌شود
                allowed_orders.append(order)
            except permissions.PermissionDenied:
                continue
        return Response(orders)

    def post(self, request):
        self.check_object_permissions(request, request.data['user_id'])
        serializer = OrderedProductSerializer(data=request.data)
        if serializer.is_valid():
            order = create_order(serializer.validated_data)
            return Response(order, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrderView(views.APIView):
    permission_classes = [IsOwnerOrAdmin]
    def get_object(self, order_id):
        try:
            return OrderedProductDocument.get(id=order_id)
        except Exception:
            return None

    def get(self, request, order_id):
        user_id = order_id.split('-')[0]
        self.check_object_permissions(request, user_id)
        order = self.get_object(order_id)
        if order:
            return Response(order.to_dict())
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, order_id):
        user_id = order_id.split('-')[0]
        self.check_object_permissions(request, user_id)
        order = self.get_object(order_id)
        if not order:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response({"message": f"Order {order_id} deleted"}, status=status.HTTP_204_NO_CONTENT)

class PaymentView(views.APIView):
    permission_classes = [IsOwnerOrAdmin]
    def post(self, request, user_id):
        self.check_object_permissions(request, user_id)
        cleared = clear_cart(user_id)
        if cleared:
            return Response({"message": "Payment successful"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
