from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Product

# Create your views here.

def home(request):
    products=Product.objects.all()
    return render(request, 'store/home.html', {"products":products})

def product_detail(request,product_id):
    product=Product.objects.get(pk=product_id)
    return render(request, 'store/product_detail.html', {"product":product})

