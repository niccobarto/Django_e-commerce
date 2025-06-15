from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from accounts.forms import CustomUserCreationForm


# Create your views here.
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
        return render(request, "accounts/login.html")


def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')

def register_user(request):
    if request.method=="POST":
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "User created successfully")
            return redirect("home")
        else:
            messages.error(request, "Form invalid")
            return redirect("register")
    else:
        form=CustomUserCreationForm()
        return render(request,"accounts/register.html",{"form":form})