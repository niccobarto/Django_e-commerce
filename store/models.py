from django.db import models
from django.db.models import CASCADE
import datetime
import enum
from django.conf import settings
from django.contrib.auth.models import AbstractUser

#Shipment enum
class ShipmentStatus(enum.Enum):
    PENDING = "PENDING"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    LOST = "LOST"

    @classmethod
    def choices(cls):
        return [(status.name, status.value) for status in cls]

# Create your models here.

#The product's categories
class Category(models.Model):
    name=models.CharField(max_length=20)
    def __str__(self):
        return self.name

#The products available in the store
class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    price=models.DecimalField(default=0,decimal_places=2,max_digits=6)
    front_image=models.ImageField(upload_to="uploads/product")
    description=models.CharField(max_length=500, default="", blank=True, null=True)
    def __str__(self):
        return self.name

#Orders of a product
class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=CASCADE)
    customer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE)
    quantity=models.IntegerField(default=1)
    address=models.CharField(max_length=100)
    datetime=models.DateTimeField(default=datetime.datetime.today)
    status=models.CharField(choices=ShipmentStatus.choices())

