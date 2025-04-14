from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Jewelry
from django.contrib.auth import login, authenticate
from .form import RegisterForm
from django.http import HttpRequest
from django.db.models import Q
from .form import Login_Form
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.auth.decorators import login_required
from account1.models import Profile
from .form import ProfileForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .form import ProfileForm
from account1.models import Profile
from cart.cart import CartSession
from .form import OrderForm
from order.models import OrderItem, Order, PaymentStatus
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account1.models import Profile, Avatar
from .form import ProfileForm
from django.contrib.auth.models import User
from .models import Slide, Review



# Create your views here.

def get_base(request):
    slides = Slide.objects.all()
    reviews = Review.objects.select_related('user__avatar').all() 


    return render(request, 'home.html', {
        'title': 'base',
        'slides': slides,
        'reviews': reviews,  
    })
    
def o_nas(request):
    return render(request, 'onas.html', {
        'title': 'onas',
    })
    
    
def tovary(request):
    return render(request, 'tovary.html', {
        'title': 'tovary',
    })
    
    
    
# def jewelry_list(request):
#     jewelry_objects = Jewelry.objects.all()
#     context = {
#         'jewelry_objects': jewelry_objects
#     }
#     return render(request, 'tovary.html', context)
def jewelry_list(request):
    
    max_price = request.GET.get('max_price')
    jewelry_objects = Jewelry.objects.all()

    
        
    if max_price:
        jewelry_objects = jewelry_objects.filter(price__lte=max_price)

    cart = CartSession(request.session)
    context = {
        'jewelry_objects': jewelry_objects,
        'cart': cart
    }
    return render(request, 'tovary.html', context)

def get_jew_detail(request, pk):
    jew_detail = Jewelry.objects.get(pk=pk)
    return render(request, 'detail_jew.html', context = {
        'jew': jew_detail
    })
    
def register(request: HttpRequest):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', context={
        'title': 'Регистрация',
        'form': form,
    })
    
    
# def search_jew(request):
#     if request.method == "GET":
#         search = request.GET['search']
#         print(f"Search term: {search}")
#         jewelry_objects = Jewelry.objects.filter(
#             Q(name__icontains = search))
#         print(f"Found items: {jewelry_objects}")
#         return render(request, template_name='tovary.html', context={
#         'jewelry_objects' : jewelry_objects,
#         'title' : 'Ювелирные изделия'
#     } )
#     return redirect(reverse('home'))
def search_jew(request):
    if request.method == "GET":
        search = request.GET.get('search', '').strip() 
        print(f"Search term: {search}")

        if search:
            jewelry_objects = Jewelry.objects.filter(
                Q(name__icontains=search)
            )
        else:
            jewelry_objects = []
            

        return render(request, template_name='tovary.html', context={
            'jewelry_objects': jewelry_objects,
            'title': 'Ювелирные изделия'
        })
    return redirect(reverse('home'))

