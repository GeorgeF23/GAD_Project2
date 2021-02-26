from django.urls import path
from .views import categories_view, category_view, product_view, add_to_cart_view, view_cart

app_name = 'storeapp'

urlpatterns = [
    path('categories/', categories_view, name='categories'),
    path('categories/<int:category_id>/', category_view, name='view_category'),
    path('products/<int:product_id>/', product_view, name='view_product'),
    path('cart/add/<int:product_id>', add_to_cart_view, name='add_to_cart'),
    path('cart/view/', view_cart, name='view_cart')
]