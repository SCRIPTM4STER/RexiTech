from django.contrib import admin
from .models_product import Product, Category, Review, ProductImage, Comment
from .models_order import Cart, CartItem, Order
from django.utils.html import format_html

# Admin setup for Product

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of empty forms to display

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'product_id', 'price', 'stock', 'created_at', 'updated_at', 'thumbnail')
    list_filter = ('category', 'price')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock')

    # Read-only fields
    readonly_fields = ('product_id',)
    
    inlines = [ProductImageInline]  # Add inlines for managing product images

    def thumbnail(self, obj):
        # Get the first image for the product
        if obj.images.exists():  # Check if there are any images
            first_image = obj.images.first()  # Get the first ProductImage instance
            return format_html('<img src="{}" style="width: 50px; height: 50px;"/>', first_image.image.url)
        return "No Image"

    thumbnail.short_description = 'Image'

admin.site.register(Product, ProductAdmin)

# Admin setup for Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)

# Admin setup for Cart with CartItems as inline
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [CartItemInline]

admin.site.register(Cart, CartAdmin)

# Admin setup for Order
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'created_at', 'total_price')
    search_fields = ('user__username', 'email')
    list_filter = ('created_at',)

admin.site.register(Order, OrderAdmin)


# Admin setup for Review
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'comment', 'rating', 'date')
    search_fields = ('product__name', 'comment')
    list_filter = ('rating', 'date')

admin.site.register(Review, ReviewAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'comment', 'reply', 'date')
    search_fields = ('product__name', 'comment')  # Ensure 'name' exists in Product model
    list_filter = ('date',)

admin.site.register(Comment, CommentAdmin)