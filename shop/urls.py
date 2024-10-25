from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('products/', ProductsView.as_view(), name='product-list'),
    path('products/<int:id>/', ProductView.as_view(), name='one-product'),
    path('orders/', OrdersView.as_view(), name='order-list'),
    path('orders/<int:id>/', OrderView.as_view(), name='one-order'),

]