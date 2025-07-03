from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render,redirect
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.password_validation import password_validators_help_texts
from accounts.forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserChangeForm, UserAddressForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import UserAddress
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
def login_user(request):
    next_url = request.GET.get("next", "")
    if request.method=="POST": #we're asking if the form has been posted(sent!!)
        form=CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            messages.success(request, "Logged in successfully")
            next_url = request.POST.get("next") or request.GET.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "accounts/login.html",{"next":next_url,"form":form})
    else:
        form = CustomUserLoginForm()
        return render(request, "accounts/login.html",{"next":next_url,"form":form})


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
            help_texts = password_validators_help_texts()
            return render(request, "accounts/register.html", {"creation_form": form, "help_texts": help_texts})
    else:
        form=CustomUserCreationForm()
        help_texts=password_validators_help_texts()
        return render(request,"accounts/register.html",{"creation_form":form,"help_texts":help_texts})

@login_required(login_url="login")
def view_account(request):
    return render(request,'accounts/view_account.html')

@permission_required('accounts.change_customuser',raise_exception=True)
@login_required(login_url='login')
def change_password(request):
    if request.method=="POST":
        form=PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user=form.save()
            update_session_auth_hash(request, user)
            return redirect('view_account')
        else:
            messages.error(request,"Errors on the password change")
    else:
        form=PasswordChangeForm(request.user)
    return render(request,'accounts/change_password.html',{'form':form})

@permission_required('accounts.view_useraddress', raise_exception=True)
@permission_required('accounts.add_useraddress', raise_exception=True)
@permission_required('accounts.change_customuser',raise_exception=True)
@login_required(login_url='login')
def manage_addresses(request):
    customer=request.user
    address_form=UserAddressForm()
    addresses=UserAddress.objects.filter(customer=customer)
    if request.method=="POST":
        action = request.POST.get('action')
        delete_address=request.POST.get('delete_address_id')
        if action=="delete":
            if delete_address:
                UserAddress.objects.filter(id=delete_address).delete()
                messages.success(request,"Address deleted")
            return redirect('manage_addresses')
        if action=="add":
            address_form = UserAddressForm(request.POST)
            if address_form.is_valid():
                new_address = address_form.save(commit=False)
                new_address.customer = customer
                new_address.save()
                messages.success(request, "Address added successfully.")
                return redirect("manage_addresses")
            else:
                messages.error(request, "Please correct the errors below.")
    return render(request, "accounts/manage_addresses.html", {
        "add_address_form": address_form,
        "addresses": addresses
    })

def edit_address(request,address_id):
    address=UserAddress.objects.get(id=address_id)
    user=request.user
    if request.method == 'POST':
        form = UserAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Addres updated with success")
            return redirect('manage_addresses')
    else:
        form = UserAddressForm(instance=address)

    return render(request, 'accounts/edit_address.html', {'form': form})

@permission_required('accounts.change_customuser',raise_exception=True)
@login_required(login_url="login")
def edit_account(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('view_account')
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'accounts/edit_account.html', {'form': form})