from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

AuthUserModel = get_user_model()


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ('R', 'Received'),  # order received by the store
        ('P', 'Processed'),  # the store processed the order and will send it to the courier
        ('D', 'Delivered'),  # the store gave the package to the courier
    )

    products = models.ManyToManyField(Product, through='OrderItem')
    client = models.ForeignKey(AuthUserModel, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='R')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def send_update_email(self, new_order=False):
        subject = 'GAD Store order'
        if new_order is False:
            message = f'The order with id {self.id} containing the following products: {[product.name for product in self.products.all()]} has changed it\'s status to: {self.get_status_display()}'
        else:
            message = f'The order with id {self.id} containing the following products: {[product.name for product in self.products.all()]} has been received and it\'s status is: {self.get_status_display()}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.client.email]

        send_mail(
            subject,
            message,
            email_from,
            recipient_list,
            fail_silently=False
        )


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