# def login_user(request: HttpRequest):
#     if request.method == 'POST':
#         form = Login_Form(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             if user is not None:
#                 login(request, 'login.html', context={
#                     'title': 'Авторизация',
#                     'form': form,
#                 })
def login_view(request):
    if request.method == 'POST':
        form = Login_Form(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
               
                login(request, user)

                
                return redirect('profile_view') 

        else:
           
            print(f"Form is not valid: {form.errors}") 
            return render(request, 'auth_faled.html', context={
                'title': 'Авторизация не пройдена',
                'form': form,
            })

    else:
        
        form = Login_Form()
        return render(request, 'auth.html', context={
            'title': 'Авторизация',
            'form': form,
        })
                
                
class CustomLogoutView(BaseLogoutView):
    template_name = 'logout.html'

    def get_next_page(self):
       
        if self.next_page:
            return super().get_next_page()
        return '/home/' 


import requests
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialToken

@login_required(login_url='auth')
def revoke_google_token(request):
    # Получите токен доступа пользователя
    social_token = SocialToken.objects.filter(account__user=request.user, account__provider='google').first()
    
    if social_token:
        # URL для отзыва токена
        revoke_url = 'https://accounts.google.com/o/oauth2/revoke'
        
        # Параметры запроса
        params = {'token': social_token.token}
        
        # Отправьте запрос на отзыв токена
        response = requests.post(revoke_url, params=params)
        
        if response.status_code == 200:
            # Успешный отзыв токена
            social_token.delete()  # Удалите токен из базы данных
            messages.success(request, "Токен доступа Google успешно отозван.")
        else:
            # Ошибка при отзыве токена
            messages.error(request, "Не удалось отозвать токен доступа Google.")
    
    return redirect('profile')


from account1.models import Avatar
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account1.models import Profile, Avatar
from order.models import Order
from .models import Favorite
from .form import ProfileForm
@login_required(login_url='auth')








@login_required(login_url='auth')
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    avatar, _ = Avatar.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if 'avatar' in request.FILES:
            avatar.avatar = request.FILES['avatar']
            avatar.save()
            messages.success(request, "Аватар успешно обновлен.")
        else:
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()

            if not username:
                messages.error(request, "Имя пользователя не может быть пустым.")
                return redirect('profile_view')

            user = request.user
            user.username = username
            user.email = email
            user.save()

            profile.phone = phone
            profile.save()

            messages.success(request, "Профиль успешно обновлен.")
            return redirect('profile_view')
    else:
        form = ProfileForm(instance=profile)

    favorites = Favorite.objects.filter(user=request.user).select_related('jewelry')
    favorite_ids = favorites.values_list('jewelry_id', flat=True)

    orders = Order.objects.filter(customer_user=request.user)
    
    return render(request, 'profile.html', context={
        'form': form,
        'avatar': avatar,
        'profile': profile,
        'orders': orders,
        'favorites': favorites,
        'favorite_ids': favorite_ids 
    })
   
    
    

def create_or_edit_profile(request):
   
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)  
        if form.is_valid():
            form.save()  
            messages.success(request, "Профиль успешно обновлен." if not created else "Профиль успешно создан.")
            return redirect('profile_view')  
    else:
        form = ProfileForm(instance=profile) 

    return render(request, 'create_profile.html', {'form': form})




# @login_required(login_url='auth')
# def create_order(request: HttpRequest):
#     cart = CartSession(request.session)
#     if request.method == "POST":
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.customer_user = request.user
#             order.save()
#             for item_cart in cart:
#                 OrderItem.objects.create(order=order, jew=item_cart['jew'], quantity=item_cart['quantity']).save()
#             cart.clear()
#             return redirect(reverse('profile'))
#         else:
#             form = OrderForm()   
from django.shortcuts import render, redirect
from baza.form import OrderForm
from order.models import Order, OrderItem
from cart.cart import CartSession

from django.shortcuts import render, redirect
from baza.form import OrderForm
from order.models import Order, OrderItem
from cart.cart import CartSession
from datetime import timedelta

@login_required(login_url='auth')
def create_order(request):
    cart = CartSession(request.session)

    if not cart:
        return redirect('cart_detail')

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer_user = request.user
            order.status = PaymentStatus.NOT_STARTED
            order.paid = False
            order.save()  # Сначала сохраняем заказ

            for item_cart in cart:
                OrderItem.objects.create(order=order, jew=item_cart['jew'], quantity=item_cart['quantity'])

            # Рассчитываем end_date после создания всех OrderItem
            if order.start_date:
                order_item = order.items.first()
                if order_item:
                    order.end_date = order.start_date + timedelta(days=order_item.jew.days)
                order.save()  # Сохраняем изменения в order

            cart.clear()
            return redirect('profile_view')
    else:
        form = OrderForm()

    return render(request, 'cart_detail.html', {'orderForm': form, 'cart': cart})




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Jewelry, Favorite

@login_required(login_url='auth')
def add_to_favorites(request, jewelry_id):
    jewelry = get_object_or_404(Jewelry, id=jewelry_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, jewelry=jewelry)
    
    if created:
        messages.success(request, f"{jewelry.name} добавлено в избранное.")
    else:
        messages.info(request, f"{jewelry.name} уже в избранном.")
    
    return redirect('profile_view')

@login_required(login_url='auth')
def remove_from_favorites(request, jewelry_id):
    jewelry = get_object_or_404(Jewelry, id=jewelry_id)
    favorite = Favorite.objects.filter(user=request.user, jewelry=jewelry).first()
    
    if favorite:
        favorite.delete()
        messages.success(request, f"{jewelry.name} удалено из избранного.")
    else:
        messages.info(request, f"{jewelry.name} не найдено в избранном.")
    
    return redirect('profile_view')





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order, Review
from .form import ReviewForm

@login_required
def leave_review(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer_user=request.user, status='COMPLETED')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.order = order
            review.user = request.user
            review.save()
            return redirect('profile_view')
    else:
        form = ReviewForm()

    return render(request, 'leave_review.html', {'form': form, 'order': order})