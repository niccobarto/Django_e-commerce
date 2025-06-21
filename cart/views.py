from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from pyexpat.errors import messages
from django.contrib import messages
from store.models import Product
from accounts.models import CustomUser
from .models import CartItem
from store.utils import check_product_availability
from django.contrib.auth.password_validation import password_validators_help_texts
# Create your views here.

@login_required(login_url='login')
def view_cart(request):
    customer=CustomUser.objects.get(username=request.user.username)
    items=CartItem.objects.filter(customer=customer)
    total_item=0
    total_price=0
    for item in items:
        total_item+=item.quantity
        total_price+=(item.product.price*item.quantity)
    return render(request,"cart/cart.html",{'total_item':total_item,'total_price':total_price,'items':items})

@login_required(login_url='login')
def add_cart(request,product_id):
    customer=CustomUser.objects.get(username=request.user.username)
    product=get_object_or_404(Product,id=product_id)

    #We verify if already exist a CartItem with a particular customer and product. If exist we only
    #increment the quantity, otherwise we create a new CartItem
    item_exists = CartItem.objects.filter(customer=customer, product=product).exists()
    if item_exists:
        cart_item = CartItem.objects.get(customer=customer, product=product)
        if check_product_availability(product.pk,cart_item.quantity+1):
            cart_item.quantity+=1
            cart_item.save()
        else:
            messages.warning(request,f"There are no more then {product.quantity} elements available of {product.name}")
    else:
        if check_product_availability(product_id,1):
            CartItem.objects.create(customer=customer,product=product,quantity=1)
            messages.success(request, f"{product.name} added to cart")
        else:
            messages.error(request,f"There are no more then {product.quantity} elements available of {product.name}")
    #Redirect to the page where the button "add to cart" was pressed
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required(login_url='login')
def remove_all_cart(request,product_id):
    customer=CustomUser.objects.get(username=request.user.username)
    product=get_object_or_404(Product, id=product_id)
    try:
        cart_item=CartItem.objects.get(customer=customer,product=product)
        cart_item.delete()
        messages.success(request, f"{product.name} removed from cart")
    except CartItem.DoesNotExist:
        messages.error(request, f"{product.name} not found in cart")
    return redirect('view_cart')


@login_required(login_url='login')
def decrease_quantity(request, product_id):
    customer = CustomUser.objects.get(username=request.user.username)
    product = get_object_or_404(Product, pk=product_id)
    try:
        cart_item = CartItem.objects.get(customer=customer, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            messages.success(request, f"{product.name} removed from cart")
    except CartItem.DoesNotExist:
        messages.warning(request, f"{product.name} wasn't found in cart.")
    return redirect('view_cart')


