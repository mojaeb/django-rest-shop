from django.urls import re_path
from .views import CustomUserCreate, BlacklistTokenUpdateView

app_name = 'users'

urlpatterns = [
    re_path(r'^create/', CustomUserCreate.as_view(), name="create_user"),
    re_path(r'^logout/blacklist/', BlacklistTokenUpdateView.as_view(),
         name='blacklist')
]
