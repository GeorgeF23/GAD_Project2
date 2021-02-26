from django.contrib import admin
from .models import Product, Category, Order, OrderItem


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'address')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'final_price')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
