from django.urls import path
from .views import *

urlpatterns = [
    path('hello/', hell),
    path('users/', UserView.as_view(), name='user-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:id>/', ProductView.as_view(), name='one-product'),
]

