from django.shortcuts import render
from django.http import *
from .models import *
from django.views import *
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import json

# Create your views here.
def product_list(request):
    return render(request, 'shop/product_list.html', {'title': 'Homepage','username': 'Fateme',})
    #return HttpResponse("Welcome to the homepage!")


class ProductsView(View):
    #get a list of all products
    def get(self, request):
        products = Product.objects.all().values()
        # print(products)
        return JsonResponse(list(products), safe=False)
    
    #create a product, only admin have access
    def post(self, request):
        data = json.loads(request.body)
        product = Product.objects.create(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            category=data['category']
        )
        return JsonResponse({'id': product.id, 'message': 'Product created'}, status=201)


class ProductView(View):
    #find product by id
    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            return HttpResponseNotFound({'error': 'Product not found'})
        
    #get a product detail by id
    def get(self, request, id):
        data = self.get_object(id)
        product={
            'name':data.name,
            'description':data.description,
            'price':data.price,
            'category':data.category}
        return JsonResponse(product)
    
    #delete a product by id, only admin have access
    def delete(self, request, id):
        product = self.get_object(id)
        product.delete()
        return JsonResponse({'message':'Product deleted'})

    #edit a product detail by id, only admin have access
    def put(self, request, id):
        data = json.loads(request.body)
        product = self.get_object(id)
        product.name = data['name']
        product.description = data['description']
        product.price = data['price']
        product.category = data['category']
        product.save()
        return JsonResponse({'message': 'Product updated'})


class OrdersView(View):
    #get all orders
    def get(self, request):
        orders = Order.objects.all().values()
        return JsonResponse(list(orders), safe=False)

    #create an order
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(id=data['user_id'])
            product = Product.objects.get(id=data['product_id'])
            order = Order.objects.create(user=user, product=product)
            return JsonResponse({'id': order.id, 'message': 'Order created'}, status=201)
        except (User.DoesNotExist, Product.DoesNotExist):
            return JsonResponse({'error': 'user or product not found'}, status=404)


class OrderView(View):
    #find order by id
    def get_object(self, id):
        try:
            return Order.objects.get(id=id)
        except Order.DoesNotExist:
            return HttpResponseNotFound({'error': 'Order not found'})
        
    #get orders by its user_id
    def get(self, request, id):
        try:
            orders = Order.objects.filter(user = id).values()
            return JsonResponse(list(orders), safe=False)
        except (User.DoesNotExist):
            return JsonResponse({'error': 'user not found'}, status=404)

    #make an order paid and final by its id
    def patch(self, request, id):
        data = json.loads(request.body)
        order = self.get_object(id)
        order.paid = data['paid']
        order.save()
        return JsonResponse({'message': 'Order updated'})

    #delete an order by id
    def delete(self, request, id):
        order = self.get_object(id)
        order.delete()
        return JsonResponse({'message':'Product deleted'})
        






# filterquery = Q()
# if data['name']: filterquery &= Q(name=data['name'])
# if data['category']: filterquery &= Q(category=data['category'])
# products = Product.objects.filter(filterquery)