from store.models import Product

def quantity_price(price, quantity):
    return price * quantity

def cart_total_price(cart_items):
    total=0
    for item in cart_items:
        total += quantity_price(item.product.discounted_price, item.quantity)
    return total

def cart_total_items(cart_items):
    total=0
    for item in cart_items:
        total+=item.quantity
    return total
