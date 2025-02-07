from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from account.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('category/<int:category_id>/', category_detail, name='category_detail'),  # С ID
    path('product/<int:product_id>/add_review/', add_review, name='add_review'),
    path('category/', category_detail, name='category_list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
