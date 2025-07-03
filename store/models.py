from django.db import models
from django.db.models import CASCADE
import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

# Create your models here.

#The product's categories
class Category(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self):
        return self.name

#The products available in the store
class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name=models.CharField(max_length=100)
    price=models.DecimalField(default=0,decimal_places=2,max_digits=6,blank=False,null=False)
    front_image=CloudinaryField('image',folder="uploads/product",null=False,blank=False)
    description=models.CharField(max_length=500, default="", blank=True, null=True)
    quantity=models.PositiveIntegerField(default=0)
    is_active=models.BooleanField(default=True)
    discount=models.DecimalField(default=0,decimal_places=2,max_digits=6,blank=False,null=False)
    def __str__(self):
        return self.name

    def discounted_price(self):
        if 0 < self.discount < self.price:
            return self.price - self.discount
        return self.price
    def is_discounted(self):
        return self.discount > 0
    def discount_percent(self):
        if 0 < self.discount < self.price:
            percent = (self.discount / self.price) * 100
            return round(percent)
        return 0