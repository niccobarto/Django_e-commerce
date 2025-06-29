from django.db import models
from django.db.models import CASCADE
import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

#The product's categories
class Category(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self):
        return self.name

#The products available in the store
class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name=models.CharField(max_length=50)
    price=models.DecimalField(default=0,decimal_places=2,max_digits=6)
    front_image=models.ImageField(upload_to="uploads/product")
    description=models.CharField(max_length=500, default="", blank=True, null=True)
    quantity=models.PositiveIntegerField(default=0)
    is_active=models.BooleanField(default=True)
    def __str__(self):
        return self.name

