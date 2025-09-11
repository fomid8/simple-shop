from django.urls import path
from . import views
#from .views import *
#from django.urls.conf import include
#from rest_framework_nested import routers



urlpatterns = [
    path('hello/', views.hell)
#     path('', views.product_list, name='product_list'),
#     path('products/', ProductsView.as_view(), name='product-list'),
#     path('products/<int:id>/', ProductView.as_view(), name='one-product'),
#     path('orders/', OrdersView.as_view(), name='order-list'),
#     path('orders/<int:id>/', OrderView.as_view(), name='one-order'),
]

'''
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet,
                         basename='product-reviews')
# products_router.register('images', views.ProductImageViewSet,
#                          basename='product-images')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

# URLConf
urlpatterns = router.urls + products_router.urls + carts_router.urls

'''