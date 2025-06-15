from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def home(request):
    products=Product.objects.all()
    return render(request, 'home.html', {"products":products})

def product_detail(request,product_id):
    product=Product.objects.get(pk=product_id)
    return render(request, 'product_detail.html', {"product":product})

def login_user(request):
    if request.method=="POST": #we're asking if the form has been posted(sent!!)
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "Logged in successfully")
            return redirect("home")
        else:
            messages.warning(request, "Login failed")
            return redirect("login")
    else:
        return render(request, "login.html")


def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')
