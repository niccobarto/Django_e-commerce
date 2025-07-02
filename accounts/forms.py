from django import forms
from .models import UserAddress
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm
from .models import CustomUser


class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields=['username','password']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class']='form-control'


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=["username","first_name","last_name","email","password1","password2","phone"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class']='form-control'
            if self.errors.get(field_name):
                field.widget.attrs['class']+='form-control is-invalid'

class CustomUserChangeForm(UserChangeForm):
    password=None
    class Meta:
        model=CustomUser
        fields=['username','first_name','last_name','email','phone','image_profile']


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