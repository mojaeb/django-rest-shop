from django.urls import path, re_path
from rest_framework_simplejwt import views as jwt_views
from . import views

CHECK_SHIPPING_PRICE = 'https://public.api.tapin.ir/api/v1/public/check-price/'

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # products
    path('products/', views.get_products),
    path('brands/', views.get_brands),
    path('categories/', views.get_categories),
    path('product/<int:pid>/', views.get_product),
    path('like-product/<int:pid>/', views.like_product),
    path('unlike-product/<int:pid>/', views.unlike_product),
    path('product/<int:pid>/add-comment/', views.add_comment),
    path('product/remove-comment/<int:cid>/', views.remove_comment),

    # user
    path('notifications/', views.get_notifications),
    path('likes/', views.get_likes),
    # user address
    path('addresses/', views.get_addresses),
    path('address/<int:aid>/', views.address),
    path('address/', views.add_address),
    # public
    path('banners/', views.get_banners),
    path('sliders/', views.get_sliders),
    # shopping functionality
    path('add-to-cart/<int:product_id>/<int:quantity>/', views.add_to_cart),
    path('remove-from-cart/<int:order_item_id>/', views.remove_from_cart),
    path('seed-to-cart/', views.get_sliders),
    path('cart/', views.cart),
    path('checkout/', views.checkout),
    path('verify-payment', views.verify_payment, name="verify_payment"),
    path('increment-quantity/<int:order_item_id>', views.increase_quantity),
    path('decrement-quantity/<int:order_item_id>', views.decrease_quantity)
]
