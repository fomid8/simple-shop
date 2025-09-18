from django.urls import path
from .views import *

urlpatterns = [
    path('hello/', hell),
    path('users/', UserView.as_view(), name='user-list'),
    path('products/', ProductListView.as_view(), name='product-list-create'),
    path('products/<int:id>/', ProductView.as_view(), name='product-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list-create'),
    path('categories/<str:name>/', CategoryView.as_view(), name='category-detail'),
    path('orders/', OrderListView.as_view(), name='order-list-search'),
    path('orders/<str:order_id>/', OrderView.as_view(), name='order-detail'),
    path('carts/', CartListView.as_view(), name='cart-list'),
    path('carts/<str:user_id>/', CartView.as_view(), name='cart-detail'),
    path('carts/<str:user_id>/pay/', PaymentView.as_view(), name='orders-pay'),
]

