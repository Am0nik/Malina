from django.urls import path
from .views import *
from shop.views import *

urlpatterns = [
    path('profile/', profile_view, name='user_profile'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('basket/', basket, name='basket'),
    path("logout/", logout_view, name="logout"),
    path('edit_profile',edit_profile, name='edit_profile'),
    path('cart/', view_cart, name="view_cart"),
    path('cart/add/<int:product_id>/', add_to_cart, name="add_to_cart"),
    path('cart/remove/<int:product_id>/', remove_from_cart, name="remove_from_cart"),
    path('.../shop/product/<int:product_id>/',product_detail, name='product_detail'),

]
