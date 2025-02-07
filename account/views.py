from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm 
from .models import CustomUser
from .forms import RegistrationForm
from shop.models import *

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
            user.set_password(form.cleaned_data["password"])  # Хешируем пароль
            user.save()  # Сохраняем пользователя в БД
            messages.success(request, "Регистрация успешна! Теперь войдите в систему.")
            return redirect("login")  
        else:
            messages.error(request, "Ошибка при регистрации. Проверьте данные.")
    else:
        form = RegistrationForm()
    
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        '''print(f"Попытка входа: {username}")'''
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Вы успешно вошли!")
            return redirect("user_profile")  
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
            print("Ошибка входа: пользователь не найден.")

    return render(request, "login.html")


@login_required
def profile_view(request):
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')  # Получаем отзывы текущего пользователя
    return render(request, 'user_profile.html', {'reviews': reviews})

@login_required
def basket(request):
    popular_categories = Category.objects.filter(is_popular=True)
    cart = get_cart(request)
    products = Product.objects.all()
    return render(request, "basket.html", {"cart": cart,'popular_categories': popular_categories, 'products': products})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из аккаунта.")
    return redirect("index") 


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserChangeForm

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        
        if form.is_valid():
            updated_user = form.save(commit=False)

            # Проверка уникальности email и phone_number
            if CustomUser.objects.exclude(id=request.user.id).filter(email=updated_user.email).exists():
                form.add_error('email', 'Пользователь с таким email уже существует.')
            elif CustomUser.objects.exclude(id=request.user.id).filter(phone_number=updated_user.phone_number).exists():
                form.add_error('phone_number', 'Пользователь с таким номером телефона уже существует.')
            else:
                updated_user.save()
                messages.success(request, 'Профиль успешно обновлён!')
                return redirect('user_profile')

        else:
            messages.error(request, 'Проверьте форму на ошибки.')
    
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem
from shop.models import Product
from django.contrib import messages

def get_cart(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key

    cart, created = Cart.objects.get_or_create(session_id=session_id, user=request.user if request.user.is_authenticated else None)
    return cart


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    
    cart, created = Cart.objects.get_or_create(session_id=request.session.session_key, user=request.user if request.user.is_authenticated else None)

    if cart.items.filter(product=product).exists():
        messages.info(request, 'Этот товар уже в вашей корзине.')
    else:
        CartItem.objects.create(cart=cart, product=product)

    return redirect('view_cart') 

def remove_from_cart(request, product_id):
    cart = get_cart(request)
    cart.items.filter(product_id=product_id).delete()
    return redirect('view_cart')


@login_required
def view_cart(request):
    popular_categories = Category.objects.filter(is_popular=True)
    
    products = Product.objects.all()
    cart = get_cart(request)
    return render(request, "basket.html", {"cart": cart, 'popular_categories': popular_categories, 'products': products})
