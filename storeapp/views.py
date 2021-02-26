from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Order, OrderItem


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
def delete_from_cart_view(request, product_id):
    if 'cart' in request.session:
        if product_id in request.session['cart']:
            request.session['cart'].remove(product_id)
            request.session.modified = True

    return redirect('storeapp:view_cart')


def get_products_from_cart(cart):
    products = Product.objects.filter(pk__in=cart)
    return products


def get_products_price(products):
    price = 0
    for product in products:
        price += product.price
    return price


@login_required
def view_cart(request):
    products = []

    if 'cart' in request.session:
        products = get_products_from_cart(request.session['cart'])

    price = get_products_price(products)

    return render(request, 'storeapp/cart.html', {
        "products": products,
        "price": price
    })


@login_required
def finish_order(request):
    if 'cart' not in request.session or not request.session['cart']:
        return render(request, 'storeapp/cart.html', {
            "error": "Cart is empty!"
        })

    address = request.POST['order_address']
    if len(address) == 0:
        return render(request, 'storeapp/cart.html', {
            "error": "Invalid address!"
        })

    products = []

    if 'cart' in request.session:
        products = get_products_from_cart(request.session['cart'])

    order = Order(client=request.user, address=address)
    order.save()

    items = []
    for product in products:
        items.append(OrderItem(product_id=product.pk, order_id=order.pk, final_price=product.price))

    OrderItem.objects.bulk_create(items)

    request.session['cart'] = []
    request.session.modified = True
    return render(request, 'storeapp/cart.html', {
        "success": "Order placed!"
    })


@login_required
def view_orders(request):
    orders = Order.objects.filter(client=request.user).all()

    for order in orders:
        print(order)
        print(order.products.all())

    return render(request, 'storeapp/order.html', {
        "orders": orders
    })
