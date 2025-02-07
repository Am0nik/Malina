from django.shortcuts import render
from shop.models import *

def index(request):
    popular_categories = Category.objects.filter(is_popular=True)
    
    products = Product.objects.all()

    print(popular_categories)
    return render(request, 'index.html', {'popular_categories': popular_categories, 'products': products})

