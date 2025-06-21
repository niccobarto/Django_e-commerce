from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
# Create your models here.

class CustomUser(AbstractUser):
    phone=models.CharField(max_length=10, null=True, blank=True)

class UserAddress(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    city=models.CharField(max_length=100)
    country=CountryField()
    postal_code=models.CharField(max_length=10)
    street_address=models.CharField(max_length=100)