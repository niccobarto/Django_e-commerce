from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import Product
from .models import CartItem
from store.utils import check_product_availability
from .utils import cart_total_items,cart_total_price

# Create your views here.

@login_required(login_url='login')
def view_cart(request):
    customer=request.user
    items=CartItem.objects.filter(customer=customer)
    cleaned_cart=[]
    for item in items:
        if item.product.is_active:
            if not check_product_availability(item.product.id,item.quantity):
                to_remove=item.quantity-item.product.quantity
                if item.quantity-to_remove <= 0:
                    item.delete()
                    messages.warning(request,f"{item.product.name} not available anymore")
                else:
                    item.quantity-=to_remove
                    item.save()
                    cleaned_cart.append(item)
                    messages.warning(request,f"Removed {to_remove} elements of {item.product.name} not available anymore")
            else:
                cleaned_cart.append(item)
        else:
            item.delete()
            messages.warning(request, f"{item.product.name} not available anymore")
    return render(request,"cart/cart.html",{'total_items':cart_total_items(cleaned_cart),'total_price':cart_total_price(cleaned_cart),'items':cleaned_cart})

@login_required(login_url='login')
def add_cart(request,product_id):
    customer = request.user
    product_selected=get_object_or_404(Product, id=product_id)
    #We verify if already exist a CartItem with a particular customer and product. If exist we only
    #increment the quantity, otherwise we create a new CartItem
    item_exists = CartItem.objects.filter(customer=customer, product=product_selected).exists()
    if item_exists:
        cart_item = CartItem.objects.get(customer=customer, product=product_selected)
        if check_product_availability(product_selected.pk, cart_item.quantity + 1):
            cart_item.quantity+=1
            cart_item.save()
        else:
            messages.warning(request,f"There are no more then {product_selected.quantity} elements available of {product_selected.name}")
    else:
        if check_product_availability(product_id,1):
            CartItem.objects.create(customer=customer, product=product_selected, quantity=1)
            messages.success(request, f"{product_selected.name} added to cart")
        else:
            messages.error(request,f"There are no more then {product_selected.quantity} elements available of {product_selected.name}")
    #Redirect to the page where the button "add to cart" was pressed
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required(login_url='login')
def remove_all_cart(request,product_id):
    customer = request.user
    product_selected=get_object_or_404(Product, id=product_id)
    try:
        cart_item=CartItem.objects.get(customer=customer, product=product_selected)
        cart_item.delete()
        messages.success(request, f"{product_selected.name} removed from cart")
    except CartItem.DoesNotExist:
        messages.error(request, f"{product_selected.name} not found in cart")
    return redirect('view_cart')


@login_required(login_url='login')
def decrease_quantity(request, product_id):
    customer = request.user
    product_selected = get_object_or_404(Product, pk=product_id)
    try:
        cart_item = CartItem.objects.get(customer=customer, product=product_selected)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
            messages.success(request, f"{product_selected.name} removed from cart")
    except CartItem.DoesNotExist:
        messages.warning(request, f"{product_selected.name} wasn't found in cart.")
    return redirect('view_cart')

