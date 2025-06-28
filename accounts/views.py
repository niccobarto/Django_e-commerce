from django.shortcuts import render,redirect
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.password_validation import password_validators_help_texts
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
            next_url = request.POST.get("next") or request.GET.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("home")
        else:
            messages.warning(request, "Login failed")
            return redirect("login")
    else:
        next_url = request.GET.get("next","")
        return render(request, "accounts/login.html",{"next":next_url})


def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('home')

def register_user(request):
    if request.method=="POST":
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            customer_group=Group.objects.get(name="Customer")
            user.groups.add(customer_group)
            messages.success(request, "User created successfully")
            login(request,user)
            return redirect("home")
        else:
            messages.error(request, "Form invalid")
            return redirect("register")
    else:
        form=CustomUserCreationForm()
        help_texts=password_validators_help_texts()
        return render(request,"accounts/register.html",{"creation_form":form,"help_texts":help_texts})