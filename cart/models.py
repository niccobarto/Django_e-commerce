from django.db import models
from django.db.models import CASCADE
from store.models import Product
from accounts.models import CustomUser
import datetime
from django_countries.fields import CountryField

SHIPMENT_STATUS=[
    ("PENDING","PENDING"),
    ("IN_TRANSIT","IN_TRANSIT"),
    ("DELIVERED","DELIVERED"),
    ("LOST","LOST"),
]
# Create your models here.

class CartItem(models.Model):
    customer=models.ForeignKey(CustomUser, on_delete=CASCADE)
    product=models.ForeignKey(Product,on_delete=CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} - {self.product.name} - {self.customer.username}"

#Invece di mettere una foreignkey su UserAddress lo copiamo. Questo perché se poi l'indirizzo utilizzato venisse copiato
#lo storico ordini muterebbe
class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=CASCADE)
    total_price=models.DecimalField(max_digits=10, decimal_places=2)
    datetime = models.DateTimeField(default=datetime.datetime.today)
    status = models.CharField(choices=SHIPMENT_STATUS, default="PENDING")
    shipment_city = models.CharField(max_length=100)
    shipment_country = CountryField()
    shipment_postal_code = models.CharField(max_length=10)
    shipment_street_address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user} - {self.total_price} - {self.shipment_city}"

    @property
    def user(self):
        return self.customer.username


class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=CASCADE)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} - {self.order.customer.username}"