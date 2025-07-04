from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from cloudinary.models import CloudinaryField
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True,null=False,blank=False)
    phone=models.CharField(max_length=10, null=True, blank=True)
    image_profile=CloudinaryField('image',folder="uploads/image_profile", null=True)
    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def get_profile_image(self):
        if self.image_profile and hasattr(self.image_profile, 'url'):
            return self.image_profile.url
        return "https://res.cloudinary.com/dcepg3wpo/image/upload/v1751549320/default_ye2vsv.png"

class UserAddress(models.Model):
    customer=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    city=models.CharField(max_length=100)
    country=CountryField()
    postal_code=models.CharField(max_length=10)
    street_address=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.full_name} - {self.city} - {self.country} - {self.street_address} - {self.postal_code}"

    @property
    def str(self):
        return f"{self.full_name} - {self.city} - {self.country} - {self.street_address} - {self.postal_code}"
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"