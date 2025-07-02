from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields=['name','category','price','description','front_image','quantity','is_active']