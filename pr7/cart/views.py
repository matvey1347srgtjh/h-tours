from django.shortcuts import render
from .cart import CartSession
from django.http import HttpRequest
from baza.models import Jewelry
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from baza.models import Jewelry




from django.contrib import messages

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from baza.models import Jewelry

def cart_add(request: HttpRequest, jew_id):
    cart = CartSession(request.session)
    jew_id_str = str(jew_id)

    
    if len(cart) > 0 and jew_id_str not in cart.cart:
        messages.error(request, "Вы не можете добавить разные туры в корзину. Пожалуйста, сначала очистите корзину.")
        return redirect(reverse('cart_detail'))

    
    cart.add(jew_id=jew_id)
    messages.success(request, "Тур добавлен в корзину.")
    return redirect(reverse('cart_detail'))

def cart_remove(request: HttpRequest, jew_id):
    cart = CartSession(request.session)
    jew = get_object_or_404(Jewelry, id=jew_id)
    cart.remove(jew=jew)
    return redirect(reverse('cart_detail'))



def cart_detail(request: HttpRequest):
    cart = CartSession(request.session)
    return render(request, 'cart_detail.html', context={
        'cart': cart
    })
    
def cart_clear(request: HttpRequest):
    cart = CartSession(request.session)
    cart.clear()
    return redirect(reverse('cart_detail'))


