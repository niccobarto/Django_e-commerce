from django.db import models
from django.db.models import CASCADE
from store.models import Product
from accounts.models import CustomUser
import datetime
from django_countries.fields import CountryField

SHIPMENT_STATUS=[
    ("PENDING","PENDING"),
    ("IN_TRANSIT","IN TRANSIT"),
    ("DELIVERED","DELIVERED"),
    ("LOST","LOST"),
]

# Create your models here.

#Invece di mettere una foreignkey su UserAddress lo copiamo. Questo perché se poi l'indirizzo utilizzato venisse copiato
#lo storico ordini muterebbe
class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=CASCADE)
    total_price=models.DecimalField(max_digits=10, decimal_places=2)
    datetime = models.DateTimeField(default=datetime.datetime.today)
    status = models.CharField(choices=SHIPMENT_STATUS, default="PENDING")
    shipment_first_name = models.CharField(max_length=100)
    shipment_last_name = models.CharField(max_length=100)
    shipment_city = models.CharField(max_length=100)
    shipment_country = CountryField()
    shipment_postal_code = models.CharField(max_length=10)
    shipment_street_address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user} - {self.total_price} - {self.shipment_city}"

    @property
    def address_str(self):
        return f"{self.full_name} - {self.shipment_city} - {self.shipment_country} - {self.shipment_postal_code} - {self.shipment_street_address}"

    @property
    def full_name(self):
        return f"{self.shipment_first_name} {self.shipment_last_name}"
    @property
    def user(self):
        return self.customer.username


class OrderItem(models.Model):
    order=models.ForeignKey(Order, related_name='items',on_delete=CASCADE)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True)
    product_name = models.CharField(max_length=100)
    product_image = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} - {self.quantity} - {self.order.customer.username}"
    def subtotal(self):
        return self.price * self.quantity