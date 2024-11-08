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
    path('checkout/', views.checkout, name='checkout'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),

    path('search', views.search, name='product_search'),
    
    # URL pattern for product details, using product_id (alphanumeric)
    path('product/<str:product_id>/', views.product_detail, name='product_detail'),
    path("robots.txt", views.robots_txt, name="robots_txt"),


    # URL patterns for authentication views
    path('register', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

