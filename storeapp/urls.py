from django.urls import path
from .views import categories_view, category_view, product_view, add_to_cart_view

app_name = 'storeapp'

urlpatterns = [
    path('categories/', categories_view, name='categories'),
    path('categories/<int:category_id>/', category_view, name='view_category'),
    path('products/<int:product_id>/', product_view, name='view_product')
]