from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:id>/', views.category_products, name='category'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('review/<int:id>/', views.add_review, name='add_review'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('order/<int:id>/', views.create_order, name='create_order'),
    path('order/<int:id>/', views.create_order, name='create_order'),
    path('order-success/', views.order_success, name='order_success'),

]