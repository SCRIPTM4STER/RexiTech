from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/item_count/', views.cart_item_count, name='cart_item_count'),

    path('checkout/', views.checkout, name='checkout'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),


    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),

    path('search', views.search, name='product_search'),
    
    # URL pattern for product details, using product_id (alphanumeric)
    path('product/<str:product_id>/', views.product_detail, name='product_detail'),
    path("robots.txt", views.robots_txt, name="robots_txt"),


    # URL patterns for authentication views
    path('auth/register', views.register, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/profile/', views.profile, name='profile'),
    path('auth/profile/edit/', views.edit_profile, name='edit_profile'),
    path('auth/delete_account/', views.delete_account, name='delete_account'),
    path('auth/account_settings/', views.account_settings, name='account_settings'),
    path('auth/password_change/', views.change_password, name='change_password'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

