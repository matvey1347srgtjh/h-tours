from django.urls import path, include
from .views import get_base, o_nas, jewelry_list, get_jew_detail
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import register
from .views import search_jew

from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLogoutView
from .views import login_view
from .views import CustomLogoutView
from .views import create_or_edit_profile, revoke_google_token
from cart.views import cart_detail, cart_add, cart_remove, cart_clear
from .views import create_order
from chat.views import chat_session, send_message





urlpatterns = [
path('', get_base, name='home'),
path('onas/', o_nas, name='onas'),
path('tovary/', jewelry_list, name='tovary'),
path('jew/<int:pk>', get_jew_detail, name='jew_detail'),
path('register/', register, name = 'register'),
path('search/', views.search_jew, name='search'),
path('auth/', login_view, name='auth'),
path('logout/', CustomLogoutView.as_view(), name='logout'),
path('profile/', views.profile_view, name='profile_view'),
path('create-profile/', create_or_edit_profile, name='create_profile'),
path('cart/', cart_detail, name='cart_detail'),
path('cart/add/<int:jew_id>/', cart_add, name='cart_add'),
path('cart/remove/<int:jew_id>/', cart_remove, name='cart_remove'),
path('cart/clear/', cart_clear, name='cart_clear'),
path('order/', create_order, name='create_order'),
path('accounts/', include('allauth.urls')),
path('revoke-google-token/', revoke_google_token, name='revoke_google_token'),
path('favorites/add/<int:jewelry_id>/', views.add_to_favorites, name='add_to_favorites'),
path('favorites/remove/<int:jewelry_id>/', views.remove_from_favorites, name='remove_from_favorites'),
path('session/<int:admin_id>/', chat_session, name='chat_session'),
path('send/<int:session_id>/', send_message, name='send_message'),
path('leave_review/<int:order_id>/', views.leave_review, name='leave_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)