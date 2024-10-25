from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    description = models.TextField(default="empty")
    # photo = 

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'#{self.id}, user:{self.user.id}'