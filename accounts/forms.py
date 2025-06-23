from django import forms
from .models import UserAddress
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=["username","email","password1","password2","phone"]

class UserAddressForm(forms.ModelForm):
    class Meta:
        model=UserAddress
        fields=["first_name","last_name","city","country","postal_code","street_address",]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',  # stile Bootstrap
                'placeholder': field.label,  # segnaposto dinamico
            })