from django import forms
from .models import UserAddress
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=["username","email","password1","password2","phone"]

class UserAddressForm(forms.ModelForm):
    model=UserAddress
    fields=["username","city","country","postal_code","street_address",]