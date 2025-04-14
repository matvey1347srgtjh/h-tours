from django.contrib.sessions.backends.base import SessionBase
from baza.models import Jewelry
from django.shortcuts import render, redirect, get_object_or_404

class CartSession(SessionBase):
    CART_SESSION_ID = 'cart'
    
    
    def __init__(self, session: dict) -> None:
        self.session : dict = session
        self.cart = self.session.get(self.CART_SESSION_ID)
        self.ids = []
        
        if not self.cart:
            
            self.cart = self.session[self.CART_SESSION_ID] = {}
            
    # def __iter__(self):
        
    #     jew_ids = self.cart.keys()
        
    #     jewelrys = Jewelry.objects.filter(id__in=jew_ids)
        
    #     cart = self.cart.copy()
        
    #     for jew in jewelrys:
    #         cart[str(jew.id)]['jew'] = jew
            
    #     for item in cart.values():
    #         item['price'] = int(item['price'])
    #         item['total_price'] = item['price'] * item['quantity']
    #         yield item
    def __iter__(self):

        jew_ids = self.cart.keys()

        jewelrys = Jewelry.objects.filter(id__in=jew_ids)

        cart = self.cart.copy()

        for jew in jewelrys:
            cart[str(jew.id)]['jew'] = jew

        self.ids = list(jew_ids)

        for item in cart.values():
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
            
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def save(self):
        self.session.modified = True
        
    # def add(self, jew, quantity=1, update_quantity=False):
    #     jew_id = str(jew.id)
        
    #     if jew_id not in self.cart:
    #         self.cart[jew_id] = {'quantity' : 0, 'price': jew.price}
            
    #     if update_quantity:
    #         self.cart[jew_id]['quantity'] = quantity
            
    #     else:
    #         self.cart[jew_id]['quantity'] += quantity
    #     self.save()
    
    def add(self, jew_id, quantity=1, update_quantity=False):

        if str(jew_id) not in self.cart:
            jew = get_object_or_404(Jewelry, id=jew_id)
            self.cart[str(jew_id)] = {'quantity' : 0, 'price': float(jew.price)}

        if update_quantity:
            self.cart[str(jew_id)]['quantity'] = quantity

        else:
            self.cart[str(jew_id)]['quantity'] += quantity
        self.save()
        
    def remove(self, jew):
        jew_id = str(jew.id)
        
        if jew_id in self.cart:
            if self.cart[jew_id]['quantity'] > 1:
                self.cart[jew_id]['quantity'] -=1
            else:
                del self.cart[jew_id]
            self.save()

    def get_total_price(self):
        
        return sum(int(item['price']) * int(item['quantity']) for item in self.cart.values())
    
    def clear(self):
        del self.session[self.CART_SESSION_ID]
        self.save()
        