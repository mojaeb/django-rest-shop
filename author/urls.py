from django.urls import path, re_path
from rest_framework_simplejwt import views as jwt_views
from . import views


urlpatterns = [
    path('', views.index),
    path('orders', views.get_orders, name='orders'),
    path('order/<int:pk>', views.get_order, name='order'),
    path('available-in-warehouse/<int:order_id>', views.available_in_warehouse),
    path('deliver/<int:order_id>', views.deliver),
    path('enable-return/<int:order_id>', views.enable_return),
    path('disable-return/<int:order_id>', views.disable_return),
]
