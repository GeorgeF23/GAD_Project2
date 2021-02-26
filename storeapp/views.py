from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
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


@login_required
def add_to_cart_view(request, product_id):
    if not Product.objects.filter(pk=product_id).exists():
        raise Http404("Product does not exist!")

    if 'cart' not in request.session:
        request.session['cart'] = []

    request.session['cart'].append(product_id)
    request.session.modified = True

    return redirect('storeapp:view_cart')


@login_required
def view_cart(request):
    products = []

    if 'cart' in request.session:
        for product_id in request.session['cart']:
            products.append(Product.objects.filter(pk=product_id).first())

    return render(request, 'storeapp/cart.html', {
        "products": products
    })
