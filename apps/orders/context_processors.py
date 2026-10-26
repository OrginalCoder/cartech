from .cart import Cart


def cart_processor(request):
    return {
        'cart': Cart(request),
        'cart_count': len(Cart(request)),
    }
