from django.shortcuts import render
from django.http import Http404
from .models import Category, Product


def categories_view(request):
    categories = Category.objects.filter().all()
    return render(request, 'storeapp/categories.html', {
        "categories": categories
    })


def category_view(request, category_id):
    if not Category.objects.filter(pk=category_id).exists():
        raise Http404("Category does not exist!")

    products = Product.objects.filter(category__pk=category_id).all()
    return render(request, 'storeapp/products.html', {
        "products": products
    })


def product_view(request, product_id):
    if not Product.objects.filter(pk=product_id).exists():
        raise Http404("Product does not exist!")

    product = Product.objects.filter(pk=product_id).first()
    return render(request, 'storeapp/product.html', {
        "product": product
    })


def add_to_cart_view(request, product_id):
    pass