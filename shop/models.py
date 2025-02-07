from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.functions import Lower
from unidecode import unidecode  # Добавляем импорт для транслитерации

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    image = models.ImageField(upload_to='categories/', verbose_name="Изображение", blank=True, null=True)
    is_popular = models.BooleanField(default=False, verbose_name="Популярная категория")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название товара")
    search_name = models.CharField(max_length=200, blank=True)  # Поле для быстрого поиска
    description = models.TextField(verbose_name="Описание товара")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение товара", blank=True, null=True)
    manufacturer = models.CharField(max_length=100, verbose_name="Производитель", blank=True, null=True)
    release_date = models.DateField(verbose_name="Дата выпуска товара")
    country_of_origin = models.CharField(max_length=100, verbose_name="Страна производства")
    price = models.CharField(max_length=100, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, default=1)
    add_info = models.TextField(default='', blank=True)

    def save(self, *args, **kwargs):
        self.search_name = unidecode(self.name.lower())  # Транслитерация + нижний регистр
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Review(models.Model):
    User = get_user_model()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')  # Добавляем related_name
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=True) 

    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.product.name}"
