from cart.cart import CartSession


def cart(request):
    
    return {'cart' : CartSession(request.session), }