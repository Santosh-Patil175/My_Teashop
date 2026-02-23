from django.contrib import admin
from .models import Category, Product, Wishlist, Review, Order, OrderItem


# ===============================
# Category Admin
# ===============================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


# ===============================
# Product Admin
# ===============================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    list_per_page = 10


# ===============================
# Wishlist Admin
# ===============================
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('user__username', 'product__name')
    ordering = ('-added_at',)


# ===============================
# Review Admin
# ===============================
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username')
    ordering = ('-created_at',)


# ===============================
# OrderItem Inline
# ===============================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# ===============================
# Order Admin
# ===============================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
    ordering = ('-created_at',)
    inlines = [OrderItemInline]