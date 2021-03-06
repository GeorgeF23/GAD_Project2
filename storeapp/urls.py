from django.urls import path
from .views import categories_view, category_view, product_view, add_to_cart_view, delete_from_cart_view, view_cart, finish_order, view_orders

app_name = 'storeapp'

urlpatterns = [
    path('categories/', categories_view, name='categories'),
    path('categories/<int:category_id>/', category_view, name='view_category'),
    path('products/<int:product_id>/', product_view, name='view_product'),
    path('cart/add/<int:product_id>', add_to_cart_view, name='add_to_cart'),
    path('cart/delete/<int:product_id>', delete_from_cart_view, name='delete_from_cart'),
    path('cart/view/', view_cart, name='view_cart'),
    path('cart/order', finish_order, name='finish_order'),
    path('orders/', view_orders, name='view_orders')
]