from .models import Product


def check_product_availability(product_id, amount_request):
    product=Product.objects.get(pk=product_id)
    if product.quantity>=amount_request:
        return True
    else:
        return False