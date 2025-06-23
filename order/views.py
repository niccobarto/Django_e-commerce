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

# Create your views here.

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
                return redirect("view_checkout")
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

@login_required(login_url='login')
def view_checkout(request):
    customer=request.user
    cart_items = CartItem.objects.filter(customer=customer)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("view_cart")

    if not request.session.get("allow_checkout"):
        messages.warning(request, "Accedi al checkout solo passando dal carrello.")
        return redirect("view_cart")

    address=UserAddress.objects.get(id=request.session['checkout_address_id'],customer=customer)
    return render(request, 'order/checkout.html', {'address':address, 'cart_items':cart_items, 'total_price':cart_total_price(cart_items)})

@login_required(login_url='login')
def confirm_order(request):
    customer=request.user
    cart_items = CartItem.objects.filter(customer=customer)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
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
            quantity=item.quantity,
            price=quantity_price(item.product.price,item.quantity)
        )
        item.product.quantity -=  item.quantity
        item.product.save()
    cart_items.delete()

    request.session.pop("checkout_address_id", None)
    request.session.pop("allow_checkout", None)

    return redirect('home')