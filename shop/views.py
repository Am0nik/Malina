from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from .models import Product, Category, Review
from .forms import ReviewForm

def index(request):
    popular_categories = Category.objects.all() 
    
    return render(request, 'index.html', { 'popular_categories': popular_categories})


from unidecode import unidecode  # Добавляем импорт транслитерации

def category_detail(request, category_id=None):
    """Страница категории с фильтрацией товаров и поиском."""
    print(f"category_id: {category_id}")

    products = Product.objects.all()
    category = None

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)
        print(f"Фильтруем товары по категории: {category}")

    query = request.GET.get('search', '').strip()
    print(f"Получен поисковый запрос: '{query}'")

    if query:
        # Преобразуем в нижний регистр + транслитерация
        normalized_query = unidecode(query.lower())
        print(f"Транслитерированный запрос: '{normalized_query}'")

        # Фильтруем по оригинальному и транслитерированному названию
        products = products.annotate(
            lower_name=Lower('name'),
            search_name_lower=Lower('search_name')
        ).filter(lower_name__icontains=query) | products.filter(search_name__icontains=normalized_query)

        print(f"Найдено товаров по запросу '{query}': {products.count()}")

    print(f"Всего товаров для отображения: {products.count()}")

    return render(request, 'index.html', {
        'category': category,
        'products': products,
        'popular_categories': Category.objects.all(),
        'search_query': query,
    })


@login_required
def product_detail(request, product_id):
    """Детальная страница товара с отзывами."""
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all().order_by('-created_at')  # Используем related_name='reviews'
    popular_categories = Category.objects.all() 
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')  # Перенаправляем на страницу входа

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Подставляем текущего пользователя
            review.product = product
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'product.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
        'popular_categories': popular_categories
    })


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        text = request.POST.get("text")
        rating = request.POST.get("rating")  # Получаем рейтинг из формы
        if text and rating:
            Review.objects.create(user=request.user, product=product, text=text, rating=int(rating))
    return redirect('product_detail', product_id=product_id)