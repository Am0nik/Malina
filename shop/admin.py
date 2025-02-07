from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_popular')
    list_filter = ('is_popular',)
    search_fields = ('name',)

admin.site.register(Product)
admin.site.register(Review)