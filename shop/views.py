from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Review, Wishlist, Order, OrderItem
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, logout
from .forms import RegisterForm, OrderForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def home(request):
    query = request.GET.get('q')
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    categories = Category.objects.all()

    return render(request, 'home.html', {
        'products': products,
        'categories': categories
    })

def category_products(request, id):
    category = get_object_or_404(Category, id=id)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {
        'category': category,
        'products': products
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews
    })

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
    return render(request, 'register.html', {'form': form})

# Login View
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('home')
    return render(request, 'login.html', {'form': form})

#logout View

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def add_review(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )

    return redirect('product_detail', id=id)

@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('product_detail', id=id)


@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'items': items})

@login_required
def create_order(request, id):
    product = get_object_or_404(Product, id=id)

    order = Order.objects.create(
        user=request.user,
        total_price=product.price
    )

    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=1
    )

    return redirect('home')

from django.contrib.auth.decorators import login_required

@login_required
def create_order(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            total_price = product.price * quantity

            order = form.save(commit=False)
            order.user = request.user
            order.total_price = total_price
            order.save()

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

            return redirect('order_success')

    else:
        form = OrderForm()

    return render(request, 'checkout.html', {
        'form': form,
        'product': product
    })

def order_success(request):
    return render(request, 'order_success.html')
