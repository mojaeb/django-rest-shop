from django.urls import re_path
from .views import CustomUserCreate

app_name = 'users'

urlpatterns = [
    re_path(r'^create/', CustomUserCreate.as_view(), name="create_user"),
]
