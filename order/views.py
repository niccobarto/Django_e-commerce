from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from pyexpat.errors import messages
from django.contrib import messages
from accounts.forms import UserAddressForm
from store.models import Product
from accounts.models import UserAddress
from .models import Order,OrderItem
from cart.models import CartItem
from cart.utils import cart_total_price,quantity_price
from django.contrib.auth.decorators import permission_required

# Create your views here.

@permission_required('accounts.view_useraddress', raise_exception=True)
@permission_required('accounts.add_useraddress', raise_exception=True)
@login_required
def shipment_address(request):
    customer = request.user
    cart_items = CartItem.objects.filter(customer=customer)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("view_cart")
    address_form = UserAddressForm()
    addresses = UserAddress.objects.filter(customer=customer)

    if request.method == "POST":
        if 'checkout_submit' in request.POST:
            address_id = request.POST.get("address_id")
            if address_id:
                request.session["checkout_address_id"] = address_id
                request.session["allow_checkout"] = True
                return redirect("credit_card")
            else:
                messages.error(request, "Please select an address.")

        elif 'add_address_submit' in request.POST:
            address_form = UserAddressForm(request.POST)
            if address_form.is_valid():
                new_address = address_form.save(commit=False)
                new_address.customer = customer
                new_address.save()
                messages.success(request, "Address added successfully.")
                return redirect("shipment_address")
            else:
                messages.error(request, "Please correct the errors below.")

    return render(request, "order/shipment_address.html", {
        "add_address_form": address_form,
        "addresses": addresses
    })

@login_required(login_url="login")
def credit_card_info(request):
    if request.method=="POST":
        request.session["card_number"] = request.POST.get("card_number")
        request.session["card_expiry"] = request.POST.get("card_expiry")
        request.session["card_cv"] = request.POST.get("card_cv")
        request.session["card_holder"] = request.POST.get("card_holder")
        request.session["allow_checkout_payment"] = True
        return redirect("view_checkout")
    else:
        return render(request, "order/credit_card.html")

@login_required(login_url='login')
def view_checkout(request):
    customer=request.user
    cart_items = CartItem.objects.filter(customer=customer)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("view_cart")

    if not (request.session.get("allow_checkout") and request.session.get("allow_checkout_payment")):
        messages.warning(request, "Access the checkout by going through the cart.")
        return redirect("view_cart")
    if request.method == "POST":
        request.session["allow_final_checkout"] = True
        return redirect("confirm_order")
    else:
        address=UserAddress.objects.get(id=request.session['checkout_address_id'],customer=customer)
        return render(request, 'order/checkout.html', {'address':address, 'cart_items':cart_items, 'total_price':cart_total_price(cart_items)})

@permission_required('order.add_order',raise_exception=True)
@login_required(login_url='login')
def confirm_order(request):
    customer=request.user
    cart_items = CartItem.objects.filter(customer=customer)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("view_cart")

    if  not (request.session.get("allow_checkout") and request.session.get("allow_checkout_payment") and request.session.get("allow_final_checkout")):
        messages.warning(request, "Access the checkout by going through the cart")
        return redirect("view_cart")

    address=UserAddress.objects.get(id=request.session['checkout_address_id'],customer=customer)
    order= Order.objects.create(
        customer=customer,
        total_price=cart_total_price(cart_items),
        shipment_first_name = address.first_name,
        shipment_last_name=address.last_name,
        shipment_city=address.city,
        shipment_country=address.country,
        shipment_postal_code=address.postal_code,
        shipment_street_address=address.street_address,
    )
    for item in cart_items:
        order_item=OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            product_image = item.product.front_image.url if item.product.front_image else "",
            quantity=item.quantity,
            price=quantity_price(item.product.discounted_price(),item.quantity)
        )
        item.product.quantity -=  item.quantity
        item.product.save()
    cart_items.delete()

    request.session.pop("checkout_address_id", None)
    request.session.pop("allow_checkout", None)
    request.session.pop("allow_checkout_payment", None)
    request.session.pop("allow_final_checkout", None)

    return redirect('home')

@login_required(login_url='login')
def orders_history(request):
    customer = request.user
    orders = Order.objects.filter(customer=customer).order_by('-datetime')
    history=[]
    for order in orders:
        order_items=OrderItem.objects.filter(order=order)
        history.append((order_items,order))
    return render(request,'order/history.html',{'history':history})