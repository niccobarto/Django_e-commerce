from django.db import models
from django.db.models import CASCADE
from store.models import Product
from accounts.models import CustomUser

# Create your models here.

class CartItem(models.Model):
    customer=models.ForeignKey(CustomUser, on_delete=CASCADE)
    product=models.ForeignKey(Product,on_delete=CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} - {self.product.name} - {self.customer.username}"
