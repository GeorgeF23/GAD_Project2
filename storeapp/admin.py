from django.contrib import admin
from .models import Product, Category, Order, OrderItem


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'address', 'price', 'status')

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data:
            obj.send_update_email()

        super(OrderAdmin, self).save_model(request, obj, form, change)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'final_price')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
